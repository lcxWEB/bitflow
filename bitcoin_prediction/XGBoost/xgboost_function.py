import pickle
import pandas as pd
import numpy as np
import time
from datetime import datetime
import xgboost as xgb
import requests
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error

# Load the xgboost model
def load_model():
    with open('xgboost_model.pkl', 'rb') as file:
        model_data = pickle.load(file)
    return model_data

def fetch_crypto_data(start_date, end_date):
        """
        Fetch Bitcoin price data from CryptoCompare API
        """
        start_ts = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp())
        end_ts = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp())
        days = (end_ts - start_ts) // 86400 + 1
        
        url = "https://min-api.cryptocompare.com/data/v2/histoday"
        params = {
            "fsym": "BTC",
            "tsym": "USD",
            #"limit": days + 30,
            "limit": 30,
            "toTs": end_ts
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['Response'] != 'Success':
            raise Exception(f"API Error: {data.get('Message', 'Unknown error')}")
            
        df = pd.DataFrame(data['Data']['Data'])
        df['date'] = pd.to_datetime(df['time'], unit='s')
        df = df.rename(columns={
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'volumefrom': 'Volume'
        })
        
        return df

# Predict Bitcoin prices using xgboost model
def predict_prices(start_date, end_date):
    model_data = load_model()
    model = model_data['model']
    # mae = model_data['mae']
    # mape = model_data['mape']

    # Generate the future date range
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Placeholder for exogenous data if needed
    exogenous_data = pd.DataFrame({'sentiment_scores': [0] * len(date_range)}, index=date_range)

    # Placeholder for storing predictions
    future_predictions = []

    # Assume we have the last row of data as the starting point
    last_row = pd.Series({
        'Open': 73297.0,  # Replace with the last known open value
        'High': 73508.0,  # Replace with the last known high value
        'Low': 73297.0,   # Replace with the last known low value
        'Volume': 146.055446, # Replace with the last known volume value
        'sentiment_scores': 0.318447,  # Replace with the last known sentiment score if applicable
        'lag1': 73468.0,
        'lag2': 73468.0,
        'lag7': 73468.0,
        'rolling_mean_7': 70463.285714,
        'rolling_std_7': 4689.409537,
    })

    start_time = time.time()
    # Iteratively predict the next day's price
    for _ in range(len(date_range)):
        input_data = np.array([last_row.values]).reshape(1, -1)

        feature_names = ['Open', 'High', 'Low', 'Volume', 'sentiment_scores', 'lag1', 'lag2', 'lag7', 'rolling_mean_7', 'rolling_std_7']
        dmatrix = xgb.DMatrix(input_data, feature_names=feature_names)  # Convert to DMatrix format
        
        next_pred = model.predict(dmatrix)[0]
        future_predictions.append(next_pred)
        
        # Update last_row for the next iteration (simulate lag features if necessary)
        last_row['Open'] = next_pred  # You can update based on your feature engineering logic

    end_time = time.time()
    runtime = int((end_time - start_time) * 1000) # milliseconds

    future_predictions = [round(pred, 3) for pred in future_predictions]

    df = fetch_crypto_data(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    actual_price = df['Close']
    mae = mean_absolute_error(future_predictions, actual_price)
    mape = mean_absolute_percentage_error(future_predictions, actual_price)

    # Convert predictions to DataFrame
    pred_df = pd.DataFrame({'Date': date_range, 'Predicted_Price': future_predictions})

    return {
        'mae': mae,
        'mape': mape,
        'runtime': runtime,
        'predictions': pred_df
    }

# if __name__ == "__main__":
#     start_date = "2024-10-03"
#     end_date = "2024-11-02"
#     result = predict_prices(start_date, end_date)

#     # Print results
#     print("MAE:", result['mae'])
#     print("MAPE:", result['mape'])
#     print("Runtime:", result['runtime'])
#     print("Predicted Prices:")
#     print(result['predictions'])