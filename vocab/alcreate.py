from sqlalchemy import (create_engine,
    Table, Column, Integer, String, MetaData)
from vocab.fileman import make_fqname, DBDIR

fqdbname = make_fqname("alctest", DBDIR)
print(fqdbname)
print(f"sqlite:///{fqdbname}")

engine = create_engine(f"sqlite:///{fqdbname}", echo = True)

meta = MetaData()

vocab = Table('vocab', meta,
    Column('id', Integer, primary_key=True),
    Column('src', String),
    Column('target', String),
    Column('supp', String))

meta.create_all(engine)


