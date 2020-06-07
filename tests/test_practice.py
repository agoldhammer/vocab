from vocab import practice
from unittest.mock import Mock


def test_correctp():
    practice.getch = Mock()
    practice.getch.return_value = 'r'
    assert(practice.Keypress.RIGHT == practice.correctp())
    practice.getch.return_value = 'w'
    assert(practice.Keypress.WRONG == practice.correctp())
    practice.getch.return_value = 'j'
    assert(practice.Keypress.OTHER == practice.correctp())
