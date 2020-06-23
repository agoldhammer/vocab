from pathlib import Path

import pytest

from vocab import fileman as fm


def test_make_fqname():
    fqn = fm.make_fqname("dummy", fm.DBDIR, True)
    desired = Path.home() / Path(fm.DBDIR) / Path("dummy.db")
    assert(fqn == desired)

    with pytest.raises(FileNotFoundError):
        fqn = fm.make_fqname("nonexistent", fm.DBDIR)

    # the test.db should exist in the program dir
    with pytest.raises(FileExistsError):
        fqn = fm.make_fqname("test", fm.DBDIR, new=True)

    # dir other than DBDIR or VOCABDIR should raise exc
    with pytest.raises(fm.FilemanError):
        fqn = fm.make_fqname("test", "randomdir")


def test_db_connect():
    # the test db should exist
    conn = fm.db_connect("test")
    assert(conn is not None)


def test_get_fqdocname():
    "will fail if testdummy.docx not in VOCABDIR"
    fqn = fm.get_fqdocname("testdummy")
    desired = Path.home() / Path(fm.VOCABDIR) / Path("testdummy.docx")
    assert(fqn == desired)
