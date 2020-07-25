# file manager for slexy
from configparser import ConfigParser
import os
import shutil
import sqlite3
from pathlib import Path

# DBDIR = "Prog/vocab/vocab"
# VOCABDIR = "Google Drive/Vocabulary"

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


def db_exists(dbname):
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
