import os
import sqlite3
import sys
from pathlib import Path

import click

from vocab.practice import show_selected


def db_connect(dbname):
    dbname = dbname + ".db"
    # FIXME
    dbfile = Path.home() / Path("Prog/vocab/vocab") / Path(dbname)
    if not os.path.exists(dbfile):
        print(f"Error: database {dbfile} not found")
        sys.exit(1)
    conn = sqlite3.connect(dbfile)
    return conn, conn.cursor()


@click.group()
def main():
    pass


@main.command()
@click.option("-n", default=10, help="number of samples")
@click.option("--failed/--all", default=True, help="show previously failed only")
@click.option(
    "--forward/--backward",
    default=True,
    help="forward: show source, badkward:show target",
)
@click.argument("dbname")
def practice(n, failed, forward, dbname):
    conn, curs = db_connect(dbname)
    show_selected(n, curs, forward)
    conn.close()


@main.command()
def addvocab():
    click.echo("called addvocab")
