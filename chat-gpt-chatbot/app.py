from flask import Flask, render_template, jsonify, request
import config
import openai
import aiapi


def page_not_found(e):
    return render_template("404.html"), 404


app = Flask(__name__)
app.config.from_object(config.config["development"])

app.register_error_handler(404, page_not_found)


@app.route("/", methods=["POST", "GET"])
def index():

    if request.method == "POST":
        prompt = request.form["prompt"]

        # answer = aiapi.generate_response(prompt)
        answer = "This is where you get gpt response"
        response = {"answer": answer}
        return jsonify(response), 200

    return render_template("index.html", **locals())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8888", debug=True)
