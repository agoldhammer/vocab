from unittest.mock import Mock

import pytest

from vocab.fileman import db_connect
from vocab import practice

conn = None


@pytest.fixture()
def setup_db():
    global conn
    conn = db_connect("test1")
    yield
    conn.close()


def test_correctp():
    practice.getch = Mock()
    practice.getch.return_value = "r"
    assert practice.Keypress.RIGHT == practice.correctp()
    practice.getch.return_value = "w"
    assert practice.Keypress.WRONG == practice.correctp()


# def test_tomodify():
#     tm = practice.ToModify()
#     tm.append(2)
#     assert tm.rows_modified == [2]

@pytest.mark.parametrize("direction", [True, False])
def test_update(setup_db, direction):
    row = 10
    item = "lrd_from" if direction else "lrd_to"
    qry_row = f"""
    SELECT {item} FROM vocab WHERE rowid={row}
    """
    practice.update_row(forward=direction, row=10, conn=conn)
    cursor = conn.cursor()
    cursor.execute(qry_row)
    assert(cursor.fetchone() == (1,))
