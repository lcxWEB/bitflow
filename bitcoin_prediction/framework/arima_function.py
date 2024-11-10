import pickle
import pandas as pd
import time
from datetime import datetime

# Load the ARIMA model
def load_model():
    with open('arima_model.pkl', 'rb') as file:
        model_data = pickle.load(file)
    return model_data

# Predict Bitcoin prices using ARIMA model
def predict_prices(start_date, end_date):
    model_data = load_model()
    model = model_data['model']
    mae = model_data['mae']
    mape = model_data['mape']

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D').to_period('D')
    exogenous_data = pd.DataFrame({'sentiment_scores': [0] * len(date_range)}, index=date_range)

    start_time = time.time()
    forecast_object = model.get_forecast(steps=len(date_range), exog=exogenous_data)
    predictions = forecast_object.predicted_mean # Predicted values
    end_time = time.time()
    runtime = int((end_time - start_time) * 1000) # milliseconds

    pred_list = [(str(date), round(pred, 3)) for date, pred in zip(date_range, predictions)] # List of predictions

    return {
        'mae': mae,
        'mape': mape,
        'runtime': runtime,
        'pred_list': pred_list
    }