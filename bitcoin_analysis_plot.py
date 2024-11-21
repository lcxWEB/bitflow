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
    - MAE values: Format: {"AlgorithmName": float (3 decimal places, e.g., 12345.678), ...}
    - Runtime values: Format: {"AlgorithmName": int (milliseconds, e.g., 2300), ...}
    - MAPE values: Format: {"AlgorithmName": [float (3 decimal places, percentage, e.g., 53.333), ...], ...}

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

# Define the chart output directory
PLOTS_DIR = "/frontend/bitflow-frontend/public/static/plots/"
os.makedirs(PLOTS_DIR, exist_ok=True)  # Create the directory if it doesn't exist

# Supported algorithms
EXPECTED_ALGORITHMS = {"ARIMA", "XGBoost", "LSTM", "RandomForest", "Prophet"}

def fetch_actual_prices_with_retry(start_date, end_date, retries=3, delay=5):
    """
    Fetch actual Bitcoin prices from the CryptoCompare API with a retry mechanism.

    Args:
        start_date (str): Start date in "YYYY-MM-DD" format.
        end_date (str): End date in "YYYY-MM-DD" format.
        retries (int): Number of retry attempts.
        delay (int): Delay in seconds between retries.

    Returns:
        dict: Actual prices as a dictionary with date keys and price values.

    Raises:
        Exception: If all retry attempts fail.
    """
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
    """
    Fetch actual Bitcoin prices from the CryptoCompare API.

    Args:
        start_date (str): Start date in "YYYY-MM-DD" format.
        end_date (str): End date in "YYYY-MM-DD" format.

    Returns:
        dict: Actual prices as a dictionary with date keys and price values.

    Raises:
        Exception: If the API request fails.
    """
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

def validate_input(data, expected_type, description):
    """
    Validate the input data type.

    Args:
        data: The input data to validate.
        expected_type (type): The expected type of the data.
        description (str): Description of the input for error messages.

    Raises:
        ValueError: If the data type does not match the expected type.
    """
    if not isinstance(data, expected_type):
        raise ValueError(f"{description} should be of type {expected_type}. Got: {type(data)}")
    if isinstance(data, dict) and not data:
        raise ValueError(f"{description} should not be empty.")

def validate_algorithm_names(data, description):
    """
    Validate that all algorithm names in the input are supported.

    Args:
        data (dict): Dictionary with algorithm names as keys.
        description (str): Description of the input for error messages.

    Raises:
        ValueError: If any algorithm name is not supported.
    """
    if not all(algo in EXPECTED_ALGORITHMS for algo in data.keys()):
        raise ValueError(f"{description} contains unexpected algorithm names. Expected: {EXPECTED_ALGORITHMS}")

def validate_float_precision(value, decimal_places=3, description="float value"):
    """
    Validate the precision of a float value.

    Args:
        value (float): The float value to validate.
        decimal_places (int): The required number of decimal places.
        description (str): Description of the input for error messages.

    Raises:
        ValueError: If the value is not a float or does not match the precision.
    """
    if not isinstance(value, float):
        raise ValueError(f"{description} should be a float. Got: {type(value)}")
    if round(value, decimal_places) != value:
        raise ValueError(f"{description} should have at most {decimal_places} decimal places. Got: {value}")

def plot_trend_chart(predict_dictionary, actual_prices, output_name="trend_chart.png"):
    """
    Generate a trend line chart comparing predicted and actual prices.

    Args:
        predict_dictionary (dict): Predicted prices for each algorithm.
        actual_prices (dict): Actual Bitcoin prices.
        output_name (str): Name of the output file.

    Returns:
        str: The file path of the saved chart.

    Raises:
        ValueError: If input data is invalid.
    """
    validate_input(predict_dictionary, dict, "Predicted prices dictionary")
    validate_input(actual_prices, dict, "Actual prices dictionary")
    validate_algorithm_names(predict_dictionary, "Predicted prices dictionary")

    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    for algo, data in predict_dictionary.items():
        if not isinstance(data, dict):
            raise ValueError(f"Each algorithm's data in predicted prices should be a dictionary. Got: {type(data)}")
        dates = list(data.keys())
        prices = list(data.values())
        plt.plot(dates, prices, label=f"Predicted by {algo}")

    # Add actual prices
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
    """
    Generate a bar chart comparing Mean Absolute Error (MAE) across algorithms.

    Args:
        mae_list (dict): A dictionary with algorithm names as keys and MAE values as floats (3 decimal places).
        output_name (str): Name of the output file.

    Returns:
        str: The file path of the saved chart.

    Raises:
        ValueError: If input data is invalid or precision requirements are not met.
    """
    validate_input(mae_list, dict, "MAE values dictionary")
    validate_algorithm_names(mae_list, "MAE values dictionary")
    for value in mae_list.values():
        validate_float_precision(value, 3, "MAE value")

    sns.set(style="whitegrid")
    data = pd.DataFrame(list(mae_list.items()), columns=["Algorithm", "MAE"])
    ax = sns.barplot(x="Algorithm", y="MAE", data=data, palette="coolwarm")

    # Add value labels
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
    """
    Generate a bar chart comparing runtime efficiency of algorithms.

    Args:
        runtime_list (dict): A dictionary with algorithm names as keys and runtime values as integers (milliseconds).
        output_name (str): Name of the output file.

    Returns:
        str: The file path of the saved chart.

    Raises:
        ValueError: If input data is invalid.
    """
    validate_input(runtime_list, dict, "Runtime values dictionary")
    validate_algorithm_names(runtime_list, "Runtime values dictionary")
    for value in runtime_list.values():
        if not isinstance(value, int):
            raise ValueError(f"Each runtime value should be an int. Got: {type(value)}")

    sns.set(style="whitegrid")
    data = pd.DataFrame(list(runtime_list.items()), columns=["Algorithm", "Runtime"])
    ax = sns.barplot(x="Algorithm", y="Runtime", data=data, palette="Greens")

    # Add value labels
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
    """
    Generate a dynamic error line chart showing MAPE trends for each algorithm.

    Args:
        mape_list (dict): A dictionary with algorithm names as keys and lists of MAPE values (floats, 3 decimal places).
        output_name (str): Name of the output file.

    Returns:
        str: The file path of the saved chart.

    Raises:
        ValueError: If input data is invalid or precision requirements are not met.
    """
    validate_input(mape_list, dict, "MAPE values dictionary")
    validate_algorithm_names(mape_list, "MAPE values dictionary")
    for algo, values in mape_list.items():
        for value in values:
            validate_float_precision(value, 3, "MAPE trend value")

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