# file manager for slexy

import os
import sqlite3
from pathlib import Path

DBDIR = "Prog/vocab/vocab"
VOCABDIR = "Google Drive/Vocabulary"


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
    if not os.path.exists(fqname):
        raise FilemanError(f"Error: file {fqname} not found")
    return fqname


def db_connect(dbname):
    """
    connect to dbname.db if it exists
    and return connection
    """
    fqdbname = make_fqname(dbname, DBDIR)
    conn = sqlite3.connect(fqdbname)
    return conn


def get_fqdocname(docname):
    """
    return fully qualified doc file name
    """
    return make_fqname(docname, VOCABDIR)
