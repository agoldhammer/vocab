import sys

from vocab.fileman import db_connect


def create_db(name):
    """create db for use by slexy
    fields: src text, target text, supplementary texxt,
    learned from [source], learned to [target]

    Args:
        name (str): name of db to create, w/o extension
    """
    conn = db_connect(name, create=True)
    curs = conn.cursor()
    curs.execute(
        """CREATE TABLE vocab
        (src text, target text, supp text,
        lrd_from integer, lrd_to integer,
        nseen integer)"""
    )
    conn.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Must specify db name")
        sys.exit(1)
    else:
        create_db(sys.argv[1])
