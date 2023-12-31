from flask import Flask
from housing.logger import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def index():
    logger.info("We are testing logging module")
    return "Starting Machine Learning Project"


if __name__ == "__main__":
    app.run(debug=True)