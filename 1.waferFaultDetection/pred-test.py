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


# try:

path = "Prediction_Batch_files"
pred_val = predValidation(path)

# calling the prediction_validation function
pred_val.prediction_validation()

# object initialization
pred = prediction(path)

# predicting for dataset present in database
path, json_predictions = pred.prediction_from_model()

print(0)

# except ValueError:
#     print(1)
# except KeyError:
#     print(2)
# except Exception as e:
#     print(str(e))

