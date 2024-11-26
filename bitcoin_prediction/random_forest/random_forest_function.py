import pandas as pd
import numpy as np
import requests
import datetime
import joblib
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
import time


# Get actual Bitcoin price between startDate and endDate
def get_actual_bitcoin_prices(startDate, endDate):
    url = 'https://min-api.cryptocompare.com/data/v2/histoday'
    params = {
        'fsym': 'BTC',
        'tsym': 'USD',
        'limit': 2000,
        'toTs': int(datetime.datetime.strptime(endDate, "%Y-%m-%d").timestamp())
    }
    response = requests.get(url, params=params)
    data = response.json()
    if 'Data' in data and 'Data' in data['Data']:
        prices = data['Data']['Data']
        df = pd.DataFrame(prices)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', inplace=True)
        df = df.loc[startDate:endDate]
        return df
    else:
        raise ValueError("Could not retrieve data from API")
# Prepare input features for prediction
def prepare_features(scaler, prices):
    features = pd.DataFrame()
    features['sentiment_scores'] = prices.get('sentiment_scores', 0)  # Assuming sentiment scores are available, set to 0 if not
    features['Open'] = prices['open']
    features['High'] = prices['high']
    features['Low'] = prices['low']
    features['Volume'] = prices['volumeto']
    # Reindex features to ensure correct column order
    features = features.reindex(columns=scaler.feature_names_in_)
    if features.empty:
        raise ValueError("No valid data available after processing. Please check the input date range or feature preparation.")
    scaled_features = scaler.transform(features)
    return scaled_features, features.index

# Predict Bitcoin prices between startDate and endDate
def predict_bitcoin_prices(rf_model, scaler, startDate, endDate):
    actual_prices = get_actual_bitcoin_prices(startDate, endDate)
    X, dates = prepare_features(scaler, actual_prices)
    predicted_prices = rf_model.predict(X)
    return pd.Series(predicted_prices, index=dates)

# Plot the actual vs predicted Bitcoin prices
def plot_prices(actual_prices, predicted_prices, runtime, mae, mape):
    plt.figure(figsize=(10, 6))
    plt.plot(actual_prices.index, actual_prices, label='Actual Prices', color='green')
    plt.plot(predicted_prices.index, predicted_prices, label='Predicted Prices', color='red')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.title('Bitcoin Price Prediction vs Actual Prices')
    plt.legend()
    plt.grid()
    plt.figtext(0.15, 0.01, f"Runtime: {runtime} ms, MAE: {mae:.2f}, MAPE: {mape:.2f}%", fontsize=10)
    plt.show()




def predict(startDate, endDate):
    # Import model 
    model_file_path = os.path.join(os.path.dirname(__file__), 'rf_model.pkl')
    if not os.path.exists(model_file_path):
        raise FileNotFoundError(f"Model file '{model_file_path}' not found. Please ensure the model is trained and saved.")
    rf_model = joblib.load(model_file_path)
    # Import Scaler 
    scaler_file_path = os.path.join(os.path.dirname(__file__), 'rf_scaler.pkl')
    if not os.path.exists(scaler_file_path):
        raise FileNotFoundError(f"Scaler file '{scaler_file_path}' not found. Please ensure the scaler is trained and saved.")
    scaler = joblib.load(scaler_file_path)

    # Get real price
    actual_prices = get_actual_bitcoin_prices(startDate, endDate)
    # Measure prediction runtime
    start_time = time.time()
    predicted_prices = predict_bitcoin_prices(rf_model,scaler, startDate, endDate)
    runtime = int((time.time() - start_time) * 1000)
    mae = mean_absolute_error(actual_prices['close'][-len(predicted_prices):], predicted_prices)
    mape = mean_absolute_percentage_error(actual_prices['close'][-len(predicted_prices):], predicted_prices) * 100
    forecast_array = [{"date": date.strftime("%Y-%m-%d"), "price": round(price, 3)}
                  for date, price in zip(predicted_prices.index, predicted_prices)]
    #forecast_array = [{"date": date.strftime("%Y-%m-%d"), "price": price} for date, price in zip(predicted_prices.index, predicted_prices)]
    # Output to console
    print("MAE:", mae)
    print("MAPE:", mape)
    print("Runtime (ms):", runtime)
    print("Forecast Array:", forecast_array)
    return mae, mape, runtime, forecast_array

    
# Main function
def main():
    # Load the Random Forest model and scaler
    rf_model = joblib.load(os.path.join(os.path.dirname(__file__), 'rf_model.pkl'))
    scaler = joblib.load(os.path.join(os.path.dirname(__file__), 'rf_scaler.pkl'))

    startDate = "2024-10-01"
    endDate = "2024-10-31"
    actual_prices = get_actual_bitcoin_prices(startDate, endDate)
    # Measure prediction runtime
    start_time = time.time()
    predicted_prices = predict_bitcoin_prices(rf_model, startDate, endDate)
    runtime = int((time.time() - start_time) * 1000)
    mae = mean_absolute_error(actual_prices['close'][-len(predicted_prices):], predicted_prices)
    mape = mean_absolute_percentage_error(actual_prices['close'][-len(predicted_prices):], predicted_prices) * 100
    plot_prices(actual_prices['close'][-len(predicted_prices):], predicted_prices, runtime, mae, mape)

if __name__ == "__main__":
    startDate = "2024-10-01"
    endDate = "2024-10-31"
    predict(startDate, endDate)