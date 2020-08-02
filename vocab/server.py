from flask import (Flask, jsonify, session,
                   render_template, request,
                   send_from_directory)

from vocab.fileman import get_all_dbs, db_connect
from vocab.practice import get_count, fetch_nitems


class ServerException(Exception):
    pass


site_path = "/Users/agold/Prog/lexy/public"
app = Flask(__name__,
            static_folder=site_path,
            template_folder=site_path)
app.secret_key = b'96\x91Q\xf1N\x86\x1b\xc3&1\x92\x9f\tU\xca'


@app.route("/")
def index():
    return(render_template("index.html"))


@app.route("/css/<fname>")
def css(fname):
    print(fname)
    return send_from_directory(f"{site_path}/css/", fname)


@app.route("/js/compiled/<fname>")
def js(fname):
    print(fname)
    return send_from_directory(f"{site_path}/js/compiled", fname)


# TODO: for dev only, remove later
def prepare_response(resp, status_code):
    """add headers to response

    Args:
        resp ([raw response]): [response to request]

    Returns:
        [json resp]: [with heaers]
    """
    response = jsonify(resp)
    response.headers.set('Access-Control-Allow-Origin', 'http://localhost:8700')
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST')
    response.headers.set('Access-Control-Allow-Credentials', "true")
    return response, status_code


@app.route("/files/<pattern>")
def get_files(pattern):
    files = get_all_dbs(pattern)
    return prepare_response(files, 200)


@app.route("/seldb/<dbname>")
def sel_db(dbname):
    session["active_db"] = dbname
    return prepare_response("active db set", 200)


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
        return prepare_response(resp, 200)
    except ServerException as e:
        return prepare_response(f"internal error: {e}")


@app.route("/fetch")
def fetch():
    try:
        conn = get_conn()
        curs = conn.cursor()
        slugs = fetch_nitems(curs, 5, True, False, web=True)
        conn.close()
        resp = {"slugs": slugs,
                "count": len(slugs),
                "dir": "fwd",
                "unlearned": False}
        return prepare_response(resp, 200)
    except ServerException as e:
        return f"Internal error: {e}"
