# Copyright Amethyst Reese
# Licensed under the MIT license

import pkgutil
from bisect import bisect
from functools import lru_cache
from io import StringIO
from ipaddress import ip_address, IPv6Address
from typing import Generator, NamedTuple

from rich import print


class IPv4Range(NamedTuple):
    start: int
    end: int
    region: str


IP2COUNTRY_V4: list[IPv4Range] = []


def load() -> None:
    global IP2COUNTRY_V4

    data = pkgutil.get_data(
        "nalax",
        "vendor/ip2asn/ip2country-v4-u32.tsv",
    ).decode("utf-8")

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


@lru_cache(maxsize=1024)
def lookup(ips: str) -> tuple[str, str]:
    try:
        ip = ip_address(ips)
    except ValueError:
        return "None", "none"
    if isinstance(ip, IPv6Address):
        return "None", "ipv6"
    else:
        ip32 = int(ip)
        idx = bisect(IP2COUNTRY_V4, (ip32,))
        if idx >= len(IP2COUNTRY_V4):
            idx -= 1
        ipr = IP2COUNTRY_V4[idx]
        if ip32 < ipr.start:
            ipr = IP2COUNTRY_V4[idx - 1]
        if ip32 > ipr.end:
            return "Unknown"
        return ipr.region, "ipv4"


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
        cc, net = lookup(ips)
        print(f"{ips} => {cc} {net}")
