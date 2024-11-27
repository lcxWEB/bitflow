import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import requests
import time
import joblib
from tensorflow.keras.models import load_model
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import MinMaxScaler
import sys
import os

def predict_bitcoin_prices(start_date, end_date):
    """
    Predict Bitcoin prices for a specified date range using LSTM model.
    
    Args:
        start_date (str): Start date in format 'YYYY-MM-DD'
        end_date (str): End date in format 'YYYY-MM-DD'
    
    Returns:
        dict: Dictionary containing:
            - mae (float): Mean Absolute Error
            - mape (float): Mean Absolute Percentage Error
            - runtime (int): Prediction runtime in milliseconds
            - pred_list (list): List of predicted prices
            - actual_prices (list): List of actual prices
    """
    
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
            "limit": days + 30,
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
    
    try:
        # 添加项目根目录到 sys.path
        # current_dir = os.path.dirname(os.path.abspath(__file__))  # 获取 LSTM_function.py 所在目录
        # project_root = os.path.join(current_dir, '.')  # 获取项目根目录
        # sys.path.append(project_root)       

        # 现在可以导入 config 内的 model_config
        #from config.model_config import ModelConfig
        # Load model and setup

        # 获取当前脚本的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))        

        # 拼接 config 文件夹的绝对路径
        config_dir = os.path.join(current_dir, 'config')        

        # 将 config 文件夹添加到 sys.path
        sys.path.append(config_dir)
        print("sys.path:", sys.path)
        #sys.path.append('./config')
        from model_config import ModelConfig

        # 获取当前脚本的绝对路径
        lstm_current_dir = os.path.dirname(os.path.abspath(__file__))

        # 拼接模型文件的绝对路径
        lstm_model_path = os.path.join(lstm_current_dir, 'models', 'lstm_model.keras')

        # 检查模型文件是否存在
        if not os.path.exists(lstm_model_path):
            raise FileNotFoundError(f"Model file not found at {lstm_model_path}")

        # 加载模型
        model = load_model(lstm_model_path)

        #model = load_model('./models/lstm_model.keras')
        
        # Fetch and prepare data
        df = fetch_crypto_data(start_date, end_date)
        df['sentiment_scores'] = 0.5
        df['is_real_sentiment'] = False
        
        # Prepare features
        features = ['Open', 'Volume', 'sentiment_scores', 'is_real_sentiment']
        X = df[features]
        y = df['Close']
        
        # Normalize data
        scaler_X_new = MinMaxScaler()
        scaler_y_new = MinMaxScaler()
        X_normalized = pd.DataFrame(
            scaler_X_new.fit_transform(X),
            columns=X.columns,
            index=X.index
        )
        y_normalized = pd.DataFrame(
            scaler_y_new.fit_transform(y.values.reshape(-1, 1)),
            columns=['Close'],
            index=y.index
        )
        
        # Create sequences
        def create_sequences(X, y, time_steps=30):
            Xs, ys = [], []
            for i in range(len(X) - time_steps):
                Xs.append(X.iloc[i:(i + time_steps)].values)
                ys.append(y.iloc[i + time_steps])
            return np.array(Xs), np.array(ys)
        
        X_seq, y_seq = create_sequences(X_normalized, y_normalized)
        
        # Make predictions
        start_time = time.time()
        y_pred_normalized = model.predict(X_seq, verbose=0)
        end_time = time.time()
        prediction_runtime = int((end_time - start_time) * 1000)
        
        # Inverse transform predictions
        y_pred = scaler_y_new.inverse_transform(y_pred_normalized)
        y_actual = y.iloc[30:].values
        
        # Calculate metrics
        mae = mean_absolute_error(y_actual, y_pred)
        mape = np.mean(np.abs((y_actual - y_pred) / y_actual)) * 100
        
        # Create and save plot
        os.makedirs('./output', exist_ok=True)
        plt.figure(figsize=(15, 7))
        plt.plot(df['date'][30:], y_actual, label='Actual Price', color='blue', alpha=0.7)
        plt.plot(df['date'][30:], y_pred, label='Predicted Price', color='red', alpha=0.7)
        plt.title('Bitcoin Price: Actual vs Predicted')
        plt.xlabel('Date')
        plt.ylabel('Price ($)')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('./output/prediction_plot.png')
        plt.close()
        
        return {
            'mae': float(mae),
            'mape': float(mape),
            'runtime': prediction_runtime,
            'pred_list': y_pred.flatten().tolist(),
            'actual_prices': y_actual.flatten().tolist()
        }
        
    except Exception as e:
        return {
            'error': f"Error during prediction: {str(e)}"
        }
        # print(f"Error during prediction: {str(e)}")
        # return None

# Test code 
'''
if __name__ == "__main__":
    start_date = '2023-12-01'
    end_date = '2024-01-31'
    results = predict_bitcoin_prices(start_date, end_date)
    
    if results:
        print(f"MAE: ${results['mae']:.2f}")
        print(f"MAPE: {results['mape']:.2f}%")
        print(f"Runtime: {results['runtime']} ms")
        print(f"Number of predictions: {len(results['pred_list'])}")
        print("Plot saved as 'prediction_plot.png' in output directory")
'''