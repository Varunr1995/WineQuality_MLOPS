# The main reason to use test_config.py file is that when we deploy the project in to a page, the user will provide inputs.
# If the values provided by the user is too low or too high which we call it as outlier's then the output generated will be false.
# In order to overcome the issue we will specify a range of values that the user need to provide as input.
# If the value doesn't reside in that range, then the error will popup stating that the value is out off range please change it.
# By getting this notification the user will change the values.


import json
import logging
import os
import joblib
import pytest
from prediction_service.prediction import form_response, api_response
import prediction_service

input_data = {
    "incorrect_range": 
    {"fixed_acidity": 7897897, 
    "volatile_acidity": 555, 
    "citric_acid": 99, 
    "residual_sugar": 99, 
    "chlorides": 12, 
    "free_sulfur_dioxide": 789, 
    "total_sulfur_dioxide": 75, 
    "density": 2, 
    "pH": 33, 
    "sulphates": 9, 
    "alcohol": 9
    },

    "correct_range":
    {"fixed_acidity": 5, 
    "volatile_acidity": 1, 
    "citric_acid": 0.5, 
    "residual_sugar": 10, 
    "chlorides": 0.5, 
    "free_sulfur_dioxide": 3, 
    "total_sulfur_dioxide": 75, 
    "density": 1, 
    "pH": 3, 
    "sulphates": 1, 
    "alcohol": 9
    },

    "incorrect_col":
    {"fixed acidity": 5, 
    "volatile acidity": 1, 
    "citric acid": 0.5, 
    "residual sugar": 10, 
    "chlorides": 0.5, 
    "free sulfur dioxide": 3, 
    "total_sulfur dioxide": 75, 
    "density": 1, 
    "pH": 3, 
    "sulphates": 1, 
    "alcohol": 9
    }
}

TARGET_range = {
    "min": 3.0,
    "max": 8.0
}

def test_form_response_correct_range(data = input_data['correct_range']):
    res = form_response(data)
    assert TARGET_range["min"] <= res <= TARGET_range["max"]

def test_api_response_correct_range(data = input_data['correct_range']):
    res = api_response(data)
    assert TARGET_range["min"] <= res['response'] <= TARGET_range["max"] # The reason to use the response in specific is that the api response should be in json format.

def test_form_response_incorrect_range(data=input_data["incorrect_range"]):
    with pytest.raises(prediction_service.prediction.NotInRange):
        res = form_response(data)

def test_api_response_incorrect_range(data=input_data["incorrect_range"]):
    res = api_response(data)
    assert res["response"] == prediction_service.prediction.NotInRange().message # The reason to use the response in specific is that the api response should be in json format.

def test_api_response_incorrect_col(data=input_data["incorrect_col"]):
    res = api_response(data)
    assert res["response"] == prediction_service.prediction.NotInCols().message