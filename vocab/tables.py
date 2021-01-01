# tables for vocab server
from sqlalchemy import Table, Column, Integer, String, MetaData

meta_lexicon = MetaData()

lexicon = Table('lexicon', meta_lexicon,
    Column('id', Integer, primary_key=True),
    Column('src', String),
    Column('target', String),
    Column('supp', String))