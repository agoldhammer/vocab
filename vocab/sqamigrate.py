import sys

from vocab.fileman import db_connect, db_exists

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
    conn = db_connect(old_db_name)
    curs = conn.cursor()
    curs.execute(
        f"""
       SELECT * FROM vocab;
        """
    )
    keys = ("src", "target", "supp")
    for item in curs:
        dicts = dict(zip(keys, item))
        print(dicts)
    curs.close()
    # conn.commit()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Must specify masterdb and olddb")
        sys.exit(1)
    else:
        masterdb_name = sys.argv[1]
        old_db_name = sys.argv[2]
        migrate(masterdb_name, old_db_name)
