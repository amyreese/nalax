# Copyright Amethyst Reese
# Licensed under the MIT license

from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

import arrow


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
    network: str
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
    network: str
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
            network=row[6],
            agent=Agent(row[7], row[8], row[9]),
        )

    def as_row(self) -> EventRow:
        return EventRow(
            timestamp=self.timestamp.int_timestamp,
            host=self.host,
            path=self.path,
            method=self.method,
            status=self.status,
            region=self.region,
            network=self.network,
            device=self.agent.device,
            os=self.agent.os,
            browser=self.agent.browser,
        )
