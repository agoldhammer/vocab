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


def wait_to_show():
    "show definition only after pressing spacebar"
    while True:
        print("Press spacebar to show definition")
        if getch() == " ":
            return


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
    qry_count = "SELECT COUNT(*) FROM vocab"
    curs.execute(qry_count)
    count = curs.fetchone()
    return count[0]


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


def update_learned(key, forward, row, conn):
    """update proper learned field if keypress was RIGHT

    Args:
        key (Keypress): RIGHT or WRONG
        forward (bool): True if forward direction
        row (int): rowid of record to update
        conn (db connection): connection
    """
    if key == Keypress.RIGHT:
        cursor = conn.cursor()
        field = "lrd_from" if forward else "lrd_to"
        sql = f"UPDATE vocab SET {field} = 1 WHERE ROWID = {row}"
        cursor.execute(sql)
        # DEBUG
        # print(f"updated {row}")
        conn.commit()


def show_selected(n, conn, forward, unlearned):
    """show n vitems from curs
    with forward/backward option

    Args:
        n (int): no of itmes to show
        conn (connection): db connection
        forward (Bool): True if show source first
        unlearned (bool): if True, show only unlearned for given direction only
    """
    item_cursor = conn.cursor()
    # FIXME: need to implement fetch for failed only
    vitems = fetch_nitems(item_cursor, n)
    for vitem in vitems:
        key = show_vitem(vitem, forward)
        # DEBUG
        # print(f"next after row {vitem.rowid}")
        update_learned(key, forward, vitem.rowid, conn)
    count = get_count(item_cursor)
    print(f"Count: {count}")


if __name__ == "__main__":
    print("should be called from cli")
