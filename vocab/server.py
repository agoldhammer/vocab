from flask import Flask, jsonify

from vocab.fileman import get_all_dbs


app = Flask(__name__)


@app.route("/files")
def get_files():
    files = get_all_dbs("german")
    return jsonify(files)
