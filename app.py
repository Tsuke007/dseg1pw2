import numpy as np
from flask import Flask, request
import joblib
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

wsgi_app = app.wsgi_app


@app.route('/')
def home():
    return "Hello DSEG1"


@app.route('/predict', methods = ['GET'])
def predict():
    model = joblib.load('model.pkl')
    if request.method == 'GET':

        Age = int(request.args.get("age"))
        Driving_License = str(request.args.get("driving_license")) == "Yes"
        Region_Code = int(request.args.get("region_code"))
        Previously_Insured = str(request.args.get("previously_insured")) == "Yes"
        Annual_Premium = int(request.args.get("annual_premium"))
        Policy_Sales_Channel = int(request.args.get("policy_sales_channel"))
        Vintage = int(request.args.get("vintage"))
        Gender = str(request.args.get("gender"))
        Vehicle_Age = str(request.args.get("vehicle_age"))
        Vehicle_Damage_Yes =  str(request.args.get("vehicle_damage_yes")) == "Yes"

        Driving_License_No = 1
        if str(request.args.get("driving_license")) == "Yes":
            Driving_License_No = 1

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
    app.run()
    #import os
    #host = os.environ.get('server_host', 'localhost')
    #try:
    #    port = int(os.environ.get('server_port', '5555'))
    #except valueerror:
    #    port = 5555

    #app.run(host, port)
