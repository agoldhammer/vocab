from collections import namedtuple
from dataclasses import dataclass, field
from enum import Enum
from typing import List

from getch import getch


class Keypress(Enum):
    RIGHT = 0
    WRONG = 1
    OTHER = 2

# FIXME: this won't be needed if cursor modified after each item
@dataclass
class ToModify:
    rows_modified: List[int] = field(default_factory=list)

    def append(self, nrow: int):
        self.rows_modified.append(nrow)


Vitem = namedtuple("Vitem", ["rowid", "src", "target", "supp", "fwd", "bkwd"])


qry_count = """
SELECT COUNT(*) FROM vocab
"""


def wait_to_show():
    # print('Press key to show definition')
    getch()


def correctp():
    """keypress filer: allow only r or w

    Returns:
        Keypress enum: returns Keypress.RIGHT, WRONG, or OTHER
    """
    while True:
        c = getch()
        if c == "r":
            return Keypress.RIGHT
        elif c == "w":
            return Keypress.WRONG
        print("Must press r or w")


def get_count(curs):
    """count items in the db

    Args:
        curs (dbcursor): sql cursor

    Returns:
        int: number of items in db
    """
    curs.execute(qry_count)
    return next(curs)[0]


def fetch_nitems(curs, n):
    """fetch n items from the db

    Args:
        curs (db cursort): sql cursor
        n (int): number of items to fetch

    Returns:
        list[Vitems]: list of Vitem namedtuples, incl rowid
    """
    qry_nitems = f"""
               SELECT rowid, * FROM vocab
               ORDER BY RANDOM() LIMIT {n}"""
    curs.execute(qry_nitems)
    return map(Vitem._make, curs)


def show_vitem(vitem, forward):
    """display vitem

    Args:
        vitem (Vitem): named tuple
        forward (Bool): if True, display source first; else display target

    Returns:
        Keypress.Enum: see correctp return values
    """
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
    """show n vitems from curs
    with forward/backward option

    Args:
        n (int): no of itmes to show
        curs (cursor): db cursor
        forward (Bool): True if show source first
    """
    vitems = fetch_nitems(curs, n)
    for vitem in vitems:
        key = show_vitem(vitem, forward)
        if key == Keypress.OTHER:
            show_vitem(vitem, forward)
        else:
            # FIXME
            print(f"next after row {vitem.rowid}")
    count = get_count(curs)
    print(f"Count: {count}")


if __name__ == "__main__":
    print("should be called from cli")
