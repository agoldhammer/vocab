
from werkzeug.security import check_password_hash
from vocab.fileman import db_connect


class User():
    def __init__(self, udbname):
        self.conn = db_connect(udbname)

    def is_authenticated(self, username, password):
        cursor = self.conn.cursor()
        res = cursor.execute(
            f"SELECT rowid, * FROM users WHERE username = '{username}'"
        )
        print(f"res: {res}")
        hash = res.fetchone()[2]
        print(f"hash: {hash}")
        return check_password_hash(hash, password)

    def is_active(self, username):
        return True

    def is_anonymous(self, username):
        return False

    def get_id(self, username):
        pass


# for debugging
# u = User("users")
# print(f"user obj: {u}")
# res = u.is_authenticated("test", "dummy")
# print(f"dummy {res}")
# res = u.is_authenticated("test", "goldie")
# print(f"goldie {res}")
