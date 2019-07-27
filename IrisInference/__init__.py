# Azure Function for scoring a model trained on the iris dataset
#
# July 2019, FastTrack for Azure - jose.moreno@microsoft.com
#
# Simple function for loading a model trained on the Iris dataset with joblib and score data supplied in JSON payload
# The model could have been trained in different ways, for example, using Azure ML.
#
# Using joblib to serialize the model because it tends to be more solid than pickle for sklearn models

import logging
import azure.functions as func
import json, joblib, os
import numpy as np

# Importing sklearn not required for scoring
# from sklearn.svm import SVC

def init(model_filename):
    print("Loading model...")
    try:
        model = joblib.load(model_filename)
        return model
    except:
        return None

# note you can pass in multiple rows for scoring
def predict(model, raw_data):
    try:
        #data = json.loads(raw_data)['data']
        data = raw_data['data']
        data = np.array(data)
        logging.info("Predicting: " + str(data))
        result = model.predict(data)
        return result.tolist()
    except Exception as e:
        logging.error('Error when trying to load model')
        return str(e)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    # Let's init some variables
    model_filename = './irismodel.pkl'
    req_body = req.get_json()

    # Try to get a model
    model = init(model_filename)
    if model is None:
        # We include some troubleshooting info in the response if the model file could not be found
        response = {'operation_result': 'error - model file {0} not found'.format(model_filename),
            'data': str(req_body['data']),
            'cwd': os.getcwd(),
            'files_in_cwd': str(os.listdir()) }
        response_string = json.dumps(response)
        return func.HttpResponse(response_string, status_code=400)

    # With the model, run the prediction
    logging.info('Starting prediction')
    score_result = predict(model, req_body)
    logging.info('Prediction result: ' + str(score_result))

    # Verify we got a list, everything else is considered to be an error
    if isinstance(score_result, list):
        response = {'operation_result': 'success', 
                    'data': str(req_body['data']),
                    'prediction': str(score_result) }
        response_string = json.dumps(response)
        return func.HttpResponse(response_string)
    else:
        response = {'operation_result': 'error',
                    'data': str(req_body['data']),
                    'prediction': str(score_result),
                    'prediction data type': str(type(score_result)) }
        response_string = json.dumps(response)
        return func.HttpResponse(response_string, status_code=400)
