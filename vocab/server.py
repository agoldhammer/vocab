from flask import (Flask, session, request)
import flask_login as fli
from flask_sqlalchemy import SQLAlchemy

from vocab.fileman import db_connect
from vocab.users import User, UsersDB
from vocab.datafetch import fetch_slugs, count_vocab


class ServerException(Exception):
    pass


site_path = "/Users/agold/Prog/lexy/public"
app = Flask(__name__,
            static_folder=site_path,
            template_folder=site_path)
app.secret_key = b'96\x91Q\xf1N\x86\x1b\xc3&1\x92\x9f\tU\xca'

# FIXME: this is temporary!!
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/agold/Dropbox/Vocabulary/dbs/redux.db"
db = SQLAlchemy(app)


def unauth_callback():
    return {"access": "unauthorized"}


login_manager = fli.LoginManager(app)
login_manager.login_view = "login"
login_manager.unauthorized_handler = unauth_callback


# https://github.com/shihanng/flask-login-example
@login_manager.user_loader
def load_user(uid: str):
    print(f"load user looking for uid: {uid}")
    users_db = UsersDB("users")
    print(f"load user loaded {users_db.id_to_record(uid)}")
    row = users_db.id_to_record(uid)
    if row is not None:
        return User(row['username'])
    else:
        return None


# @app.route("/files/<pattern>")
# def get_files(pattern):
#     files = get_all_dbs(pattern)
#     return {"files": files}


# @app.route("/seldb/<dbname>")
# def sel_db(dbname):
#     session["active_db"] = dbname
#     return {"ok": "active db set"}


def get_conn():
    if "active_db" in session:
        dbname = session["active_db"].lower()
        print(f"get_conn: dbname {dbname}")
        conn = db_connect(dbname)
        return conn
    else:
        raise(ServerException("active db not set"))


@app.route("/getcount")
@fli.login_required
def getcount():
    print(request.headers)
    try:
        total = count_vocab(db.session)
        resp = {"total": total}
        return resp
    except ServerException as e:
        return f"Internal error {e}", 500


@app.route("/fetch")
@fli.login_required
def fetch():
    try:
        print("fetching")

        slugs = fetch_slugs(db.session, 50)
        resp = {"slugs": slugs,
                "count": len(slugs),
                "dir": "fwd",
                "unlearned": False}
        print(resp)
        return resp
    except ServerException as e:
        return f"Internal error: {e}", 500


@app.route("/login", methods=["POST"])
def login():
    login_data = request.get_json(force=True)
    username = login_data["username"]
    pw = login_data["password"]
    lang = login_data["lang"]
    print(f"login: {username} {pw} {lang}")
    session["active_db"] = lang.lower()
    total = count_vocab(db.session)
    user = User(username)
    fli.login_user(user)
    if user.is_authenticated(pw):
        session["username"] = username
        session["uid"] = user.user["rowid"]
        return {"login": "ok",
                "active-db": lang.lower(),
                "total": total}
    else:
        return {"login": "rejected"}
