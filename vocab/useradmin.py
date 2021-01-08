from vocab.fileman import get_session

from vocab.models import User, Score


def add_user(dbname: str, name: str, pw: str, hash: int = 0):
    user = User(uname=name, pw=pw, hash=hash)
    sess = get_session(dbname)
    sess.add(user)
    sess.commit()


# this should be used inside a session
def append_new_score(user: User, wid: int):
    uid = user.uid
    score = Score(uid=uid, wid=wid, lrndsrc=0, lrndtgt=0, nseen=1)
    user.scores.append(score)


if __name__ == "__main__":
    sess = get_session("redux")
    users = sess.query(User)
    for user in users:
        print(user)
    user = users.filter(User.uid == 1).one()
    append_new_score(user=user, wid=1)
    print(user)
    sess.commit()
    users = sess.query(User)
    for user in users:
        for score in user.scores:
            print(score)
