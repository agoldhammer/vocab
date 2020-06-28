import pytest

from vocab.createdb import create_db
from vocab.fileman import db_connect, rm_db


@pytest.fixture()
def create():
    tst_dbname = "testcreate"
    create_db(tst_dbname)
    yield
    rm_db(tst_dbname)


def test_create(create):
    conn = db_connect("testcreate")
    assert(conn is not None)
