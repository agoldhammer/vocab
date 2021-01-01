# from collections import namedtuple

# from dataclasses import dataclass, field
# from enum import Enum

# from typing import List

# from getch import getch


# class Keypress(Enum):
#     RIGHT = 0
#     WRONG = 1
#     OTHER = 2


# Vitem = namedtuple(
#     "Vitem", ["rowid", "src", "target", "supp", "lrd_from", "lrd_to", "nseen"]
# )


# def wait_to_show():
#     "show definition only after pressing spacebar"
#     while True:
#         print("Press spacebar to show definition")
#         if getch() == " ":
#             return


# def correctp():
#     """keypress filer: allow only r or w

#     Returns:
#         Keypress enum: returns Keypress.RIGHT, WRONG, or OTHER
#     """
#     while True:
#         c = getch()
#         if c == "r":
#             return Keypress.RIGHT
#         elif c == "w":
#             return Keypress.WRONG
#         print("Must press r or w")


def get_count(conn):
    """count items in the db

    Args:
        conn (Connection): sql connection

    Returns:
        int: number of items in db
    """
    qry_count = "SELECT COUNT(*) FROM vocab"
    #  qry_from = " where lrd_from = 1"
    #  qry_to = " where lrd_to = 1"
    curs = conn.cursor()
    curs.execute(qry_count)
    total = curs.fetchone()[0]
    # curs.execute(qry_count + qry_from)
    # nfrom = curs.fetchone()[0]
    # curs.execute(qry_count + qry_to)
    # nto = curs.fetchone()[0]
    return total  # , nfrom, nto


def fetch_nitems(curs, n, forward, unlearned, web=False):
    """fetch n (or fewer) items from the db

    Args:
        curs (db cursort): sql cursor
        n (int): number of items to fetch
        forward (bool): true if forward direction
        unlearned (bool): unlearned only
        web (bool): if true, return raw items
         for Web server to convert to json

    Returns:
        list[Vitems]: list of Vitem namedtuples, incl rowid
    """
    selector = "lrd_from" if forward else "lrd_to"
    if unlearned:
        where_clause = f"WHERE {selector} = 0"
    else:
        where_clause = ""
    qry_nitems = f"""
               SELECT rowid, * FROM vocab {where_clause}
               ORDER BY RANDOM() LIMIT {n}"""
    curs.execute(qry_nitems)
    if web:
        return [item for item in curs]
    # else:
    #     return map(Vitem._make, curs)


def update_nseen(row, conn):
    """update nseen field for currently displayed item

    Args:
        row (int): rowid to update
        conn (sql.Conn): connection
    """
    qry = f"UPDATE vocab SET nseen = nseen + 1 WHERE ROWID={row}"
    cursor = conn.cursor()
    cursor.execute(qry)
    conn.commit()


# def show_vitem(vitem, forward, conn):
#     """display vitem

#     Args:
#         vitem (Vitem): named tuple
#         forward (Bool): if True, display source first; else display target
#         conn (sqlite.Conn): connection

#     Returns:
#         Keypress.Enum: see correctp return values
#     """
#     src = vitem.src
#     target = vitem.target
#     update_nseen(vitem.rowid, conn)
#     if forward:
#         print(src)
#     else:
#         print(target)
#     wait_to_show()
#     if forward:
#         print(f"{target}\n")
#     else:
#         print(f"{src}\n")
#     if vitem.supp != "":
#         print(vitem.supp)
#     print("Press r if right, w if wrong")
#     # FIXME
#     return correctp()


# def update_row(forward, row, conn):
#     """update row in database

#     Args:
#         forward (bool): True if forward direction
#         row (int): rowid of record to update
#         conn (sqlite.Conn): connection
#     """
#     field = "lrd_from" if forward else "lrd_to"
#     cursor = conn.cursor()
#     sql = f"UPDATE vocab SET {field} = 1 WHERE ROWID = {row}"
#     cursor.execute(sql)
#     # DEBUG
#     # print(f"updated {row}")
#     conn.commit()


# def update_learned(key, forward, row, conn):
#     """update proper learned field if keypress was RIGHT

#     Args:
#         key (Keypress): RIGHT or WRONG
#         forward (bool): True if forward direction
#         row (int): rowid of record to update
#         conn (db connection): connection
#     """
#     if key == Keypress.RIGHT:
#         update_row(forward, row, conn)


# def gather_selected(n, conn, forward, unlearned):
#     """make generator with selected items

#     Args:
#         n (int): num of items
#         conn (sqlite.Conn): connection
#         forward (bool): True if fwd direction
#         unlearned (bool): show unlearned only
#     """
#     item_cursor = conn.cursor()
#     # FIXME: need to implement fetch for failed only
#     vitems = fetch_nitems(item_cursor, n, forward, unlearned)
#     for vitem in vitems:
#         yield vitem


# def show_selected(n, conn, forward, unlearned):
#     """show n vitems from curs
#     with forward/backward option

#     Args:
#         n (int): no of itmes to show
#         conn (connection): db connection
#         forward (Bool): True if show source first
#         unlearned (bool): if True, show only unlearned for given direction only
#     """
#     item_cursor = conn.cursor()
#     # FIXME: need to implement fetch for failed only
#     vitems = fetch_nitems(item_cursor, n, forward, unlearned)
#     for vitem in vitems:
#         key = show_vitem(vitem, forward, conn)
#         # DEBUG
#         # print(f"next after row {vitem.rowid}")
#         update_learned(key, forward, vitem.rowid, conn)
#     count = get_count(conn)
#     print(f"Count (total, learned_from, learned_to): {count}")


if __name__ == "__main__":
    print("should be called from cli")
