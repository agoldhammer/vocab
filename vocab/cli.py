import click
import sqlite3
from vocab.practice import show_selected


def db_connect(dbname):
    conn = sqlite3.connect(dbname)
    return conn, conn.cursor()


@click.group()
def main():
    pass


@main.command()
@click.option('-n', default=10, help='number of samples')
@click.option('--failed/--all', default=True,
              help='show previously failed only')
@click.option('--forward/--backward',
              default=True, help='forward: show source, badkward:show target')
@click.argument('dbname')
def practice(n, failed, forward, dbname):
    conn, curs = db_connect(dbname + '.db')
    show_selected(n, curs, forward)
    conn.close()
