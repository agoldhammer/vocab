from flask import Flask, jsonify, session, request

from vocab.fileman import get_all_dbs, db_connect
from vocab.practice import get_count, fetch_nitems


class ServerException(Exception):
    pass


app = Flask(__name__)
app.secret_key = b'96\x91Q\xf1N\x86\x1b\xc3&1\x92\x9f\tU\xca'


@app.route("/files/<pattern>")
def get_files(pattern):
    files = get_all_dbs(pattern)
    return jsonify(files)


@app.route("/seldb/<dbname>")
def sel_db(dbname):
    session["active_db"] = dbname
    return "active db set"


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
        return f"internal error: {e}"


@app.route("/fetch")
def fetch():
    try:
        conn = get_conn()
        curs = conn.cursor()
        slugs = fetch_nitems(curs, 5, True, False, web=True)
        conn.close()
        return {"slugs": slugs,
                "count": len(slugs),
                "dir": "fwd",
                "unlearned": False}
    except ServerException as e:
        return f"Internal error: {e}"
