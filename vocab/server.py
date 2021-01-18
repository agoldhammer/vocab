import os
import sys
from typing import Optional

import flask_login as fli
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy

from vocab.datafetch import (count_vocab, fetch_slugs, fetch_user_by_id,
                             fetch_user_by_name)
from vocab.fileman import db_exists
# from vocab.fileman import db_connect
from vocab.models import User


class ServerException(Exception):
    pass


site_path = "/Users/agold/Prog/lexy/public"
app = Flask(__name__, static_folder=site_path, template_folder=site_path)
app.secret_key = b"96\x91Q\xf1N\x86\x1b\xc3&1\x92\x9f\tU\xca"

# app.config.from_envvar("SETTINGS")
lang = os.environ.get("LANG")
print(f"Language {lang}")
if lang is not None:
    lang = lang.lower()
    dbpath, dbexists = db_exists(lang)
    if dbexists:
        dbpath = "sqlite:///" + str(dbpath)
        print(f"dbpath: {dbpath}")
        app.config["SQLALCHEMY_DATABASE_URI"] = dbpath
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    else:
        print(f"Database {dbpath} does not exist")
        sys.exit(1)
else:
    print("Must specify LANG env var in server setup script")
    sys.exit(1)

db = SQLAlchemy(app)


def unauth_callback():
    return {"access": "unauthorized"}


login_manager = fli.LoginManager(app)
login_manager.login_view = "login"
login_manager.unauthorized_handler = unauth_callback


# TODO: Check if uid should be unicode string per flask
# https://github.com/shihanng/flask-login-example
@login_manager.user_loader
def load_user(uid: int) -> Optional[User]:
    """load user with given id

    Args:
        uid (int): user id

    Returns:
        models.User or None: [user]
    """
    print(f"load user looking for uid: {uid}")
    user = fetch_user_by_id(db.session, uid)
    if user is not None:
        print(f"User uid {user.uname} is {user}, loaded")
    else:
        print(f"User uid {uid} not found")
    return user


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
        resp = {"slugs": slugs, "count": len(slugs), "dir": "fwd", "unlearned": False}
        print(resp)
        return resp
    except ServerException as e:
        return f"Internal error: {e}", 500


@app.route("/login", methods=["POST"])
def login():
    global lang
    login_data = request.get_json(force=True)
    username = login_data["username"]
    pw = login_data["password"]
    # lang = login_data["lang"]
    print(f"login: {username} {pw} {lang}")
    # dbname is made from lowercased lang request
    total = count_vocab(db.session)
    # user = User(username)
    user = fetch_user_by_name(db.session, username)
    fli.login_user(user)
    if user.is_authenticated(pw):
        session["username"] = username
        session["uid"] = user.uid
        return {"login": "ok", "active-db": lang, "total": total}
    else:
        return {"login": "rejected"}
