from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from vocab.fileman import get_vocab_engine

Base = declarative_base()


class Slug(Base):
    __tablename__ = "lexicon"

    wid = Column(Integer, primary_key=True)
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
    scores = relationship("Score", back_populates="users")

    def __repr__(self) -> str:
        return f"<User(uid={self.uid}, uname={self.uname}, pw={self.pw}, hash={self.hash})>"


class Score(Base):
    __tablename__ = "scores"

    sid = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey("users.uid"))
    wid = Column(Integer, ForeignKey("lexicon.wid"))
    lrndsrc = Column(Integer)
    lrndtgt = Column(Integer)
    nseen = Column(Integer)
    users = relationship("User", back_populates="scores")

    def __repr__(self) -> str:
        return f"<Score(sid={self.sid}, uid={self.uid}, wid={self.wid},\
             lrndsrc={self.lrndsrc}, lrndtgt={self.lrndtgt}, nseen={self.nseen})>"


def create_sqldb(dbname: str):
    """Create a sqlalchemy database embodying the above models

    Args:
        dbname (str): base name of db; will use dir specified by config file
    """
    engine = get_vocab_engine(dbname)
    Base.metadata.create_all(engine)
