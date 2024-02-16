import os
from wsgiref import simple_server
from flask import Flask, render_template, jsonify, request, Response
from flask_cors import CORS, cross_origin
import requests


app = Flask(__name__)
CORS(app)

# @app.route('/talks/streams', methods=['POST'])
# def proxy():
#     try:
#         url = 'https://api.d-id.com/talks/streams'
#         headers = {
#             'Authorization': request.headers.get('Authorization'),
#             'Content-Type': 'application/json'
#         }
#         response = requests.post(url, headers=headers, json=request.json)
#         return jsonify(response.json()), response.status_code
#     except Exception as e:
#         print('Error proxying request:', e)
#         return 'Internal Server Error', 500


@app.route("/")
@cross_origin()
def hello_world():
    return render_template("index.html")


port = int(os.getenv("PORT", 5000))
if __name__ == "__main__":
    host = "0.0.0.0"
    httpd = simple_server.make_server(host, port, app)
    print("Serving on %s %d" % (host, port))
    # http://localhost:5000
    httpd.serve_forever()
