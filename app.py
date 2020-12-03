import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from flask import Flask, request, jsonify
import pickle
import joblib
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

@app.route('/')
def home():
    return "Hello API"


@app.route('/predict', methods = ['GET'])
def predict():
    model = joblib.load('model.pkl')
    if request.method == 'GET':
        #answer_list = []
        Age = int(request.args.get("age"))  #@param {type:"number"}
        Driving_License = str(request.args.get("driving_license")) == "Yes"  #@param {type:"boolean"}
        Region_Code = int(request.args.get("region_code")) #@param {type:"number"}
        Previously_Insured = str(request.args.get("previously_insured")) == "Yes" #@param {type:"boolean"}
        Annual_Premium = int(request.args.get("annual_premium")) #@param {type:"number"}
        Policy_Sales_Channel = int(request.args.get("policy_sales_channel")) #@param {type:"number"}
        Vintage = int(request.args.get("vintage")) #@param {type:"number"}
        Gender = str(request.args.get("gender")) #@param ['Male', 'Female'] {type:"string"}
        Vehicle_Age = str(request.args.get("vehicle_age")) #@param ['< 1 Year', '1-2 Year', '> 2 Years'] {type:"string"}
        Vehicle_Damage_Yes =  str(request.args.get("vehicle_damage_yes")) == "Yes" #@param {type:"boolean"}

        Driving_License_No = 1
        if str(request.args.get("driving_license")) == "Yes":
            Driving_License_No = 0

        Driving_License_Yes = 0
        if str(request.args.get("driving_license")) == "Yes":
           Driving_License_Yes = 1

        Previously_Insured_No = 1
        if str(request.args.get("previously_insured")) == "Yes":
           Previously_Insured_No = 0

        Previously_Insured_Yes = 0
        if str(request.args.get("previously_insured")) == "Yes":
           Previously_Insured_Yes = 1

        Gender_Female = 0
        if str(request.args.get("gender")) == "Female":
           Gender_Female = 1

        Gender_Male = 1
        if str(request.args.get("gender")) == "Female":
           Gender_Male = 0

        Vehicle_Age_1_Year = 0
        Vehicle_Age_1_2_Year = 0
        Vehicle_Age_2_Years = 0
        if str(request.args.get("vehicle_age")) == "< 1 Year":
            Vehicle_Age_1_Year = 1
        elif str(request.args.get("vehicle_age")) == "1-2 Year":
            Vehicle_Age_1_2_Year = 1
        elif str(request.args.get("vehicle_age")) == "> 2 Years":   
            Vehicle_Age_2_Years=1

        Vehicle_Damage_Yes = 0
        if str(request.args.get("vehicle_damage_yes")) == "Yes":
           Vehicle_Damage_Yes = 1

        Vehicle_Damage_No = 1
        if str(request.args.get("vehicle_damage_yes")) == "Yes":
           Vehicle_Damage_No = 0

        feature = [Age, Region_Code, Annual_Premium, Policy_Sales_Channel, Vintage, Gender_Female, Gender_Male, Driving_License_No, Driving_License_Yes, Previously_Insured_No, Previously_Insured_Yes, Vehicle_Age_1_Year, Vehicle_Age_1_2_Year, Vehicle_Age_2_Years, Vehicle_Damage_No, Vehicle_Damage_Yes]
        feature = np.array(feature).reshape(1,-1)

        if model.predict(feature)[0] == 1:
            return "Customer is interested"
        elif model.predict(feature)[0] == 0:
            return "Customer is not interested"
            
   

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
