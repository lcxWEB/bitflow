# LSTM/utils/init_path.py
import sys
import os

def load_data(data_type: str):
    # Get file path
    file_path = DataConfig.DATA_PATHS[f'{data_type}_data']
    
    # Read data
    df = pd.read_csv(file_path)
    print(f"Loaded {data_type} data")
    return df