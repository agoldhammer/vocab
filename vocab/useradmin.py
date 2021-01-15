from vocab.fileman import get_session
from vocab.models import Score, User


class QueryError(Exception):
    pass


def add_user(dbname: str, name: str, pw: str):
    user = User(uname=name, hash=0)
    # create hash from password and save in user
    user.set_password(pw)
    sess = get_session(dbname)
    sess.add(user)
    sess.commit()


def get_user_id(sess, uid: int) -> User:
    user = sess.query(User).get(uid)
    return user


# this should be used inside a session
def append_new_score(sess, uid: int, wid: int):
    user = get_user_id(sess, uid)
    score = Score(uid=uid, wid=wid, lrndsrc=0, lrndtgt=0, nseen=1)
    user.scores.append(score)
    sess.add(user)


# on query with joins, see
#  https://stackoverflow.com/questions/45290283/querying-with-joins-in-sql-alchemy-and-avoiding-select-all
def get_score_by_uid_wid(sess, uid: int, wid: int) -> Score:
    scores = sess.query(User, Score).filter(User.uid == uid).\
        filter(Score.uid == uid).\
        filter(Score.wid == wid).all()
    if len(scores) == 1:
        return scores[0]
    elif len(scores) == 0:
        return None
    else:
        raise QueryError(f"Error querying score uid {uid}, wid {wid}")


if __name__ == "__main__":
    sess = get_session("redux")
    for uid in range(1, 4):
        user = get_user_id(sess, uid)
        if user is not None:
            print(user)
        else:
            print(f"No such user id={uid}")
    append_new_score(sess, uid=1, wid=1)
    s = get_score_by_uid_wid(sess, 1, 1)
    # print(u)
    print(s)
    s = get_score_by_uid_wid(sess, 2, 1)
    print(s)
    # score = get_score_by_uid_wid(sess, 1, 1)
    # print(f"score word 1: {score}")
    # score = get_score_by_uid_wid(sess, 2, 1)
    # print(f"should be None: {score}")
    # print(user)
    # sess.commit()
    # users = sess.query(User)
    # for user in users:
    #     for score in user.scores:
    #         print(score)
