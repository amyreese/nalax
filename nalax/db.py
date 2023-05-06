import sqlite3 as sqlite
from collections import defaultdict
from pathlib import Path

import arrow
from rich import print

from .schema import SCHEMA, SCHEMA_INSERT, SCHEMA_SELECT
from .types import Event


def connect(location: Path) -> sqlite.Connection:
    conn = sqlite.connect(location.as_posix())
    conn.row_factory = sqlite.Row
    return conn


def update_schema(database: Path) -> int:
    with connect(database) as conn:
        cursor = conn.cursor()

        version = 0
        latest = len(SCHEMA)
        while version < latest:
            now = arrow.utcnow().int_timestamp
            print(version, SCHEMA[version])
            cursor.execute(SCHEMA[version])
            print(SCHEMA_INSERT, version, now)
            cursor.execute(SCHEMA_INSERT, (version, now))
            conn.commit()

            # look for the *next* schema to apply
            result = cursor.execute(SCHEMA_SELECT)
            last_version, _timestamp = result.fetchone()
            print(SCHEMA_SELECT, last_version, _timestamp)
            version = last_version + 1

        conn.commit()
        return last_version


def insert_events(database: Path, batch: list[Event]) -> None:
    with connect(database) as conn:
        cursor = conn.cursor()
        query = """
            insert into `nalax_events` (
                `timestamp`, `host`, `path`, `method`,
                `status`, `referrer`, `region`, `agent`
            ) values
        """ + ", ".join(
            ["(?, ?, ?, ?, ?, ?, ?, ?)"] * len(batch)
        )
        params = []
        for event in batch:
            params += event.as_row()

        cursor.execute(query, params)
        conn.commit()


def aggregate_daily_events(
    database: Path, threshold: int | None = None, purge: bool = True
) -> None:
    threshold = threshold or arrow.utcnow().floor("day").int_timestamp

    daily_pages: dict[tuple, int] = defaultdict(int)
    daily_regions: dict[tuple, int] = defaultdict(int)

    with connect(database) as conn:
        cursor = conn.cursor()
        cursor.row_factory = Event.row_factory

        query = """
            select * from `nalax_events` where `timestamp` < ?
        """
        params = (threshold,)
        result = cursor.execute(query, params)
        while events := result.fetchmany():
            for event in events:
                event: Event
                print(event)
                t = event.timestamp

                # daily pages
                bucket = (t.year, t.month, t.day, event.host, event.path, event.method)
                daily_pages[bucket] += 1

                # daily regions
                bucket = (t.year, t.month, t.day, event.host, event.region)
                daily_regions[bucket] += 1

        print("daily_pages:", daily_pages)
        print("daily_regions:", daily_regions)

        # daily pages
        query = """
            insert into `nalax_daily_pages`
                (`year`, `month`, `day`, `host`, `path`, `method`, `count`)
                values (?, ?, ?, ?, ?, ?, ?)
                on conflict(`year`, `month`, `day`, `host`, `path`, `method`)
                    do update set `count` = `count` + excluded.count
        """
        for (year, month, day, host, path, method), count in daily_pages.items():
            params = (year, month, day, host, path, method, count)
            cursor.execute(query, params)

        # daily regions
        query = """
            insert into `nalax_daily_regions`
                (`year`, `month`, `day`, `host`, `region`, `count`)
                values (?, ?, ?, ?, ?, ?)
                on conflict(`year`, `month`, `day`, `host`, `region`)
                    do update set `count` = `count` + excluded.count
        """
        for (year, month, day, host, region), count in daily_regions.items():
            params = (year, month, day, host, region, count)
            cursor.execute(query, params)

        if purge:
            query = """
                delete from `nalax_events` where `timestamp` < ?
            """
            params = (threshold,)
            cursor.execute(query, params)

        conn.commit()
