# Copyright Amethyst Reese
# Licensed under the MIT license

import logging
import sys
from pathlib import Path
from time import time_ns

import arrow
import click
from rich import print

from . import db, iplookup
from .__version__ import __version__
from .tail import tail
from .types import Event, Options

LOG = logging.getLogger(__name__)


@click.group()
@click.pass_context
@click.version_option(__version__, "--version", "-V")
@click.option("--verbose / --quiet", "-v / -q", default=None)
@click.option(
    "--database",
    "-d",
    type=click.Path(dir_okay=False, writable=True, resolve_path=True, path_type=Path),
    default=Path("nalax.db"),
)
def main(ctx: click.Context, database: Path, verbose: bool | None) -> None:
    options = Options(
        database=database,
    )
    level = (
        logging.DEBUG
        if verbose
        else (logging.WARNING if verbose is None else logging.ERROR)
    )
    logging.basicConfig(level=level, stream=sys.stderr)
    db.update_schema(options.database)
    iplookup.load()
    ctx.obj = options


@main.command("tail")
@click.pass_context
@click.option(
    "--buffer-size",
    "-b",
    type=int,
    default=0,
    help="number of events to gather before flushing batch",
)
@click.option(
    "--buffer-time",
    "-t",
    type=int,
    default=0,
    help="nanoseconds to wait before flushing batch",
)
@click.argument(
    "log-path",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path),
)
def tail_logs(
    ctx: click.Context, log_path: Path, buffer_size: int, buffer_time: int
) -> None:
    """
    Tail access logs and add to database
    """
    options: Options = ctx.obj

    batch: list[Event] = []

    def buffered() -> None:
        target = time_ns() + buffer_time
        for event in tail(log_path):
            now = time_ns()
            if now > target and not batch:
                target = now + buffer_time

            batch.append(event)

            if len(batch) >= buffer_size or now > target:
                db.insert_events(options.database, batch)
                LOG.info("recorded %d events", len(batch))
                batch.clear()
                target = now + buffer_time

    if buffer_size or buffer_time:
        return buffered()

    else:
        for event in tail(log_path):
            db.insert_events(options.database, [event])
            sys.stdout.write(".")
            sys.stdout.flush()


@main.command("aggregate")
@click.pass_context
@click.argument("before", type=str, required=False)
def aggregate(ctx: click.Context, before: str | None) -> None:
    """
    Aggregate raw events into daily/weekly/monthly stats
    """
    options: Options = ctx.obj

    if before is None:
        before = arrow.utcnow()
    else:
        try:
            before = arrow.utcnow().dehumanize(before)
        except ValueError:
            before = arrow.get(before).to("utc")

    print(f"Aggregating events before {before} ...")
    event_count = db.aggregate_daily_events(options.database, before)
    print(f"{event_count} events aggregated")


@main.command("report")
@click.pass_context
def report(ctx: click.Context) -> None:
    """
    Generate reports
    """
    options: Options = ctx.obj
    with db.connect(options.database) as conn:
        result = conn.execute(
            "select * from nalax_daily_pages order by count desc limit 20"
        )
        for row in result.fetchall():
            print(*row)

        result = conn.execute(
            "select * from nalax_daily_regions order by count desc limit 20"
        )
        for row in result.fetchall():
            print(*row)

        result = conn.execute(
            "select * from nalax_daily_devices order by count desc limit 20"
        )
        for row in result.fetchall():
            print(*row)
