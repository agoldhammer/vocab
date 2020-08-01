from flask import Flask, jsonify, session, request

from vocab.fileman import get_all_dbs, db_connect
from vocab.practice import get_count


app = Flask(__name__)
app.secret_key = b'96\x91Q\xf1N\x86\x1b\xc3&1\x92\x9f\tU\xca'


@app.route("/files")
def get_files():
    files = get_all_dbs("german")
    return jsonify(files)


@app.route("/seldb/<dbname>")
def sel_db(dbname):
    session["active_db"] = dbname
    return "active db set"


@app.route("/getcount")
def getcount():
    print(request.headers)
    if "active_db" in session:
        dbname = session["active_db"]
        conn = db_connect(dbname)
        total, nfrom, nto = get_count(conn)
        resp = {"total": total,
                "nfrom": nfrom,
                "nto": nto}
        return resp
    else:
        return "internal error: active db not set"
