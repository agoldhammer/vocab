import sqlite3
import click
from collections import namedtuple

qry_all = """
SELECT * FROM vocab
ORDER BY RANDOM()
"""


def db_connect():
    conn = sqlite3.connect('german.db')
    return conn, conn.cursor()


def get_all(curs):
    curs.execute(qry_all)


if __name__ == "__main__":
    Vitem = namedtuple('Vitem', ['src', 'target', 'supp', 'fwd', 'bkwd'])
    conn, curs = db_connect()
    get_all(curs)
    for vitem in curs:
        print(Vitem._make(vitem))
    conn.close()
