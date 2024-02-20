import os
import pickle
import json
from pathlib import Path
from wsgiref import simple_server
from flask import Flask, render_template, jsonify, request, Response
from flask_cors import CORS, cross_origin
import requests
from langchain_helper import create_pickle_file


app = Flask(__name__)
CORS(app)


@app.route("/answer", methods=["POST"])
@cross_origin()
def return_response():
    try:
        if request.json is not None:
            pass
            user_query = request.json["userquery"]

            create_pickle_file()

            fileObj = open("data.obj", "rb")
            chat = pickle.load(fileObj)
            fileObj.close()

            answer = chat.return_response(user_query)

            fileObj = open("data.obj", "wb")
            pickle.dump(chat, fileObj)
            fileObj.close()

            return jsonify({"answer": answer}), 200

        else:
            return Response("Please enter a valid query")

    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)


@app.route("/")
@cross_origin()
def hello_world():
    return render_template("index.html")


port = int(os.getenv("PORT", 5000))
if __name__ == "__main__":
    if Path("data.obj").exists():
        Path("data.obj").unlink()
    host = "0.0.0.0"
    httpd = simple_server.make_server(host, port, app)
    print("Serving on %s %d" % (host, port))
    # http://localhost:5000
    httpd.serve_forever()
