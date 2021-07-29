import yaml
import os
import json
import joblib # Used to load the model
import numpy as np


params_path = "params.yaml"
schema_path = os.path.join("prediction_service", "schema_in.json") # The dictionary file where the ranges will be stored

class NotInRange(Exception): # To provide error message to user stating that the values are not in the range""
    def __init__(self, message="Values Entered are not in the range"):
        self.message = message
        super().__init__(self.message) # To read the message

class NotInCols(Exception): # To provide error message to user stating that the column data is not available, this is used when a person is using our application but in api format
    def __init__(self, message="Not in Columns"):
        self.message = message
        super.__init__(self.message) # To read the message

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def predict(data):
    config = read_params(params_path)
    model_dir_path = config["webapp_model_dir"]
    model = joblib.load(model_dir_path)
    prediction = model.predict(data).tolist()[0] # The reason to use 0 in list is to stop the output to be printed in list format.

    try:
        if 3 <= prediction <= 8:
            return prediction
        else:
            raise NotInRange
    except NotInRange:
        return "UnExpected Result"

def get_schema(schema_path=schema_path): # Using the schema_in file to get the range of values
    with open(schema_path) as json_file:
        schema = json.load(json_file)
    return schema

def validate_input(dict_request): # Validating User Input
    def _validate_cols(col):
        schema = get_schema()
        actual_cols = schema.keys()
        if col not in actual_cols:
            raise NotInCols
    
    def _validate_values(val):
        schema = get_schema()
        if not(schema[col]["min"] <= float(dict_request[col]) <= schema[col]["max"]):
            raise NotInRange
        
    for col, val in dict_request.items():
        _validate_cols(col) # The reason to use _ is to make sure that its a internal function
        _validate_values(col, val)
    return True

def form_response(dict_request): # Validating form response
    if validate_input(dict_request):
        data = dict_request.values()
        data = [list(map(float, data))]
        response = predict(data)
        return response

def api_response(dict_request): # Getting user input in API form and valdiating it
    try:
        if validate_input(dict_request):
            data = np.array([list(dict_request.values)])
            response = predict(data)
            response ={'response':response}
            return response
    except Exception as e: # If the api response fail to pass through the parameters we will rise this error.
        response = {"The_Expected_Range":get_schema(), "response":str(e)}
        return response