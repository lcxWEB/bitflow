import { useState } from 'react';
import styled from 'styled-components';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

// 注册 ChartJS 组件
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

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

const ChartContainer = styled.div`
  margin-bottom: 2rem;
`;

interface PredictResultsProps {
  selectedModel: string;
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const PredictResults = ({ selectedModel }: PredictResultsProps) => {

  const [startDate, setStartDate] = useState<Date | undefined>(undefined);

  const [endDate, setEndDate] = useState<Date | undefined>(undefined);

//   const [startDate, setStartDate] = useState<Date | null>(null);
//   const [endDate, setEndDate] = useState<Date | null>(null);

  // 模拟数据 - 实际项目中应该从API获取
  const chartData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Predicted Price',
        data: [65000, 68000, 67000, 69000, 71000, 72000],
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
      {
        label: 'Actual Price',
        data: [64500, 67800, 66500, 69200, 70800, 71500],
        borderColor: 'rgb(255, 99, 132)',
        tension: 0.1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Bitcoin Price Prediction vs Actual',
      },
    },
    scales: {
      y: {
        beginAtZero: false,
      },
    },
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
      </DatePickerContainer>

      <ChartContainer>
        <Line data={chartData} options={chartOptions} />
      </ChartContainer>

      {/* 额外的图表可以在这里添加 */}
      <div>
        <ul>
          <li>Chart 1: Trend Line Chart: Visualizes predicted vs. actual prices</li>
          <li>Chart 2-4:</li>
          <li>Error Bar Chart: Shows MAE for accuracy comparison</li>
          <li>Runtime Bar Chart: Displays efficiency of each algorithm</li>
          <li>Dynamic Error Line Chart: Shows MAPE trends over time</li>
        </ul>
      </div>
    </Container>
  );
};

export default PredictResults;