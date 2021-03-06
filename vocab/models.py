from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from vocab.fileman import get_vocab_engine

if TYPE_CHECKING:
    Base = object
else:
    Base = declarative_base()


class Slug(Base):  # type: ignore
    __tablename__ = "lexicon"

    wid = Column(Integer, primary_key=True)
    src = Column(String)
    target = Column(String)
    supp = Column(String)

    def __repr__(self) -> str:
        return (
            f"<Slug(id={id}, src={self.src}, target={self.target}, supp={self.supp})>"
        )


class User(Base):  # type: ignore
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True)
    uname = Column(String)
    hash = Column(Integer)
    # scores = relationship(
    #     "Score", back_populates="users", cascade="all, delete, delete-orphan"
    # )

    # functions for use by flask_login

    def is_authenticated(self, password):
        print(f"checking password {password}")
        print(f"hash: {self.hash}")
        return check_password_hash(self.hash, password)

    def is_active(self, username):
        return True

    def is_anonymous(self, username):
        return False

    def get_id(self):
        return str(self.uid)

    def set_password(self, password):
        self.hash = generate_password_hash(password)

    def __repr__(self) -> str:
        return f"<User(uid={self.uid}, uname={self.uname}, hash={self.hash})>"


class Score(Base):
    __tablename__ = "scores"

    sid = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey("users.uid"))
    wid = Column(Integer, ForeignKey("lexicon.wid"))
    lrndsrc = Column(Integer)
    lrndtgt = Column(Integer)
    nseen = Column(Integer)
    # users = relationship("User", back_populates="scores")

    def __repr__(self) -> str:
        return f"<Score(sid={self.sid}, uid={self.uid}, wid={self.wid},\
             lrndsrc={self.lrndsrc}, lrndtgt={self.lrndtgt}, nseen={self.nseen})>"


def create_sqldb(dbname: str):
    """Create a sqlalchemy database embodying the above models

    Args:
        dbname (str): base name of db; will use dir specified by config file
    """
    engine = get_vocab_engine(dbname)
    Base.metadata.create_all(engine)  # type: ignore
