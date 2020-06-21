import click

from vocab.practice import show_selected
from vocab.vocab import execute
from vocab.fileman import db_connect


@click.group()
def main():
    pass


@main.command()
@click.option("-n", default=10, help="number of samples")
@click.option("--failed/--all", default=True, help="show previously failed only")
@click.option(
    "--forward/--backward",
    default=True,
    help="forward: show source first, backward: show target first",
)
@click.argument("dbname")
def practice(n, failed, forward, dbname):
    conn = None
    try:
        conn = db_connect(dbname)
        show_selected(n, conn, forward)
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.commit()
            conn.close()


@main.command()
@click.option("--store/--nostore", default=False, help="store/nostore in detabase")
@click.argument("fname")
@click.argument("dbname")
def addvocab(store, fname, dbname):
    try:
        execute(store, fname, dbname)
    except Exception as e:
        print(e)
