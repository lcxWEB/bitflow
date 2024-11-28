import joblib
import os
import time
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import time
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
import numpy as np
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import utlis as utlis

def load_data():
    # read the data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "bitcoin_price_sentiment_addmean.csv")
    df = pd.read_csv(file_path)
    #df = pd.read_csv('./bitcoin_price_sentiment_addmean.csv')
    # make sure the date is in datetime format
    df['date'] = pd.to_datetime(df['date'])
    # prepare the dataframe for prophet
    prophet_df = df[['date', 'Close']].rename(columns={'date': 'ds', 'Close': 'y'})
    # prophet_df = df[['date', 'Close', 'sentiment_scores']].rename(columns={'date': 'ds', 'Close': 'y'})
    # add the features to the dataframe
    # features = ['Open', 'High', 'Low', 'Volume', 'sentiment_scores']
    features = ['sentiment_scores']
    # standardize the features
    scaler = StandardScaler()
    df[features] = scaler.fit_transform(df[features])

    # add the features to the dataframe
    for feature in features:
        prophet_df[feature] = df[feature]

    # split the data into train and test
    train_df, test_df = train_test_split(prophet_df, test_size=0.2, shuffle=False)
    return train_df, test_df, df, features


def predict(start_date, end_date):
    last_row = pd.Series({
        'sentiment_scores': 8.8205,
        'rolling_mean_7': 2.966253,
        'rolling_std_7': 5.614631
    })
    # train_df, test_df, df, features = load_data()
    features = ['sentiment_scores', 'rolling_mean_7', 'rolling_std_7']
    start_time = time.time()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_file_path = os.path.join(current_dir, "prophet_model.pkl")
    # model_file_path = "prophet_model.pkl"
    if os.path.exists(model_file_path):
        model = joblib.load(model_file_path)
    else:
        raise FileNotFoundError(f"Model file '{model_file_path}' not found. Please ensure the model is trained and saved.")

    # start_date = pd.to_datetime(start_date)
    # end_date = pd.to_datetime(end_date)
    actual_df = utlis.fetch_crypto_data(pd.to_datetime(start_date).strftime('%Y-%m-%d'), pd.to_datetime(end_date).strftime('%Y-%m-%d'))
    actual_price = actual_df['Close'].values  # Ensure it is a numpy array

    future_dates = pd.date_range(start=start_date, end=end_date)
    future_df = pd.DataFrame({'ds': future_dates})
    # print(future_dates)
    # 为未来日期添加特征值
    # 这里我们使用最后一个已知的值，你可能需要根据实际情况调整这个逻辑
    for feature in features:
        future_df[feature] = last_row[feature]
    # 进行预测
    forecast = model.predict(future_df)
    predicted_price = forecast['yhat'].values  # Extract predicted values as numpy array

    mae = mean_absolute_error(predicted_price, actual_price)
    mape = mean_absolute_percentage_error(predicted_price, actual_price) * 100

    # read the prediction result
    forecast_filtered = forecast[['ds', 'yhat']]
    # print(forecast_filtered)
    forecast_array = list(zip(forecast_filtered['ds'].tolist(), forecast_filtered['yhat'].tolist()))
    # print(forecast_array)
    end_time = time.time()
    runtime = (end_time - start_time) * 1000
    # print(f'Runtime: {runtime:.0f} milliseconds')
    print(f'MAE: {mae}')
    print(f'MAPE: {mape}')

    return mae, mape, runtime, forecast_array

def main():
    start_date = '2024-10-20'
    end_date = '2024-11-10'
    predict(start_date, end_date)

if __name__ == '__main__':
    main()