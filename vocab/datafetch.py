import sys
from typing import Optional, Tuple

from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import func

from vocab.fileman import get_session
from vocab.models import Slug, User


def fetch_slugs(sess: Session, num_to_fetch: int = 25) -> Tuple[int, str, str, str]:
    """[fetch the vocab items from lexicon]

    Args:
        sess (Session): ORM session
        num_to_fetch (int, optional): number of vocab items to fetch. Defaults to 25.

    Return:
        Tuple[wid: int, src: str, target: str, supp: str]
    """
    # See: https://stackoverflow.com/questions/60805/getting-random-row-through-sqlalchemy
    # select.order_by(func.rand()) for MySQL
    slugs = sess.query(Slug).order_by(func.random()).limit(num_to_fetch)
    return [[slug.wid, slug.src, slug.target, slug.supp] for slug in slugs]  # type: ignore


def count_vocab(sess: Session) -> int:
    """return number of vocab items in lexicon of dbname

    Args:
        sess (Session): ORM session

    Returns:
        int: number of vocab items in db
    """
    return sess.query(Slug).count()


def fetch_user_by_id(sess: Session, uid: int) -> Optional[User]:
    """fetch user by uid

    Args:
        sess (Session): sqlalchemy session
        uid (int): user id

    Returns:
        Optional[User]: the user corresponding to the uid
    """
    user = sess.query(User).filter(User.uid == uid).one_or_none()
    return user


def fetch_user_by_name(sess: Session, name: str) -> Optional[User]:
    """fetch user by user name

    Args:
        sess (Session): sqlalchemy session
        name (str): username

    Returns:
        Optional[User]: a User object
    """
    user = sess.query(User).filter(User.uname == name).one_or_none()
    return user


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Must specify name of an sqa formatted db")
        sys.exit(1)
    sqadbname = sys.argv[1]
    sess = get_session(sqadbname)
    rows = fetch_slugs(sess, 5)
    for row in rows:
        print(row)
    nrows = count_vocab(sess)
    print(f"nrows: {nrows}")
    user1 = fetch_user_by_id(sess, 1)
    print(f"User1 {user1}")
    user2 = fetch_user_by_name(sess, "agold")
    print(f"User2 {user2}")
