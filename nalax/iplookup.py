# Copyright Amethyst Reese
# Licensed under the MIT license

from pathlib import Path
from typing import Generator, NamedTuple
import pkgutil
from io import StringIO
from bisect import bisect
from rich import print
from ipaddress import ip_address
from .types import IPAddress, IPv4Address, IPv6Address

class IPv4Range(NamedTuple):
    start: int
    end: int
    region: str


IP2COUNTRY_V4: list[IPv4Range] = []


def load() -> None:
    global IP2COUNTRY_V4

    data = pkgutil.get_data("nalax", "vendor/ip2asn/ip2country-v4-u32.tsv").decode("utf-8")
    def ingest(content: StringIO) -> Generator[IPv4Range, None, None]:
        for line in content:
            values = line.strip().split()
            match values:
                case [a, b, c]:
                    yield IPv4Range(int(a), int(b), c)
                case [a, b]:
                    yield IPv4Range(int(a), int(b), "None")
                case _:
                    continue
            
    IP2COUNTRY_V4 = sorted(ingest(StringIO(data)))


def lookup(ip: IPAddress) -> str:
    if isinstance(ip, IPv6Address):
        return "IPv6"
    else:
        ip32 = int(ip)
        idx = bisect(IP2COUNTRY_V4, (ip32,))
        if idx >= len(IP2COUNTRY_V4):
            idx -= 1
        ipr = IP2COUNTRY_V4[idx]
        if ip32 < ipr.start:
            ipr = IP2COUNTRY_V4[idx - 1]
        if ip32 > ipr.end:
            return "BIG"
        return ipr.region

if __name__ == "__main__":
    import sys
    addrs = sys.argv[1:]

    load()
    for ips in addrs or (
        "174.160.149.129",
        "192.168.0.1",
        "127.0.0.1",
        "::",
    ):
        ip = ip_address(ips)
        cc = lookup(ip)
        print(f"{ips} => {cc}")