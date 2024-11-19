import React, { useState } from 'react';
import styled from 'styled-components';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import PerformanceCard from './PerformanceCard'; // 确保导入路径正确


const Container = styled.div`
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
`;

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

interface PredictResultsProps {
  selectedModel: string;
}

const PredictResults = ({ selectedModel }: PredictResultsProps) => {
  const [startDate, setStartDate] = useState<Date | undefined>(undefined);
  const [endDate, setEndDate] = useState<Date | undefined>(undefined);
  const [chart1Src, setChart1Src] = useState<string>('../static/plots/price_chart.png');
  const [chart2Src, setChart2Src] = useState<string>('../../static/plots/mae_chart.png');
  const [chart3Src, setChart3Src] = useState<string>('../../static/plots/runtime_chart.png');
  const [chart4Src, setChart4Src] = useState<string>('../../static/plots/mape_chart.png');

  const handlePredict = async () => {
    if (!startDate || !endDate) {
      alert('Please select both start and end dates.');
      return;
    }

    try {
      const response = await fetch(`http://localhost:5050/predict_plot?startDate=${startTimestamp}&endDate=${endTimestamp}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setChart1Src(data.priceChart);
      setChart2Src(data.MAEChart);
      setChart3Src(data.RuntimeChart);
      setChart4Src(data.MAPEChart);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <Container>
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
        <PredictButton onClick={handlePredict}>Predict</PredictButton>
      </DatePickerContainer>

      <div>
        <img src={chart1Src} alt="Chart 1: Trend Line Chart" />
        <p>Chart 1: Trend Line Chart: Visualizes predicted vs. actual prices</p>
      </div>

      <div>
        <img src={chart2Src} alt="Chart 2: Error Bar Chart" />
        <p>Chart 2: Error Bar Chart: Shows MAE for accuracy comparison</p>
      </div>

      <div>
        <img src={chart3Src} alt="Chart 3: Runtime Bar Chart" />
        <p>Chart 3: Runtime Bar Chart: Displays efficiency of each algorithm</p>
      </div>

      <div>
        <img src={chart4Src} alt="Chart 4: Dynamic Error Line Chart" />
        <p>Chart 4: Dynamic Error Line Chart: Shows MAPE trends over time</p>
      </div>

      {/* <PerformanceCard startDate={startDate} endDate={endDate} /> */}

    </Container>
  );
};

export default PredictResults;