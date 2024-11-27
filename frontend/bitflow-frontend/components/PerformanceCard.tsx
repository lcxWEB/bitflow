/* eslint-disable @typescript-eslint/no-unused-vars */
/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

const Card = styled.div`
  border: 1px dashed #ccc;
  border-radius: 8px;
  padding: 1.5rem;
`;

const ModelName = styled.div`
  text-align: right;
  color: #f44336;
  font-size: 0.875rem;
  margin-bottom: 1rem;
`;

const Grade = styled.div`
  text-align: center;
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
`;

const Performance = styled.div`
  text-align: center;
  font-style: italic;
  margin-bottom: 1rem;
`;

const Score = styled.div`
  text-align: center;
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 2rem;
`;

const MetricBox = styled.div<{ background: string }>`
  background: ${props => props.background};
  padding: 1rem;
  margin: 0.5rem 0;
  border-radius: 4px;
`;

const MetricLabel = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  
  span:first-child {
    font-weight: bold;
  }
  
  span:last-child {
    cursor: help;
  }
`;

const MetricValue = styled.div`
  font-size: 1.25rem;
  font-weight: bold;
`;

interface PerformanceCardProps {
  startDate: Date | undefined;
  endDate: Date | undefined;
}


const calculateCryptoRating = (mae: number, mape: number): { rating: string, finalScore: number } => {
  let maeScore: number;
  let mapeScore: number;

  if (mae <= 100) {
    maeScore = 100;
  } else if (mae <= 500) {
    maeScore = 90 - (mae - 100) * (10 / 400);
  } else if (mae <= 1000) {
    maeScore = 80 - (mae - 500) * (10 / 500);
  } else if (mae <= 2000) {
    maeScore = 70 - (mae - 1000) * (10 / 1000);
  } else if (mae <= 5000) {
    maeScore = 60 - (mae - 2000) * (20 / 3000);
  } else {
    maeScore = Math.max(0, 40 - (mae - 5000) * (40 / 5000));
  }

  if (mape <= 1) {
    mapeScore = 100;
  } else if (mape <= 3) {
    mapeScore = 90 - (mape - 1) * (10 / 2);
  } else if (mape <= 5) {
    mapeScore = 80 - (mape - 3) * (10 / 2);
  } else if (mape <= 10) {
    mapeScore = 70 - (mape - 5) * (10 / 5);
  } else if (mape <= 20) {
    mapeScore = 60 - (mape - 10) * (20 / 10);
  } else {
    mapeScore = Math.max(0, 40 - (mape - 20) * (40 / 20));
  }

  const finalScore = maeScore * 0.4 + mapeScore * 0.6;

  let rating: string;
  if (finalScore >= 95) {
    rating = 'A+';
  } else if (finalScore >= 90) {
    rating = 'A';
  } else if (finalScore >= 85) {
    rating = 'A-';
  } else if (finalScore >= 80) {
    rating = 'B+';
  } else if (finalScore >= 75) {
    rating = 'B';
  } else if (finalScore >= 70) {
    rating = 'B-';
  } else if (finalScore >= 65) {
    rating = 'C+';
  } else if (finalScore >= 60) {
    rating = 'C';
  } else if (finalScore >= 55) {
    rating = 'C-';
  } else if (finalScore >= 50) {
    rating = 'D+';
  } else if (finalScore >= 45) {
    rating = 'D';
  } else {
    rating = 'D-';
  }

  return { rating, finalScore };
};

const PerformanceCard = ({ startDate, endDate }: PerformanceCardProps) => {
  const [selectedModel, setSelectedModel] = useState('RandomForest');
  const [data, setData] = useState<any>(null);

  const handleSelectChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedModel(event.target.value);
  };


  useEffect(() => {
    if (!startDate || !endDate) return;

    const startTimestamp = startDate.getTime();
    const endTimestamp = endDate.getTime();

    // 在页面加载时调用接口
    const fetchData = async () => {
      try {
        // const response = await fetch('http://localhost:5050/predict'); // 替换为你的接口URL
        // const response = await fetch(`http://localhost:5050/predict?startDate=${startTimestamp}&endDate=${endTimestamp}`, {
        //   method: 'GET',
        //   headers: {
        //     'Content-Type': 'application/json',
        //   },
        // });
        // if (!response.ok) {
        //   throw new Error('Network response was not ok');
        // }

        // const result = await response.json();
        // mock data
        const result =  { "results": { "RandomForest": { "runtime": 2300, "mae": 150.25, "mape": 0.12, "pred_list": [ {"date": "2024-11-01", "price": 35000.75}, {"date": "2024-11-02", "price": 35210.89} ] }, "LSTM": { "runtime": 3200, "mae": 140.55, "mape": 0.10, "pred_list": [ {"date": "2024-11-01", "price": 35100.00}, {"date": "2024-11-02", "price": 35300.89} ] }, "ARIMA": { "runtime": 1800, "mae": 160.75, "mape": 0.13, "pred_list": [ {"date": "2024-11-01", "price": 34980.45}, {"date": "2024-11-02", "price": 35050.00} ] }, "xgBoost": { "runtime": 2500, "mae": 145.50, "mape": 0.11, "pred_list": [ {"date": "2024-11-01", "price": 35220.55}, {"date": "2024-11-02", "price": 35400.33} ] }, "Prophet": { "runtime": 2700, "mae": 135.20, "mape": 0.09, "pred_list": [ {"date": "2024-11-01", "price": 35300.45}, {"date": "2024-11-02", "price": 35500.75} ] } } }
        setData(result.results);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []); // 空数组作为依赖项，表示只在组件挂载时执行一次

  const modelData = data ? data[selectedModel] : null;
  const { rating, finalScore } = modelData ? calculateCryptoRating(modelData.mae, modelData.mape) : { rating: '', finalScore: 0 };

  return (
    <div>
      <select
        id="models"
        className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 mb-4"
        value={selectedModel}
        onChange={handleSelectChange}
      >
        <option value="RandomForest">Random Forest</option>
        <option value="LSTM">LSTM</option>
        <option value="ARIMA">ARIMA</option>
        <option value="XGBoost">XGBoost</option>
        <option value="Prophet">Prophet</option>
      </select>
      
      {modelData && (
        <Card>
          <ModelName>{selectedModel}</ModelName>
          <Grade>{rating}</Grade>
          <Performance>Average Performance</Performance>
          <Score>Overall Score: {finalScore.toFixed(3)}/100</Score>
          
          <MetricBox background="#f3e5f5">
            <MetricLabel>
              <span>MAE</span>
              <span>ⓘ</span>
            </MetricLabel>
            <MetricValue>{modelData.mae}</MetricValue>
          </MetricBox>
          
          <MetricBox background="#e8f5e9">
            <MetricLabel>
              <span>MAPE</span>
              <span>ⓘ</span>
            </MetricLabel>
            <MetricValue>{modelData.mape}%</MetricValue>
          </MetricBox>
          
          <MetricBox background="#e3f2fd">
            <MetricLabel>
              <span>Runtime</span>
              <span>ⓘ</span>
            </MetricLabel>
            <MetricValue>{modelData.runtime}</MetricValue>
          </MetricBox>
        </Card>
      )}
    </div>
  );
};

export default PerformanceCard;