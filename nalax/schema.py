# Copyright Amethyst Reese
# Licensed under the MIT license

SCHEMA_SELECT = """
    select `version`, `timestamp` from `nalax_schema`
    order by `version` desc
    limit 1
"""

SCHEMA_INSERT = """
    insert or ignore into `nalax_schema`
        (`version`, `timestamp`)
        values (?, ?)
"""

SCHEMA: dict[int, str] = {
    0: """
        create table if not exists `nalax_schema` (
            `version` int primary key,
            `timestamp` int
        );
    """,
    1: """
        create table if not exists `nalax_events` (
            `timestamp` int,
            `host` text,
            `path` text,
            `method` text,
            `status` int,
            `referrer` text,
            `region` text,
            `device` text,
            `os` text,
            `browser` text
        )
    """,
    2: """
        create index if not exists `idx_nalax_events_host_path`
            on `nalax_events` (`host`, `path`);
    """,
    3: """
        create table if not exists `nalax_daily_pages` (
            `year` int,
            `month` int,
            `day` int,
            `host` text,
            `path` text,
            `method` text,
            `count` int
        )
    """,
    4: """
        create unique index `idx_unique_nalax_daily_pages`
            on `nalax_daily_pages` (`year`, `month`, `day`, `host`, `path`, `method`)
    """,
    5: """
        create table if not exists `nalax_daily_regions` (
            `year` int,
            `month` int,
            `day` int,
            `host` text,
            `region` text,
            `count` int
        )
    """,
    6: """
        create unique index `idx_unique_nalax_daily_regions`
            on `nalax_daily_regions` (`year`, `month`, `day`, `host`, `region`)
    """,
    7: """
        create table if not exists `nalax_daily_devices` (
            `year` int,
            `month` int,
            `day` int,
            `host` text,
            `device` text,
            `os` text,
            `browser` text,
            `count` int
        )
    """,
    8: """
        create unique index `idx_unique_nalax_daily_devices`
            on `nalax_daily_devices` (
                `year`, `month`, `day`, `host`,
                `device`, `os`, `browser`
            )
    """,
}

for key in SCHEMA:
    assert isinstance(key, int), f"SCHEMA[{key!r}] is not an integer"
    assert isinstance(SCHEMA[key], str), f"SCHEMA[{key}] is not a string value"

for i in range(len(SCHEMA)):
    assert i in SCHEMA, f"SCHEMA[{i}] is missing"
    assert SCHEMA[i].strip(), f"SCHEMA[{i}] is empty"
