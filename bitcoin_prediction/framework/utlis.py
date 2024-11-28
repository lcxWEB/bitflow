import pandas as pd
from datetime import datetime
import requests


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
            "limit": days,
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
        
        # Debugging
        # print(f"Requested days: {days}, Actual returned rows: {len(df)}")
        # print(f"Fetched data: {df[['date', 'Close']].head()}")

        # Ensure data length matches the requested range
        df = df[-days:]  # Only keep the last 'days' rows, if extra data is returned
        
        # Fill or align data to match requested date range
        expected_dates = pd.date_range(start_date, end_date)
        df = df.set_index('date').reindex(expected_dates, method='nearest').reset_index()

        return df