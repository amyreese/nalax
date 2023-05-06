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
            `host` text,
            `timestamp` int
        )
    """
}

for i in range(len(SCHEMA)):
    assert i in SCHEMA