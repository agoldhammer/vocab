import sys

from sqlalchemy import create_engine

from vocab.fileman import db_connect, db_exists, make_fqname, DBDIR
from vocab.tables import lexicon

"""
Module to migrate from original design dbs to sqlalchemy design
"""


def migrate(masterdb_name, old_db_name):
    """perform the migration from olddb to masterdb

    Args:
        masterdb (str): name of masterdb file
        oldb (str): name of olddb file
    """
    old_db_fqname, exists = db_exists(old_db_name)
    if exists:
        print(f"dbs: {masterdb_name}, {old_db_fqname}")
    else:
        print(f"{old_db_name} not found")
        sys.exit(1)
    fqmasterdbname = make_fqname(masterdb_name, DBDIR)
    conn = db_connect(old_db_name)
    curs = conn.cursor()
    curs.execute(
        f"""
       SELECT * FROM vocab;
        """
    )
    keys = ("src", "target", "supp")
    vocab_items = [dict(zip(keys, item)) for item in curs]
    curs.close()

    engine = create_engine(f"sqlite:///{fqmasterdbname}", echo = True)
    conn = engine.connect()
    conn.execute(lexicon.insert(), vocab_items)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Must specify masterdb and olddb")
        sys.exit(1)
    else:
        masterdb_name = sys.argv[1]
        old_db_name = sys.argv[2]
        migrate(masterdb_name, old_db_name)
