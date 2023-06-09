# Copyright Amethyst Reese
# Licensed under the MIT license

import json
import logging
import shlex
import subprocess
from pathlib import Path
from typing import Generator
from urllib.parse import urlparse

import arrow
from rich import print

from . import iplookup
from .agent import user_agent
from .types import Event

LOG = logging.getLogger(__name__)


def convert(data: dict[str, str]) -> Event | None:
    try:
        timestamp = arrow.get(data["time"]).to("utc")
        uri = urlparse(data["uri"])
        region, network = iplookup.lookup(data["remote"])
        agent = user_agent(data["agent"])

        event = Event(
            timestamp=timestamp,
            host=data["host"],
            path=uri.path,
            method=data["method"],
            status=int(data["status"]),
            region=region,
            network=network,
            agent=agent,
        )
        return event

    except Exception as exc:
        LOG.warning("unrecognized data contents: %s", type(exc))
        return None


def tail(path: Path) -> Generator[Event, bool | None, None]:
    cmd = ("tail", "-Fn0", path.as_posix())
    print(f"$ {shlex.join(cmd)}")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, encoding="utf-8")
    try:
        for line in proc.stdout:
            try:
                data = json.loads(line)
            except ValueError:
                LOG.warning("failed to parse line, check logging format")

            event = convert(data)
            if event is None:
                continue

            stop = yield event
            if stop:
                break

    finally:
        if not proc.poll():
            proc.kill()
            proc.wait(2)


if __name__ == "__main__":
    import sys

    path = Path(sys.argv[1])
    iplookup.load()
    for event in tail(path):
        print(event)
        print(iplookup.lookup(event.remote))
