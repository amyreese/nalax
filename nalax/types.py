# Copyright Amethyst Reese
# Licensed under the MIT license

from dataclasses import dataclass
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address
from typing import TypeAlias, Union

IPAddress: TypeAlias = Union[IPv4Address, IPv6Address]


@dataclass
class Event:
    timestamp: datetime
    host: str
    method: str
    path: str
    status: int
    referrer: str
    remote: IPAddress
    agent: str
