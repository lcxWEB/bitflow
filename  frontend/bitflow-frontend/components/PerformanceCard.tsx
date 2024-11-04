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
  data: {
    model: string;
    overallScore: number;
    mae: number;
    mape: number;
    runtime: number;
  };
}

const PerformanceCard = ({ data }: PerformanceCardProps) => {
  return (
    <div>
      <select id="countries" className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 mb-4">
        <option selected>Choose a country</option>
        <option value="US">United States</option>
        <option value="CA">Canada</option>
        <option value="FR">France</option>
        <option value="DE">Germany</option>
    </select>
    <Card>
      <ModelName>{data.model}</ModelName>
      <Grade>C+</Grade>
      <Performance>Average Performance</Performance>
      <Score>overall Score: {data.overallScore}/100</Score>
      
      <MetricBox background="#f3e5f5">
        <MetricLabel>
          <span>MAE</span>
          <span>ⓘ</span>
        </MetricLabel>
        <MetricValue>{data.mae}</MetricValue>
      </MetricBox>
      
      <MetricBox background="#e8f5e9">
        <MetricLabel>
          <span>MAPE</span>
          <span>ⓘ</span>
        </MetricLabel>
        <MetricValue>{data.mape}%</MetricValue>
      </MetricBox>
      
      <MetricBox background="#e3f2fd">
        <MetricLabel>
          <span>Runtime</span>
          <span>ⓘ</span>
        </MetricLabel>
        <MetricValue>{data.runtime}</MetricValue>
      </MetricBox>
    </Card>
    </div>
  );
};

export default PerformanceCard;