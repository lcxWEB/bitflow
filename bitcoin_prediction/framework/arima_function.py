import pickle
import pandas as pd
import time
from datetime import datetime
import os
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
import matplotlib.pyplot as plt
import requests


# Load the ARIMA model
def load_model():
    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 拼接模型文件的完整路径
    model_path = os.path.join(current_dir, 'arima_model.pkl')
    
    # 加载模型
    with open(model_path, 'rb') as file:
        model_data = pickle.load(file)
    
    return model_data
# def load_model():
#     # 拼接模型路径
#     model_path = os.path.join(os.path.dirname(__file__), 'bitcoin_prediction', 'framework', 'arima_model.pkl')
    
#     # 检查路径是否正确
#     if not os.path.exists(model_path):
#         raise FileNotFoundError(f"ARIMA model file not found at {model_path}")
    
#     # 加载模型
#     with open(model_path, 'rb') as file:
#         model_data = pickle.load(file)
    
#     return model_data
# def load_model():
#     with open('arima_model.pkl', 'rb') as file:
#         model_data = pickle.load(file)
#     return model_data

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

# Fetch actual Bitcoin prices from the API
def fetch_actual_prices(start_date, end_date):
    url = "https://min-api.cryptocompare.com/data/v2/histoday"
    params = {
        "fsym": "BTC",
        "tsym": "USD",
        "limit": 2000,
        "toTs": int(pd.Timestamp(end_date).timestamp()),  # End timestamp
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()["Data"]["Data"]
        df = pd.DataFrame(data)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df.set_index("time", inplace=True)
        return df.loc[start_date:end_date, "close"]
    else:
        raise ValueError(f"Failed to fetch data: {response.status_code}")

# Predict and compare prices for 2024-10-25 to 2024-11-21
def predict_and_compare_future():
    start_date = '2024-10-25'
    end_date = '2024-11-21'

    # Fetch actual prices
    actual_prices = fetch_actual_prices(start_date, end_date)

    # Predict prices using the ARIMA model
    result = predict_prices(start_date, end_date)
    predictions = pd.Series(
        [item[1] for item in result['pred_list']],
        index=pd.to_datetime([item[0] for item in result['pred_list']])
    )

    # Calculate metrics
    mae = mean_absolute_error(actual_prices, predictions)
    mape = mean_absolute_percentage_error(actual_prices, predictions) * 100

    # Plot comparison
    plt.figure(figsize=(12, 6))
    plt.plot(actual_prices.index, actual_prices, label='Actual Prices', color='blue')
    plt.plot(predictions.index, predictions, label='Predicted Prices', color='red')
    plt.title(f'Bitcoin Price Prediction (2024-10-25 to 2024-11-21)\nMAE: {mae:.2f}, MAPE: {mape:.2f}%')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid()
    plt.savefig('Future_Price_Comparison.png')
    plt.show()

    print(f"Future MAE: {mae:.2f}")
    print(f"Future MAPE: {mape:.2f}%")

# Predict and compare prices for 2022-04 to 2024-10
def predict_and_compare_historical():
    start_date = '2022-04-01'
    end_date = '2024-10-03'

    # Fetch actual prices
    actual_prices = fetch_actual_prices(start_date, end_date)

    # Predict prices using the ARIMA model
    result = predict_prices(start_date, end_date)
    predictions = pd.Series(
        [item[1] for item in result['pred_list']],
        index=pd.to_datetime([item[0] for item in result['pred_list']])
    )

    # Calculate metrics
    mae = mean_absolute_error(actual_prices, predictions)
    mape = mean_absolute_percentage_error(actual_prices, predictions) * 100

    # Plot comparison
    plt.figure(figsize=(12, 6))
    plt.plot(actual_prices.index, actual_prices, label='Actual Prices', color='blue')
    plt.plot(predictions.index, predictions, label='Predicted Prices', color='red')
    plt.title(f'Bitcoin Price Prediction (2022-04 to 2024-10)\nMAE: {mae:.2f}, MAPE: {mape:.2f}%')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid()
    plt.savefig('Historical_Price_Comparison.png')
    plt.show()

    print(f"Historical MAE: {mae:.2f}")
    print(f"Historical MAPE: {mape:.2f}%")

# Example usage
if __name__ == "__main__":
    # Compare future prices
    predict_and_compare_future()

    # Compare historical prices
    predict_and_compare_historical()
