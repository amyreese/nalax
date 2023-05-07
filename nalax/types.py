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


class Agent(NamedTuple):
    device: str
    os: str
    browser: str


class EventRow(NamedTuple):
    timestamp: int
    host: str
    path: str
    method: str
    status: int
    region: str
    device: str
    os: str
    browser: str


@dataclass
class Event:
    timestamp: arrow.Arrow
    host: str
    path: str
    method: str
    status: int
    region: str
    agent: Agent

    @classmethod
    def row_factory(cls, cursor, row) -> "Event":
        return Event(
            timestamp=arrow.get(row[0]),
            host=row[1],
            path=row[2],
            method=row[3],
            status=row[4],
            region=row[5],
            agent=Agent(row[6], row[7], row[8]),
        )

    def as_row(self) -> EventRow:
        return EventRow(
            timestamp=self.timestamp.int_timestamp,
            host=self.host,
            path=self.path,
            method=self.method,
            status=self.status,
            region=self.region,
            device=self.agent.device,
            os=self.agent.os,
            browser=self.agent.browser,
        )
