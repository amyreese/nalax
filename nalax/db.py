import sqlite3 as sqlite

from rich import print
import arrow

from .schema import SCHEMA, SCHEMA_INSERT, SCHEMA_SELECT


def connect(loc: str) -> sqlite.Connection:
    conn = sqlite.connect(loc)
    conn.row_factory = sqlite.Row
    return conn


def update_schema(conn: sqlite.Connection) -> int:
    cursor = conn.cursor()

    version = 0
    latest = len(SCHEMA)
    while version < latest:
        now = arrow.utcnow().int_timestamp
        print(version, SCHEMA[version])
        cursor.execute(SCHEMA[version])
        print(SCHEMA_INSERT, version, now)
        cursor.execute(SCHEMA_INSERT, (version, now))

        # look for the *next* schema to apply
        result = cursor.execute(SCHEMA_SELECT)
        last_version, _timestamp = result.fetchone()
        print(SCHEMA_SELECT, last_version, _timestamp)
        version = last_version + 1

    conn.commit()
    return last_version