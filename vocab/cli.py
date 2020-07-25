import click

from vocab.createdb import create_db
from vocab.practice import show_selected
from vocab.vocabu import execute
from vocab.fileman import db_connect, backup_db
from vocab.lexgui import gui_conn, ExitException


@click.group()
def main():
    pass


@main.command()
@click.option("-n", default=10, help="number of samples")
@click.option("--unlearned/--all", default=True, help="show previously failed only")
@click.option(
    "--forward/--backward",
    default=True,
    help="forward: show source first, backward: show target first",
)
@click.option(
    "--nogui/--gui",
    default=True,
    help="--nogui/--gui: use cli/use gui"
)
@click.argument("dbname")
def practice(n, unlearned, forward, dbname, nogui):
    conn = None
    try:
        # backup the db before modifying
        backup_db(dbname)
        conn = db_connect(dbname)
        if nogui:
            show_selected(n, conn, forward, unlearned)
        else:
            gui_conn(n, conn, forward, unlearned)
    except ExitException as e:
        print(e)
    finally:
        if conn:
            conn.commit()
            conn.close()


@main.command()
@click.option("--store/--nostore", default=False,
              help="store/nostore in detabase, creating if necessary")
@click.argument("fname")
@click.argument("dbname")
def addvocab(store, fname, dbname):
    try:
        execute(store, fname, dbname)
    except Exception as e:
        print(e)


@main.command()
@click.argument("dbname")
def createdb(dbname):
    create_db(dbname)
