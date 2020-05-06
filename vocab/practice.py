import sqlite3
import click
from getch import getch
from collections import namedtuple
from colorama import init, Fore

init()

Vitem = namedtuple('Vitem', ['src', 'target', 'supp', 'fwd', 'bkwd'])


qry_count = """
SELECT COUNT(*) FROM vocab
"""


def wait_to_show():
    # print('Press key to show definition')
    getch()


def correctp():
    c = getch()
    return True if c == 'c' else False


def get_count(curs):
    curs.execute(qry_count)
    return next(curs)[0]


def db_connect():
    # FIXME
    conn = sqlite3.connect('german.db')
    return conn, conn.cursor()


def get_qry(curs, qry):
    curs.execute(qry)
    return map(Vitem._make, curs)


def show_forward(n, curs):
    qry_all = f"""
               SELECT * FROM vocab
               ORDER BY RANDOM() LIMIT {n}"""
    vitems = get_qry(curs, qry_all)
    for vitem in vitems:
        print(Fore.RED + f'{vitem.src}')
        wait_to_show()
        print(Fore.BLUE + f'{vitem.target}\n')
        if vitem.supp != '':
            print(Fore.CYAN + vitem.supp)
        print(Fore.GREEN + 'Press c if correct')
        # FIXME
        _ = correctp()
    count = get_count(curs)
    print(f'Count: {count}')


@click.command()
@click.option('-n', default=10, help='number of samples')
@click.option('--failed/--all', default=True,
              help='show previously failed only')
@click.option('--forward/--backward', default=True,
              help='forward: show source, badkward:show target')
def practice(n, failed, forward):
    conn, curs = db_connect()
    show_forward(n, curs)
    conn.close()


if __name__ == "__main__":
    practice()
