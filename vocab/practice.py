import sqlite3
import click
from collections import namedtuple

Vitem = namedtuple('Vitem', ['src', 'target', 'supp', 'fwd', 'bkwd'])

qry_all = """
SELECT * FROM vocab
ORDER BY RANDOM()
"""


def db_connect():
    conn = sqlite3.connect('german.db')
    return conn, conn.cursor()


def get_qry(curs, qry):
    curs.execute(qry)
    return map(Vitem._make, curs)


def show_forward(curs):
    vitems = get_qry(curs, qry_all)
    for vitem in vitems:
        print(f'{vitem.src}: {vitem.target}')


@click.command()
@click.option('--failed/--all', default=True,
              help='show previously failed only')
@click.option('--forward/--backward', default=True,
              help='forward: show source, badkward:show target')
def practice(failed, forward):
    conn, curs = db_connect()
    show_forward(curs)
    conn.close()


if __name__ == "__main__":
    practice()
