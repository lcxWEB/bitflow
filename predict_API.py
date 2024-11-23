from flask import Flask, request, jsonify
import sys
import pandas as pd
import os
import joblib

# 确保项目根目录加入 sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))  # 当前脚本所在目录
project_root = os.path.join(current_dir, '.')  # 项目根目录
sys.path.append(project_root)  # 将根目录加入 sys.path

from bitcoin_prediction.XGBoost.xgboost_function import predict_prices as xgb_predict_prices # 调用你的 XGBoost function

# Must use Python 3.10 or higher in order to import tensorflow
from bitcoin_prediction.LSTM.LSTM_function import predict_bitcoin_prices as lstm_predict_prices
from bitcoin_prediction.framework.arima_function import predict_prices as arima_predict_prices
from bitcoin_prediction.framework.prophet_function import predict as prophet_predict_prices
from bitcoin_prediction.random_forest.random_forest_function import predict_bitcoin_prices as random_forest_predict_prices
from bitcoin_prediction.random_forest.random_forest_function import main as random_forest_main

# Initialize Flask app
app = Flask(__name__)

# Load the Random Forest model
def load_rf_model():
    rf_model_path = os.path.join(os.path.dirname(__file__), 'RandomForest', 'rf_model.pkl')
    rf_model = joblib.load(rf_model_path)
    return rf_model

# Main prediction function
# Must use model_name: "xgboost", "lstm", "arima", "prophet", "randomforest". Case sensitive.
def predict_model(model_name, start_date, end_date):
    if model_name == 'xgboost':
        # Call the XGBoost function
        xgb_result = xgb_predict_prices(start_date, end_date)
        xgb_runtime = xgb_result['runtime']
        xgb_pred_list = xgb_result['predictions'].to_dict(orient='records')
        xgb_mae = xgb_result['mae']
        xgb_mape = xgb_result['mape']
        
        # Combine all results into a single dictionary
        xgb_prediction_result = {
            "model_name": model_name,
            "runtime": xgb_runtime,
            "mae": xgb_mae,
            "mape": xgb_mape,
            "pred_list": xgb_pred_list
        }
        return xgb_prediction_result
    elif model_name == 'lstm':
        # Call the LSTM function
        lstm_result = lstm_predict_prices(start_date, end_date)
        lstm_runtime = lstm_result['runtime']
        lstm_pred_list = lstm_result['pred_list'].to_dict(orient='records')
        lstm_mae = lstm_result['mae']
        lstm_mape = lstm_result['mape']
        
        # Combine all results into a single dictionary
        lstm_prediction_result = {
            "model_name": model_name,
            "runtime": lstm_runtime,
            "mae": lstm_mae,
            "mape": lstm_mape,
            "pred_list": lstm_pred_list
        }
        return lstm_prediction_result
    elif model_name == 'arima':
        # Call the ARIMA function
        arima_result = arima_predict_prices(start_date, end_date)
        arima_runtime = arima_result['runtime']
        arima_pred_list = arima_result['pred_list'].to_dict(orient='records')
        arima_mae = arima_result['mae']
        arima_mape = arima_result['mape']
        
        # Combine all results into a single dictionary
        arima_prediction_result = {
            "model_name": model_name,
            "runtime": arima_runtime,
            "mae": arima_mae,
            "mape": arima_mape,
            "pred_list": arima_pred_list
        }
        return arima_prediction_result
    elif model_name == 'prophet':
        # Call the prophet function
        prophet_mae, prophet_mape, prophet_runtime, prophet_forecast_array = prophet_predict_prices(start_date, end_date)

        # 将预测结果转为 DataFrame，再转为字典格式
        prophet_pred_list = [{'Date': date, 'Predicted_Price': price} for date, price in prophet_forecast_array]

        # Combine all results into a single dictionary
        prophet_prediction_result = {
            "model_name": model_name,
            "runtime": prophet_runtime,
            "mae": prophet_mae,
            "mape": prophet_mape,
            "pred_list": prophet_pred_list
        }
        return prophet_prediction_result
    elif model_name == 'randomforest':
        # Call the randomforest function
        rf_model = load_rf_model()
        random_forest_result = random_forest_predict_prices(rf_model, start_date, end_date)
        # 生成日期范围
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        random_forest_result_main = random_forest_main()
        random_forest_runtime = random_forest_result_main['runtime']
        random_forest_pred_list = pd.Series(random_forest_result['predicted_prices'], index=dates).to_dict()
        random_forest_mae = random_forest_result_main['mae']
        random_forest_mape = random_forest_result_main['mape']
        
        # Combine all results into a single dictionary
        random_forest_prediction_result = {
            "model_name": model_name,
            "runtime": random_forest_runtime,
            "mae": random_forest_mae,
            "mape": random_forest_mape,
            "pred_list": random_forest_pred_list
        }
        return random_forest_prediction_result
    else:
        raise ValueError("Unsupported model name!")


# Main prediction function for all models
def predict_all_models(start_date, end_date):
    models = ["xgboost", "lstm", "arima", "prophet", "randomforest"]
    predict_dictionary = {}
    mae_list = {}
    runtime_list = {}
    mape_list = {}

    for model_name in models:
        result = predict_model(model_name, start_date, end_date)

        # Extract results for each model
        predict_dictionary[model_name] = {item["Date"]: item["Predicted_Price"] for item in result["pred_list"]}
        mae_list[model_name] = result["mae"]
        runtime_list[model_name] = result["runtime"]
        mape_list[model_name] = [result["mape"]]  # Single MAPE value as a list

    return predict_dictionary, mae_list, runtime_list, mape_list

# /predict: Return the result of a specific model in dictionary form
@app.route('/predict', methods=['GET'])
def predict():
    try:
        # Get parameters from request
        model_name = request.args.get('model')
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')

        # Validate input
        if not model_name or not start_date or not end_date:
            return jsonify({"error": "model, startDate, and endDate are required"}), 400

        # Ensure start_date and end_date are in correct format
        try:
            start_date = pd.to_datetime(start_date).strftime('%Y-%m-%d')
            end_date = pd.to_datetime(end_date).strftime('%Y-%m-%d')
        except Exception:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

        # Predict using the selected model
        prediction_result = predict_model(model_name, start_date, end_date)

        # Return the prediction result as a JSON response
        return jsonify(prediction_result), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# /predict_all: Return the results of all models. Each feature, like mae, is in a dictionary.
@app.route('/predict_all', methods=['GET'])
def predict_all():
    try:
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')

        # Validate input
        if not start_date or not end_date:
            return jsonify({"error": "startDate and endDate are required"}), 400

        # 获取实际价格
        #actual_prices = get_actual_prices(start_date, end_date)

        # 获取所有模型预测结果
        predict_dictionary, mae_list, runtime_list, mape_list = predict_all_models(start_date, end_date)

        # 返回整合后的结果
        response = {
            "predict_dictionary": predict_dictionary,
            #"actual_prices": actual_prices,
            "mae_list": mae_list,
            "runtime_list": runtime_list,
            "mape_list": mape_list
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
