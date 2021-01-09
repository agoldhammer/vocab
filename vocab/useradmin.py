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


def get_user_id(sess, uid: int) -> User:
    user = sess.query(User).filter(User.uid == uid).one_or_none()
    return user


if __name__ == "__main__":
    sess = get_session("redux")
    for uid in range(1, 4):
        user = get_user_id(sess, uid)
        if user is not None:
            print(user)
        else:
            print(f"No such user id={uid}")
    # append_new_score(user=user, wid=1)
    # print(user)
    # sess.commit()
    # users = sess.query(User)
    # for user in users:
    #     for score in user.scores:
    #         print(score)
