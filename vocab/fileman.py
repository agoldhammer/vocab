# file manager for slexy
import os
import shutil
import sqlite3
from configparser import ConfigParser
from pathlib import Path
from typing import Tuple

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

# this is a singleton, created and accessed through get_vocab_engine
_vocab_engine = None


config = ConfigParser()
config.read(Path.home() / ".vocab/vocab.ini")
dirs = config["Dirs"]
DBDIR = dirs["dbdir"]
VOCABDIR = dirs["vocabdir"]


class FilemanError(Exception):
    pass


def make_fqname(fname, fpath):
    "return fully qualified filename from basename and fpath"
    if fpath == DBDIR:
        ext = ".db"
    elif fpath == VOCABDIR:
        ext = ".docx"
    else:
        raise FilemanError(f"Error: bad path {fpath}")

    fname = fname + ext
    fqname = Path.home() / Path(fpath) / Path(fname)

    return fqname


def db_exists(dbname: str) -> Tuple[str, bool]:
    fqdbname = make_fqname(dbname, DBDIR)
    return fqdbname, os.path.exists(fqdbname)


def db_connect(dbname, create=False):
    """
    connect to dbname.db if it exists
    and return connection
    """
    fqdbname, file_exists = db_exists(dbname)
    if not create and not file_exists:
        raise FileNotFoundError(f"{fqdbname}")
    elif create and file_exists:
        raise FileExistsError(f"Would clobber {fqdbname}")
    conn = sqlite3.connect(fqdbname)
    return conn


def backup_db(dbname):
    """backup the database

    Args:
        dbname (str): base name of database to backup
    """
    fqdbname = make_fqname(dbname, DBDIR)
    dbbackup_fname = Path(fqdbname)
    shutil.copy(fqdbname, str(dbbackup_fname) + ".bak")


def rm_db(dbname):
    """remove a database file (used in testing)

    Args:
        dbname (str): base dbname
    """
    fqdbname = make_fqname(dbname, DBDIR)
    os.remove(fqdbname)


def get_fqdocname(docname):
    """
    return fully qualified doc file name
    """
    return make_fqname(docname, VOCABDIR)


def get_all_dbs(lang):
    """list all dbs for specified language

    Args:
        lang (string): 'german' or 'italian'
    """
    pattern = Path.home() / Path(DBDIR)
    paths = pattern.glob(f"{lang}*.db")
    return [path.stem for path in paths]


def get_vocab_engine(dbname: str):
    """return (creating if necessary) engine for vocab db

    Args:
        dbname (str): base name of vocab db

    Returns:
        sqlalchemy.Engine: the engine
    """
    global _vocab_engine
    if _vocab_engine is None:
        fqmasterdbname = make_fqname(dbname, DBDIR)
        url = f"sqlite:///{fqmasterdbname}"
        print(f"conn to url: {url}")
        _vocab_engine = create_engine(url)
    return _vocab_engine


def get_session(dbname: str) -> Session:
    """get a session from the current engine

    Args:
        dbname (str): name of sqlalchemy db

    Returns:
        Session: ORM session object
    """
    engine = get_vocab_engine(dbname)
    Session = sessionmaker(bind=engine)
    return Session()
