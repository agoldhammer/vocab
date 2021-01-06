import click

from vocab.createdb2 import create_db
# from vocab.practice import show_selected
from vocab.vocabu import execute, add_vocab
# from vocab.fileman import db_connect, backup_db
# from vocab.lexgui import gui_conn, ExitException
from vocab.models import create_sqldb

# NOTE: createdb2 has replaced createdb, which will be removed later


@click.group()
def main():
    pass


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
@click.option("--store/--nostore", default=False,
              help="store/nostore in detabase, creating if necessary")
@click.argument("fname")
@click.argument("dbname")
def process(store, fname, dbname):
    try:
        add_vocab(store, fname, dbname)
    except Exception as e:
        print(e)


@main.command()
@click.argument("dbname")
def createdb(dbname):
    create_db(dbname)


@main.command()
@click.argument("sqdbname")
def createsqldb(sqdbname):
    create_sqldb(sqdbname)
