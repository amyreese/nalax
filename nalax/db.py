# Copyright Amethyst Reese
# Licensed under the MIT license

import logging
import sqlite3 as sqlite
from collections import defaultdict
from pathlib import Path

import arrow
from rich import print

from .schema import SCHEMA, SCHEMA_INSERT, SCHEMA_SELECT
from .types import Event

LOG = logging.getLogger(__name__)


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
            LOG.debug("Upgrade DB SCHEMA[%d]:\n%s", version, SCHEMA[version])
            cursor.execute(SCHEMA[version])
            cursor.execute(SCHEMA_INSERT, (version, now))
            conn.commit()

            # look for the *next* schema to apply
            result = cursor.execute(SCHEMA_SELECT)
            last_version, _timestamp = result.fetchone()
            LOG.debug(
                "DB on schema version %d as of %s", last_version, arrow.get(_timestamp)
            )
            version = last_version + 1

        conn.commit()
        return last_version


def insert_events(database: Path, batch: list[Event]) -> None:
    with connect(database) as conn:
        cursor = conn.cursor()
        query = """
            insert into `nalax_events` (
                `timestamp`, `host`, `path`, `method`,
                `status`, `region`, `device`, `os`, `browser`
            ) values
        """ + ", ".join(
            ["(?, ?, ?, ?, ?, ?, ?, ?, ?)"] * len(batch)
        )
        params = []
        for event in batch:
            params += event.as_row()

        cursor.execute(query, params)
        conn.commit()


def aggregate_daily_events(database: Path, before: arrow.Arrow) -> int:
    threshold = before.int_timestamp

    daily_pages: dict[tuple, int] = defaultdict(int)
    daily_regions: dict[tuple, int] = defaultdict(int)
    daily_devices: dict[tuple, int] = defaultdict(int)

    with connect(database) as conn:
        cursor = conn.cursor()
        cursor.row_factory = Event.row_factory

        query = """
            select * from `nalax_events` where `timestamp` < ?
        """
        params = (threshold,)
        result = cursor.execute(query, params)

        event_count = 0
        while events := result.fetchmany():
            for event in events:
                event: Event
                event_count += 1
                print(event)
                t = event.timestamp

                # daily pages
                bucket = (t.year, t.month, t.day, event.host, event.path, event.method)
                daily_pages[bucket] += 1

                # daily regions
                bucket = (t.year, t.month, t.day, event.host, event.region)
                daily_regions[bucket] += 1

                # daily devices
                bucket = (
                    t.year,
                    t.month,
                    t.day,
                    event.host,
                    event.agent.device,
                    event.agent.os,
                    event.agent.browser,
                )
                daily_devices[bucket] += 1

        print("daily_pages:", daily_pages)
        print("daily_regions:", daily_regions)
        print("daily_devices:", daily_devices)

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

        # daily devices
        query = """
            insert into `nalax_daily_devices`
                (`year`, `month`, `day`, `host`, `device`, `os`, `browser`, `count`)
                values (?, ?, ?, ?, ?, ?, ?, ?)
                on conflict(`year`, `month`, `day`, `host`, `device`, `os`, `browser`)
                    do update set `count` = `count` + excluded.count
        """
        for (
            year,
            month,
            day,
            host,
            device,
            dos,
            browser,
        ), count in daily_devices.items():
            params = (year, month, day, host, device, dos, browser, count)
            cursor.execute(query, params)

        # remove aggregated events
        query = """
            delete from `nalax_events` where `timestamp` < ?
        """
        params = (threshold,)
        cursor.execute(query, params)

        conn.commit()
        return event_count
