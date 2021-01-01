import sys

from sqlalchemy import create_engine

from vocab.fileman import DBDIR, make_fqname
from vocab.tables import meta_lexicon


def create_sqadb(name):
    print(f"Creating sqlite:///{name}")
    engine = create_engine(f"sqlite:///{fqdbname}", echo=True)
    meta_lexicon.create_all(engine)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Must specify db name w/o extension: e.g., sqagerman")
        sys.exit(1)
    else:
        dbname = sys.argv[1]
        fqdbname = make_fqname(dbname, DBDIR)
        create_sqadb(fqdbname)
