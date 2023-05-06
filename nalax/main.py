# Copyright Amethyst Reese
# Licensed under the MIT license

from pathlib import Path

import arrow
import click
from rich import print

from . import db, iplookup
from .tail import tail
from .types import Event, Options


@click.group()
@click.pass_context
@click.option(
    "--database",
    "-d",
    type=click.Path(dir_okay=False, writable=True, resolve_path=True, path_type=Path),
    default=Path("nalax.db"),
)
def main(ctx: click.Context, database: Path) -> None:
    options = Options(
        database=database,
    )
    db.update_schema(options.database)
    iplookup.load()
    ctx.obj = options


@main.command("tail")
@click.pass_context
@click.option("--batch-size", "-b", type=int, default=1)
@click.argument(
    "log-path",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path),
)
def tail_logs(ctx: click.Context, log_path: Path, batch_size: int) -> None:
    """
    Tail access logs and add to database
    """
    options: Options = ctx.obj

    batch: list[Event] = []
    for event in tail(log_path):
        print(event)
        batch.append(event)

        if len(batch) >= batch_size:
            print("inserting to db")
            db.insert_events(options.database, batch)


@main.command("aggregate")
@click.pass_context
def aggregate(ctx: click.Context) -> None:
    """
    Aggregate raw events into daily/weekly/monthly stats
    """
    options: Options = ctx.obj

    db.aggregate_daily_events(options.database, arrow.utcnow().int_timestamp)


@main.command("report")
@click.pass_context
def report(ctx: click.Context) -> None:
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
