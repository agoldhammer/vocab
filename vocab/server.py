from flask import (Flask, session, request)

from vocab.fileman import get_all_dbs, db_connect
from vocab.practice import get_count, fetch_nitems


class ServerException(Exception):
    pass


site_path = "/Users/agold/Prog/lexy/public"
app = Flask(__name__,
            static_folder=site_path,
            template_folder=site_path)
app.secret_key = b'96\x91Q\xf1N\x86\x1b\xc3&1\x92\x9f\tU\xca'


@app.route("/files/<pattern>")
def get_files(pattern):
    files = get_all_dbs(pattern)
    return {"files": files}


@app.route("/seldb/<dbname>")
def sel_db(dbname):
    session["active_db"] = dbname
    return {"ok": "active db set"}


def get_conn():
    if "active_db" in session:
        dbname = session["active_db"]
        conn = db_connect(dbname)
        return conn
    else:
        raise(ServerException("active db not set"))


@app.route("/getcount")
def getcount():
    print(request.headers)
    try:
        conn = get_conn()
        total, nfrom, nto = get_count(conn)
        conn.close()
        resp = {"total": total,
                "nfrom": nfrom,
                "nto": nto}
        return resp
    except ServerException as e:
        return f"Internal error {e}", 500


@app.route("/fetch")
def fetch():
    try:
        conn = get_conn()
        curs = conn.cursor()
        slugs = fetch_nitems(curs, 50, True, False, web=True)
        conn.close()
        resp = {"slugs": slugs,
                "count": len(slugs),
                "dir": "fwd",
                "unlearned": False}
        return resp
    except ServerException as e:
        return f"Internal error: {e}", 500


@app.route("/login", methods=["POST"])
def login():
    # print(f"headers: {request.headers}")
    # print(f"json: {request.get_json(force=True)}")
    # print(f"request parms: {request.values}")
    # print(f"request form {request.form}")
    logdata = request.get_json(force=True)
    uname, pw = logdata["uname"], logdata["pw"]
    print(uname, pw)
    return {"login": "ok"}
