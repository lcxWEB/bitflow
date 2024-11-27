from flask import Flask, request, jsonify
import sys
import pandas as pd
import os
import joblib
import bitcoin_analysis_plot as bap

# 修复 Matplotlib GUI 错误
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端

# 确保项目根目录加入 sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))  # 当前脚本所在目录
project_root = os.path.join(current_dir, '.')  # 项目根目录
sys.path.append(project_root)  # 将根目录加入 sys.path

from bitcoin_prediction.XGBoost.xgboost_function import predict_prices as xgb_predict_prices # 调用你的 XGBoost function

"""
- Must use Python 3.10 or higher in order to import tensorflow
- Must install tensorflow 2.16.2
"""
from bitcoin_prediction.LSTM.LSTM_function import predict_bitcoin_prices as lstm_predict_prices
from bitcoin_prediction.framework.arima_function import predict_prices as arima_predict_prices
from bitcoin_prediction.framework.prophet_function import predict as prophet_predict_prices
from bitcoin_prediction.random_forest.random_forest_function import predict as random_forest_predict_prices

# Initialize Flask app
app = Flask(__name__)

# Load the xgboost model
def load_xgboost_model():
    xgboost_model_path = os.path.join(os.path.dirname(__file__), 'bitcoin_prediction', 'framework', 'arima_model.pkl')
    if not os.path.exists(xgboost_model_path):
        raise FileNotFoundError(f"xgboost model file not found at {xgboost_model_path}")
    with open(xgboost_model_path, 'rb') as file:
        xgboost_model = joblib.load(file)
    return xgboost_model

# Load the arima model
def load_arima_model():
    arima_model_path = os.path.join(os.path.dirname(__file__), 'bitcoin_prediction', 'framework', 'arima_model.pkl')
    if not os.path.exists(arima_model_path):
        raise FileNotFoundError(f"ARIMA model file not found at {arima_model_path}")
    with open(arima_model_path, 'rb') as file:
        arima_model = joblib.load(file)
    return arima_model

# Load the Random Forest model
def load_rf_model():
    rf_model_path = os.path.join(os.path.dirname(__file__), 'bitcoin_prediction', 'random_forest', 'rf_model.pkl')
    rf_model = joblib.load(rf_model_path)
    return rf_model

# Main prediction function
# Must use model_name: "XGBoost", "LSTM", "ARIMA", "Prophet", "RandomForest". Case sensitive.
def predict_model(model_name, start_date, end_date):
    if model_name == 'XGBoost':
        # Call the XGBoost function
        xgb_result = xgb_predict_prices(start_date, end_date)
        xgb_runtime = xgb_result['runtime']
        xgb_pred_list = [
            {"date": str(row["Date"]), "price": f"{row['Predicted_Price']:.2f}"}
            for _, row in xgb_result['predictions'].iterrows()
        ]
        xgb_mae = xgb_result['mae']
        xgb_mape = xgb_result['mape']
        
        # Combine all results into a single dictionary
        xgb_prediction_result = {
            "model_name": model_name,
            "runtime": xgb_runtime,
            "mae": f"{xgb_mae:.2f}",
            "mape": f"{xgb_mape:.2f}",
            "pred_list": xgb_pred_list
        }
        return xgb_prediction_result
    elif model_name == 'LSTM':
        # Call the LSTM function
        lstm_result = lstm_predict_prices(start_date, end_date)

        # 检查是否存在错误
        if 'error' in lstm_result:
            return {
                "model_name": model_name,
                "error": lstm_result['error']
            }

        lstm_runtime = lstm_result['runtime']
        lstm_pred_list_raw = lstm_result['pred_list']  # No date
        lstm_mae = lstm_result['mae']
        lstm_mape = lstm_result['mape']
        
        # 获取预测对应的日期范围
        # 确保 prediction_dates 的长度与 lstm_pred_list_raw 一致
        prediction_dates = pd.date_range(start=start_date, periods=len(lstm_pred_list_raw), freq='D')

        # 格式化预测结果，添加日期信息
        lstm_pred_list = [
            {"date": str(date), "price": f"{price:.2f}"}
            for date, price in zip(prediction_dates, lstm_pred_list_raw)
        ]

        # Combine all results into a single dictionary
        lstm_prediction_result = {
            "model_name": model_name,
            "runtime": lstm_runtime,
            "mae": f"{lstm_mae:.2f}",
            "mape": f"{lstm_mape:.2f}",
            "pred_list": lstm_pred_list
        }
        return lstm_prediction_result
    elif model_name == 'ARIMA':
        # Call the ARIMA function
        arima_result = arima_predict_prices(start_date, end_date)
        arima_runtime = arima_result['runtime']
        arima_pred_list = [
            {"date": str(item[0]), "price": f"{item[1]:.2f}"}
            for item in arima_result['pred_list']
        ]
        arima_mae = arima_result['mae']
        arima_mape = arima_result['mape']
        
        # Combine all results into a single dictionary
        arima_prediction_result = {
            "model_name": model_name,
            "runtime": arima_runtime,
            "mae": f"{arima_mae:.2f}",
            "mape": f"{arima_mape:.2f}",
            "pred_list": arima_pred_list
        }
        return arima_prediction_result
    elif model_name == 'Prophet':
        # Call the prophet function
        prophet_mae, prophet_mape, prophet_runtime, prophet_forecast_array = prophet_predict_prices(start_date, end_date)

        prophet_pred_list = [
            {"date": str(item[0]), "price": f"{item[1]:.2f}"}
            for item in prophet_forecast_array
        ]

        # Combine all results into a single dictionary
        prophet_prediction_result = {
            "model_name": model_name,
            "runtime": round(prophet_runtime),
            "mae": f"{prophet_mae:.2f}",
            "mape": f"{prophet_mape:.2f}",
            "pred_list": prophet_pred_list
        }
        return prophet_prediction_result
    elif model_name == 'RandomForest':
        # Call the randomforest function
        random_forest_mae, random_forest_mape, random_forest_runtime, random_forest_forecast_array = random_forest_predict_prices(start_date, end_date)
        # Convert predictions into the required dictionary format
        random_forest_pred_list = [
            {"date": item["date"], "price": f"{item['price']:.2f}"}
            for item in random_forest_forecast_array
        ]
        
        # Combine all results into a single dictionary
        random_forest_prediction_result = {
            "model_name": model_name,
            "runtime": random_forest_runtime,
            "mae": f"{random_forest_mae:.2f}",
            "mape": f"{random_forest_mape:.2f}",
            "pred_list": random_forest_pred_list
        }
        return random_forest_prediction_result
    else:
        raise ValueError("Unsupported model name!")


