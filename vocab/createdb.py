import sqlite3
import sys


def create_db(name):
    conn = sqlite3.connect(name + '.db')
    curs = conn.cursor()
    curs.execute("""CREATE TABLE vocab
        (src text, target text, supp text,
        lrd_from integer, lrd_to integer)""")
    conn.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Must specify db name')
        sys.exit(1)
    else:
        create_db(sys.argv[1])
