from pathlib import Path

from vocab import fileman as fm


def test_makefqname():
    fqn = fm.make_fqname("dummy", fm.DBDIR, True)
    desired = Path.home() / Path(fm.DBDIR) / Path("dummy.db")
    assert(fqn == desired)
