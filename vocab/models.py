from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Slug(Base):
    __tablename__ = "lexicon"

    id = Column(Integer, primary_key=True)
    src = Column(String)
    target = Column(String)
    supp = Column(String)

    def __repr__(self) -> str:
        return f"<Slug(id={id}, src={self.src}, target={self.target}, supp={self.supp})>"


class User(Base):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True)
    uname = Column(String)
    pw = Column(String)
    hash = Column(Integer)

    def __repr__(self) -> str:
        return f"<User(uid={self.uid}, pw={self.pw}, hash={self.hash})>"
