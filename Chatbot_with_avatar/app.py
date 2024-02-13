import os
from wsgiref import simple_server
from flask import Flask, render_template, jsonify, request, Response


app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


port = int(os.getenv("PORT", 5000))
if __name__ == "__main__":
    host = "0.0.0.0"
    httpd = simple_server.make_server(host, port, app)
    print("Serving on %s %d" % (host, port))
    # http://localhost:5000
    httpd.serve_forever()
