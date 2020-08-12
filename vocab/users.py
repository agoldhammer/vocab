
from sqlite3 import Row

from werkzeug.security import check_password_hash

from vocab.fileman import db_connect


class UsersDB():
    def __init__(self, udbname):
        self.conn = db_connect(udbname)
        self.conn.row_factory = Row

    def username_to_record(self, username):
        cursor = self.conn.cursor()
        res = cursor.execute(
            f"SELECT rowid, * FROM users WHERE username = '{username}'"
        )
        return res.fetchone()

    def id_to_record(self, uid: str):
        uid = int(uid)
        cursor = self.conn.cursor()
        res = cursor.execute(
            f"SELECT rowid, * FROM users WHERE rowid = {uid}"
        )
        return res.fetchone()


class User():

    def __init__(self, username):
        self.username = username
        self.db = UsersDB("users")
        self.user = self.db.username_to_record(username)

    def is_authenticated(self, password):
        if self.user is None:
            return False
        return check_password_hash(self.user['pwhash'], password)

    def is_active(self, username):
        return True

    def is_anonymous(self, username):
        return False

    def get_id(self):
        if self.user is not None:
            return self.user['rowid']
        else:
            return None


# # for debugging
# usersdb = UsersDB("users")
# u = User("test", usersdb)

# # print(f"auth? {u.is_authenticated('dummy')}")
# # print(f"auth? {u.is_authenticated('goldie')}")

# print(u.user["username"])
