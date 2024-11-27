import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

// const Container = styled.div`
//   background: white;
//   padding: 1.5rem;
//   border-radius: 8px;
//   box-shadow: 0 2px 4px rgba(0,0,0,0.1);
// `;

const StyledH2 = styled.h2`
  text-align: left;
  margin-left: 0;
  padding-left: 0;
  font-weight: bold; 
`;

const DatePickerContainer = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  margin-top: 1rem;
  
  .react-datepicker-wrapper {
    width: auto;
  }
  
  input {
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    width: 130px;
  }
`;

const PredictButton = styled.button`
  background-color: #0070f3;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  margin-left: 1rem;

  &:hover {
    background-color: #0051a2;
  }
`;

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

const FlexContainer = styled.div`
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  gap: 2rem;
  & > div:first-child {
    flex: 2;
  }
  & > div:last-child {
    flex: 1;
  }
`;

const ImageContainer = styled.div`
  margin-bottom: 2rem; /* 增加底部外边距 */
`;

const PredictPerformance = () => {
  const [startDate, setStartDate] = useState<Date | undefined>(undefined);
  const [endDate, setEndDate] = useState<Date | undefined>(undefined);
  const [chart1Src, setChart1Src] = useState<string>('/static/plots/trend_chart.png');
  const [chart2Src, setChart2Src] = useState<string>('/static/plots/error_bar_chart.png');
  const [chart3Src, setChart3Src] = useState<string>('/static/plots/runtime_bar_chart.png');
  const [chart4Src, setChart4Src] = useState<string>('/static/plots/mape_bar_chart.png');
  const [selectedModel, setSelectedModel] = useState('RandomForest');
  const [data, setData] = useState<any>(null);
  const [isPredicting, setIsPredicting] = useState(false);

  const handlePredict = async () => {
    if (!startDate || !endDate) {
      alert('Please select both start and end dates.');
      return;
    }
    setIsPredicting(true);

    const startTimestamp = Math.floor(startDate.getTime() / 1000);
    const endTimestamp = Math.floor(endDate.getTime() / 1000);

    try {
      const response = await fetch(`http://127.0.0.1:5000/predict_plot?startDate=${startTimestamp}&endDate=${endTimestamp}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

    //   if (!response.ok) {
    //     throw new Error('Network response was not ok');
    //   }

      const result = await response.json();
      console.log("predic_plot result: ", result);
      setData(result.results);
      setChart1Src(data.priceChart.substring(data.priceChart.indexOf("/static")));
      setChart2Src(data.MAEChart.substring(data.MAEChart.indexOf("/static")));
      setChart3Src(data.RuntimeChart.substring(data.RuntimeChart.indexOf("/static")));
      setChart4Src(data.MAPEChart.substring(data.MAPEChart.indexOf("/static")));
    } catch (error) {
      console.error('Error fetching data:', error);
      setIsPredicting(false);
    }
  };

  const modelData = data ? data[selectedModel] : null;
  console.log(modelData);
  const { rating, finalScore } = modelData ? calculateCryptoRating(modelData.mae, modelData.mape) : { rating: '', finalScore: 0 };

  return (
    // <Container>
      <FlexContainer>
        <div>
          <StyledH2>Predict Results Compare</StyledH2>
          
          <DatePickerContainer>
            <div>
              <label>PredictDate</label>
              <DatePicker
                selected={startDate}
                onChange={(date) => setStartDate(date ?? undefined)}
                selectsStart
                startDate={startDate}
                endDate={endDate}
                placeholderText="Start date"
              />
            </div>
            
            <div>To</div>
            
            <div>
              <DatePicker
                selected={endDate}
                onChange={(date) => setEndDate(date ?? undefined)}
                selectsEnd
                startDate={startDate}
                endDate={endDate}
                minDate={startDate}
                placeholderText="End date"
              />
            </div>
            <PredictButton onClick={handlePredict} disabled={isPredicting}>Predict</PredictButton>
          </DatePickerContainer>

          <ImageContainer>
            <img src={chart1Src} alt="Chart 1: Trend Line Chart" />
            {/* <p>Chart 1: Trend Line Chart: Visualizes predicted vs. actual prices</p> */}
          </ImageContainer>

          <ImageContainer>
            <img src={chart2Src} alt="Chart 2: Error Bar Chart" />
            {/* <p>Chart 2: Error Bar Chart: Shows MAE for accuracy comparison</p> */}
          </ImageContainer>

          <ImageContainer>
            <img src={chart3Src} alt="Chart 3: Runtime Bar Chart" />
            {/* <p>Chart 3: Runtime Bar Chart: Displays efficiency of each algorithm</p> */}
          </ImageContainer>

          <ImageContainer>
            <img src={chart4Src} alt="Chart 4: Dynamic Error Line Chart" />
            {/* <p>Chart 4: Dynamic Error Line Chart: Shows MAPE trends over time</p> */}
          </ImageContainer>
        </div>
        
        <div>
          <select
            id="models"
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 mb-4"
            value={selectedModel}
            onChange={(event) => setSelectedModel(event.target.value)}
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
      </FlexContainer>
    // </Container>
  );
};

export default PredictPerformance;