# Main prediction function for all models
def main_predict_all_models(start_date, end_date):
    models = ["XGBoost", "LSTM", "ARIMA", "Prophet", "RandomForest"]
    predict_dictionary = {}
    mae_list = {}
    runtime_list = {}
    mape_list = {}

    result_dic = {}
    for model_name in models:
        result = predict_model(model_name, start_date, end_date)
        result_dic[model_name] = result
        # Extract results for each model
        predict_dictionary[model_name] = {item["date"]: item["price"] for item in result["pred_list"]}
        mae_list[model_name] = result["mae"]
        runtime_list[model_name] = result["runtime"]
        mape_list[model_name] = [result["mape"]]  # Single MAPE value as a list

    return result_dic, predict_dictionary, mae_list, runtime_list, mape_list

# /predict: Return the result of a specific model in dictionary form
@app.route('/predict', methods=['GET'])
def predict_all_models():
    try:
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')
        
        # Validate input
        if not start_date or not end_date:
            return jsonify({"error": "startDate and endDate are required"}), 400
        
        # Ensure valid date format
        start_date = pd.to_datetime(int(start_date), unit='s').strftime('%Y-%m-%d')
        end_date = pd.to_datetime(int(end_date), unit='s').strftime('%Y-%m-%d')

        # Predict for all models
        models = ['XGBoost', 'LSTM', 'ARIMA', 'Prophet', 'RandomForest']
        results = {}
        
        for model_name in models:
            try:
                results[model_name] = predict_model(model_name, start_date, end_date)
            except Exception as e:
                results[model_name] = {"error": str(e)}

        # Return all results in the required format
        return jsonify({"results": results}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# def predict():
#     try:
#         # Get parameters from request
#         model_name = request.args.get('model')
#         start_date = request.args.get('startDate')
#         end_date = request.args.get('endDate')

#         # Validate input
#         if not model_name or not start_date or not end_date:
#             return jsonify({"error": "model, startDate, and endDate are required"}), 400

#         # Ensure start_date and end_date are in correct format
#         try:
#             start_date = pd.to_datetime(start_date).strftime('%Y-%m-%d')
#             end_date = pd.to_datetime(end_date).strftime('%Y-%m-%d')
#         except Exception:
#             return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

#         # Predict using the selected model
#         prediction_result = predict_model(model_name, start_date, end_date)

#         # Return the prediction result as a JSON response
#         return jsonify(prediction_result), 200

#     except ValueError as ve:
#         return jsonify({"error": str(ve)}), 400
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    
# # /predict_all: Return the results of all models. Each feature, like mae, is in a dictionary.
# @app.route('/predict_all', methods=['GET'])
# def predict_all():
#     try:
#         start_date = request.args.get('startDate')
#         end_date = request.args.get('endDate')

#         # Validate input
#         if not start_date or not end_date:
#             return jsonify({"error": "startDate and endDate are required"}), 400

#         # 获取实际价格
#         #actual_prices = get_actual_prices(start_date, end_date)

#         # 获取所有模型预测结果
#         predict_dictionary, mae_list, runtime_list, mape_list = predict_all_models(start_date, end_date)

#         # 返回整合后的结果
#         response = {
#             "predict_dictionary": predict_dictionary,
#             #"actual_prices": actual_prices,
#             "mae_list": mae_list,
#             "runtime_list": runtime_list,
#             "mape_list": mape_list
#         }
#         return jsonify(response), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


@app.route('/predict_plot', methods=['GET'])
def predict_plot():
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    if not start_date or not end_date:
        return jsonify({"error": "startDate and endDate are required"}), 400

    try:
        # Ensure valid date format
        start_date = pd.to_datetime(int(start_date), unit='s').strftime('%Y-%m-%d')
        end_date = pd.to_datetime(int(end_date), unit='s').strftime('%Y-%m-%d')

        result_dic, predict_dictionary, mae_list, runtime_list, mape_list = main_predict_all_models(start_date, end_date)

        trend_chart_path = bap.plot_trend_chart(predict_dictionary, bap.fetch_actual_prices_with_retry(start_date, end_date))
        error_bar_chart_path = bap.plot_error_bar_chart(mae_list)
        runtime_bar_chart_path = bap.plot_runtime_bar_chart(runtime_list)
        dynamic_error_chart_path = bap.plot_dynamic_error_line_chart(mape_list)

        return jsonify({
            "results": result_dic,
            "priceChart": trend_chart_path,
            "MAEChart": error_bar_chart_path,
            "RuntimeChart": runtime_bar_chart_path,
            "MAPEChart": dynamic_error_chart_path
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
