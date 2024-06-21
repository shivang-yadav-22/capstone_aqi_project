# Importing necessary libraries
from flask import Flask, request, render_template
import pandas as pd
import joblib
import os
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Directory where joblib files are stored
model_directory = 'models/'

# Load models
models = {
  
    'Model 1': joblib.load(os.path.join(model_directory, 'my_lasso_model.joblib')),
    'Model 2': joblib.load(os.path.join(model_directory, 'my_model.joblib')),
    'Model 3': joblib.load(os.path.join(model_directory, 'my_ridge_model(1).joblib'))
}


# Define the home route
@app.route('/')
def home():
    return render_template('index.html', models=models.keys())

# Define the predict route
@app.route('/predict', methods=['POST'])
def predict():
    selected_model = request.form['model']
    model = models[selected_model]

    int_features =  [30.0,23.0,
                    float(request.form['NO']),
                    float(request.form['NO2']),
                    float(request.form['NOx']),
                    float(request.form['NH3']),
                    float(request.form['CO']),
                    float(request.form['SO2']),
                    float(request.form['O3']),
                    float(request.form['Benzene']),
                    float(request.form['Toluene'])]
     
    columns = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene']
# Create a DataFrame using the input features and columns
    df = pd.DataFrame([int_features], columns=columns)

# Make prediction
    prediction = model.predict(df)
    prediction = int(prediction)
    print(prediction)
    # Determine air quality based on AQI
    if 0 <= prediction <= 50:
        prediction_text = '{}'.format(prediction)
        prediction_text1 = 'good'
        prediction_text2 = 'Air quality is good. Enjoy outdoor activities!'
    elif 51 <= prediction <= 100:
        prediction_text = '{}'.format(prediction)
        prediction_text1 = 'moderate'
        prediction_text2 = 'Air quality is moderate. Limit outdoor exertion.'
    elif 101 <= prediction <= 200:
        prediction_text = '{}'.format(prediction)
        prediction_text1 = 'unhealthy'
        prediction_text2 = 'Air quality is unhealthy. Avoid prolonged outdoor activities.'
    elif 201 <= prediction <= 300:
        prediction_text = '{}'.format(prediction)
        prediction_text1 = 'sensitive'
        prediction_text2 = 'Air quality is sensitive. Take necessary precautions, especially if you are sensitive to pollution.'
    else:
        prediction_text = '{}'.format(prediction)
        prediction_text1 = 'hazardous'
        prediction_text2 = 'Air quality is hazardous. Stay indoors and keep windows closed.'

    return render_template('meter.html', aqii=prediction,pred=prediction_text1,pred2=prediction_text2)

if __name__ == "__main__":
    app.run(debug=True)
