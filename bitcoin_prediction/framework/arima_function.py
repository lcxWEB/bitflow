import pickle
import pandas as pd
import time
from datetime import datetime
import os

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