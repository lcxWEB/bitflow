from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib

# 创建 Flask 应用
app = Flask(__name__)

# 启用 CORS 以防其他跨域问题
CORS(app)  


# 加载预处理器和模型（你需要提前保存这些文件）
# scaler = joblib.load("rf_scaler.pkl")
model = joblib.load("rf_model.pkl")

# 加载用于查找数据的历史数据集（可以是CSV文件）
data = pd.read_csv("../bitcoin_price_sentiment.csv")
# 修正日期格式，使用正确的格式 '%Y-%m-%d'
data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
data.set_index('date', inplace=True)

@app.route('/')
def index():
    # 返回 index.html 页面
    return render_template('index.html')

@app.route('/predict', methods=['GET'])
def predict():
    date_str = request.args.get('date')
    
    try:
        # 将字符串转换为 datetime 对象
        date = pd.to_datetime(date_str)

        # 检查数据集是否包含该日期
        if date in data.index:
            # 提取特征值，并进行预测
            feature_columns = ['Open', 'High', 'Low', 'Volume', 'sentiment_scores']
            features = data.loc[date, feature_columns].values.reshape(1, -1)

            # 获取实际收盘价
            actual_close = data.loc[date, 'Close']

            # 使用模型进行预测
            predicted_close = model.predict(features)

            # 计算预测误差百分比
            error_percentage = abs(predicted_close[0] - actual_close) / actual_close * 100

            # 构建返回的 JSON 响应，确保所有的值都是标准 Python 类型
            response = {
                'date': date_str,
                'actual_close': round(float(actual_close), 2),
                'predicted_close': round(float(predicted_close[0]), 2),
                'error_percentage': round(float(error_percentage), 2)
            }
            
            print("Flask API response:", response)  # 打印调试信息
            return jsonify(response)
        else:
            return jsonify({'error': 'Date not found in historical data.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# 启动 Flask 应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)