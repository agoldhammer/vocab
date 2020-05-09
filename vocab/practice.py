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


def show_vitem(vitem, forward):
    src = vitem.src
    target = vitem.target
    if forward:
        print(Fore.RED + f'{src}')
    else:
        print(Fore.MAGENTA + f'{target}')
    wait_to_show()
    if forward:
        print(Fore.BLUE + f'{target}\n')
    else:
        print(Fore.RED + f'{src}\n')
    if vitem.supp != '':
        print(Fore.CYAN + vitem.supp)
    print(Fore.GREEN + 'Press c if correct')
    # FIXME
    return correctp()


def show_selected(n, curs, forward):
    qry_all = f"""
               SELECT * FROM vocab
               ORDER BY RANDOM() LIMIT {n}"""
    vitems = get_qry(curs, qry_all)
    for vitem in vitems:
        _ = show_vitem(vitem, forward)
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
    show_selected(n, curs, forward)
    conn.close()


if __name__ == "__main__":
    practice()
