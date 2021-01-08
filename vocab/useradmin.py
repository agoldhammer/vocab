from vocab.fileman import get_session

from vocab.models import User


def add_user(dbname: str, name: str, pw: str, hash=0):
    user = User(uname=name, pw=pw, hash=hash)
    sess = get_session(dbname)
    sess.add(user)
    sess.commit()
