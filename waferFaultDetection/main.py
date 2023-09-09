from wsgiref import simple_server
from flask import Flask, request, render_template
from flask import Response
import os
from flask_cors import CORS, cross_origin
from prediction_Validation_Insertion import predValidation
from training_model_module import trainModel
from training_Validation_Insertion import train_validation
import flask_monitoringdashboard as dashboard
from predictFromModel import prediction
import json

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
@cross_origin()
def predict_route_client():
    try:
        if request.json is not None:
            path = request.json['filepath']

            # object initialization
            pred_val = predValidation(path)

            # calling the prediction_validation function
            pred_val.prediction_validation()

            # object initialization
            pred = prediction(path)

            # predicting for dataset present in database
            path, json_predictions = pred.predictionFromModel()
            return Response(f"Prediction File created at !!! {str(path)} and few of the predictions are {str(json.loads(json_predictions))}")
        elif request.form is not None:
            path = request.form['filepath']

            # object initialization
            pred_val = predValidation(path)

            # calling the prediction_validation function
            pred_val.prediction_validation()

            # object initialization
            pred = prediction(path)

            # predicting for dataset present in database
            path, json_predictions = pred.predictionFromModel()
            return Response(f"Prediction File created at !!! {str(path)} and few of the predictions are {str(json.loads(json_predictions))}")
        else:
            print('Nothing Matched')
    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as ex:
        return Response("Error Occurred! %s" % ex)


@app.route("/train", methods=['POST'])
@cross_origin()
def train_route_client():

    try:
        if request.json['folderPath'] is not None:
            path = request.json['folderPath']
            # object initialization
            train_val_obj = train_validation(path)

            # calling the training_validation function
            train_val_obj.train_validation()

            # object initialization
            train_model_obj = trainModel()

            # training the model for the files in the table
            train_model_obj.training_model()

    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred! %s" % e)
    return Response("Training successful!!")


port = int(os.getenv("PORT", 5000))
if __name__ == "__main__":
    host = '0.0.0.0'
    httpd = simple_server.make_server(host, port, app)
    print("Serving on %s %d" % (host, port))
    # http://localhost:5000
    httpd.serve_forever()
