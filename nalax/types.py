# Copyright Amethyst Reese
# Licensed under the MIT license

from dataclasses import dataclass
from ipaddress import IPv4Address, IPv6Address
from pathlib import Path
from typing import NamedTuple, TypeAlias, Union

import arrow

IPAddress: TypeAlias = Union[IPv4Address, IPv6Address]


@dataclass
class Options:
    database: Path


class EventRow(NamedTuple):
    timestamp: int
    host: str
    path: str
    method: str
    status: int
    referrer: str
    region: str
    agent: str


@dataclass
class Event:
    timestamp: arrow.Arrow
    host: str
    path: str
    method: str
    status: int
    referrer: str
    region: str
    agent: str

    @classmethod
    def row_factory(cls, cursor, row) -> "Event":
        return Event(
            timestamp=arrow.get(row[0]),
            host=row[1],
            path=row[2],
            method=row[3],
            status=row[4],
            referrer=row[5],
            region=row[6],
            agent=row[7],
        )

    def as_row(self) -> EventRow:
        return EventRow(
            timestamp=self.timestamp.int_timestamp,
            host=self.host,
            path=self.path,
            method=self.method,
            status=self.status,
            referrer=self.referrer,
            region=self.region,
            agent=self.agent,
        )
