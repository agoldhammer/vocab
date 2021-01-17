import click

from vocab.vocabu import add_vocab
from vocab.models import create_sqldb
from vocab.useradmin import add_user


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
        add_vocab(store, fname, dbname)
    except Exception as e:
        print(e)


@main.command()
@click.argument("sqdbname")
def createsqldb(sqdbname):
    create_sqldb(sqdbname)


@main.command()
@click.argument("dbname")
@click.argument("username")
@click.argument("password")
def new_user(dbname, username, password):
    add_user(dbname, username, password)
