import sqlite3
from collections import namedtuple
from dataclasses import dataclass, field
from enum import Enum
from typing import List

from getch import getch


class Keypress(Enum):
    RIGHT = 0
    WRONG = 1
    OTHER = 2


@dataclass
class ToModify:
    rows_modified: List[int] = field(default_factory=list)

    def append(self, nrow: int):
        self.rows_modified.append(nrow)


Vitem = namedtuple("Vitem", ["src", "target", "supp", "fwd", "bkwd"])


qry_count = """
SELECT COUNT(*) FROM vocab
"""


def wait_to_show():
    # print('Press key to show definition')
    getch()


def correctp():
    while True:
        c = getch()
        if c == "r":
            return Keypress.RIGHT
        elif c == "w":
            return Keypress.WRONG
        print("Must press r or w")


def get_count(curs):
    curs.execute(qry_count)
    return next(curs)[0]


def db_connect(dbname):
    conn = sqlite3.connect(dbname)
    return conn, conn.cursor()


def get_qry(curs, qry):
    curs.execute(qry)
    return map(Vitem._make, curs)


def show_vitem(vitem, forward):
    src = vitem.src
    target = vitem.target
    if forward:
        print(src)
    else:
        print(target)
    wait_to_show()
    if forward:
        print(f"{target}\n")
    else:
        print(f"{src}\n")
    if vitem.supp != "":
        print(vitem.supp)
    print("Press r if right, w if wrong")
    # FIXME
    return correctp()


def show_selected(n, curs, forward):
    qry_all = f"""
               SELECT * FROM vocab
               ORDER BY RANDOM() LIMIT {n}"""
    vitems = get_qry(curs, qry_all)
    for vitem in vitems:
        key = show_vitem(vitem, forward)
        if key == Keypress.OTHER:
            show_vitem(vitem, forward)
        else:
            # FIXME
            print("next")
    count = get_count(curs)
    print(f"Count: {count}")


if __name__ == "__main__":
    print("should be called from cli")
