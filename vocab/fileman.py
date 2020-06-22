# file manager for slexy

import os
import shutil
import sqlite3
from pathlib import Path

DBDIR = "Prog/vocab/vocab"
VOCABDIR = "Google Drive/Vocabulary"


class FilemanError(Exception):
    pass


def make_fqname(fname, fpath, new=False):
    "return fully qualified filename from basename and fpath"
    if fpath == DBDIR:
        ext = ".db"
    elif fpath == VOCABDIR:
        ext = ".docx"
    else:
        raise FilemanError(f"Error: bad path {fpath}")

    fname = fname + ext
    fqname = Path.home() / Path(fpath) / Path(fname)
    file_exists = os.path.exists(fqname)
    if not new and not file_exists:
        raise FileNotFoundError(f"{fqname}")
    elif new and file_exists:
        raise FileExistsError(f"Would clobber {fqname}")
    return fqname


def db_exists(dbname):
    """check if db exists

    Args:
        dbname (str): base name of db w/o ext
    """
    fqdbname = make_fqname(dbname, DBDIR)
    return os.path.exists(fqdbname)


def db_connect(dbname, new=False):
    """
    connect to dbname.db if it exists
    and return connection
    """
    fqdbname = make_fqname(dbname, DBDIR, new)
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


def get_fqdocname(docname):
    """
    return fully qualified doc file name
    """
    return make_fqname(docname, VOCABDIR)
