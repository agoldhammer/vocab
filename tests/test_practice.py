from vocab import practice
from unittest.mock import Mock


def test_correctp():
    practice.getch = Mock()
    practice.getch.return_value = 'r'
    assert(practice.Keypress.RIGHT == practice.correctp())
    practice.getch.return_value = 'w'
    assert(practice.Keypress.WRONG == practice.correctp())


def test_tomodify():
    tm = practice.ToModify()
    tm.append(2)
    assert(tm.rows_modified == [2])
