"""
Description:
This script generates various charts for analyzing the performance of algorithms
in Bitcoin price prediction. The charts include:
1. Trend Line Chart: Predicted vs Actual Prices
2. Error Bar Chart: Comparison of MAE across algorithms
3. Runtime Bar Chart: Efficiency comparison of algorithms
4. Dynamic Error Line Chart: MAPE trends for each algorithm

Features:
- Fetches actual Bitcoin prices using the CryptoCompare API with retry mechanism.
- Generates visually enhanced charts using Seaborn and Matplotlib.

Expected Algorithms:
The following algorithms are supported for all input data:
- ARIMA
- XGBoost
- LSTM
- RandomForest
- Prophet

Usage:
1. Install required libraries: pip install matplotlib seaborn pandas requests

2. Prepare the input data:
    - Predicted prices: Format: {"AlgorithmName": {"YYYY-MM-DD": price, ...}, ...}
    - Start and end dates: Format: "YYYY-MM-DD"
    - MAE values: Format: {"AlgorithmName": float, ...}
    - Runtime values: Format: {"AlgorithmName": int, ...}
    - MAPE values: Format: {"AlgorithmName": [float, ...], ...}

3. Call the plotting functions:
    trend_chart = plot_trend_chart(predict_dict, actual_prices)
    error_chart = plot_error_bar_chart(mae_list)
    runtime_chart = plot_runtime_bar_chart(runtime_list)
    dynamic_error_chart = plot_dynamic_error_line_chart(mape_list)

4. Save the output charts to the specified directory:
    /frontend/bitflow-frontend/public/static/plots/
"""

import matplotlib.pyplot as plt
import seaborn as sns
import requests
import pandas as pd
import os
import logging
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Define the chart output directory relative to the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLOTS_DIR = os.path.join(BASE_DIR, "frontend/bitflow-frontend/public/static/plots/")
os.makedirs(PLOTS_DIR, exist_ok=True)  # Create the directory if it doesn't exist

# Supported algorithms
EXPECTED_ALGORITHMS = {"ARIMA", "XGBoost", "LSTM", "RandomForest", "Prophet"}

def fetch_actual_prices_with_retry(start_date, end_date, retries=3, delay=5):
    for attempt in range(retries):
        try:
            return fetch_actual_prices(start_date, end_date)
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                logger.error("All retry attempts failed.")
                raise

def fetch_actual_prices(start_date, end_date):
    logger.info("Fetching actual Bitcoin prices...")
    url = "https://min-api.cryptocompare.com/data/v2/histoday"
    params = {
        "fsym": "BTC",
        "tsym": "USD",
        "toTs": pd.to_datetime(end_date).timestamp(),
        "limit": (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days,
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        logger.error(f"Failed to fetch data: {response.json()}")
        raise Exception(f"Failed to fetch data: {response.json()}")

    data = response.json().get("Data", {}).get("Data", [])
    actual_prices = {pd.to_datetime(item["time"], unit="s").strftime("%Y-%m-%d"): item["close"] for item in data}
    logger.info("Successfully fetched actual prices.")
    return actual_prices

def plot_trend_chart(predict_dictionary, actual_prices, output_name="trend_chart.png"):
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    for algo, data in predict_dictionary.items():
        dates = list(data.keys())
        prices = list(data.values())
        plt.plot(dates, prices, label=f"Predicted by {algo}")

    actual_dates = list(actual_prices.keys())
    actual_values = list(actual_prices.values())
    plt.plot(actual_dates, actual_values, label="Actual Prices", linestyle="--", color="black")

    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("Trend Line Chart: Predicted vs Actual Prices")
    plt.legend()
    output_path = os.path.join(PLOTS_DIR, output_name)
    plt.savefig(output_path)
    plt.close()
    logger.info(f"Trend line chart saved at {output_path}")
    return output_path

def plot_error_bar_chart(mae_list, output_name="error_bar_chart.png"):
    sns.set(style="whitegrid")
    data = pd.DataFrame(list(mae_list.items()), columns=["Algorithm", "MAE"])
    ax = sns.barplot(x="Algorithm", y="MAE", data=data, palette="coolwarm")

    for p in ax.patches:
        ax.annotate(f"{p.get_height():.3f}", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points')

    plt.title("Error Bar Chart: MAE Comparison")
    plt.xlabel("Algorithm")
    plt.ylabel("Mean Absolute Error (MAE)")
    output_path = os.path.join(PLOTS_DIR, output_name)
    plt.savefig(output_path)
    plt.close()
    logger.info(f"Error bar chart saved at {output_path}")
    return output_path

def plot_runtime_bar_chart(runtime_list, output_name="runtime_bar_chart.png"):
    sns.set(style="whitegrid")
    data = pd.DataFrame(list(runtime_list.items()), columns=["Algorithm", "Runtime"])
    ax = sns.barplot(x="Algorithm", y="Runtime", data=data, palette="Greens")

    for p in ax.patches:
        ax.annotate(f"{p.get_height()}", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points')

    plt.title("Runtime Bar Chart: Algorithm Efficiency")
    plt.xlabel("Algorithm")
    plt.ylabel("Runtime (ms)")
    output_path = os.path.join(PLOTS_DIR, output_name)
    plt.savefig(output_path)
    plt.close()
    logger.info(f"Runtime bar chart saved at {output_path}")
    return output_path

def plot_dynamic_error_line_chart(mape_list, output_name="dynamic_error_chart.png"):
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    for algo, mape_values in mape_list.items():
        plt.plot(range(len(mape_values)), mape_values, label=f"{algo}")

    plt.xlabel("Time")
    plt.ylabel("Mean Absolute Percentage Error (MAPE)")
    plt.title("Dynamic Error Line Chart: MAPE Trends")
    plt.legend()
    output_path = os.path.join(PLOTS_DIR, output_name)
    plt.savefig(output_path)
    plt.close()
    logger.info(f"Dynamic error line chart saved at {output_path}")
    return output_path