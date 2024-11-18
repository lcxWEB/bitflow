import { useState } from 'react';
import styled from 'styled-components';
import ProjectDescription from '../components/ProjectDescription';
import PredictResults from '../components/PredictResults';
import PerformanceCard from '../components/PerformanceCard';

const PageContainer = styled.div`
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
`;

const ContentLayout = styled.div`
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 2rem;
  margin-top: 2rem;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const PredictionPage = () => {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [selectedModel, setSelectedModel] = useState('LSTM');
  
  const projectData = {
    name: 'Bitcoin Price Prediction',
    group: '16',
    trainingStartDate: '2012/01/01',
    trainingEndDate: '2024/10/03',
    trainingFeatures: 'Bitcoin historical daily close prices, Twitter sentiment scores',
    predictTarget: 'Daily Bitcoin closing price prediction',
    models: ['LSTM', 'Prophet', 'XGBoost', 'Random Forest', 'Arima'],
    members: ['Chunxia Li', 'Xingqiao Man', 'Kai Wang', 'Yifan She', 'Zhifeng Qi'],
  };

  const performanceData = {
    model: 'LSTM',
    overallScore: 64.5,
    mae: 500,
    mape: 1.3,
    runtime: -0.560,
  };

  return (
    <PageContainer>
      <ProjectDescription data={projectData} />
      <ContentLayout>
        <PredictResults selectedModel={selectedModel} />
        <PerformanceCard data={performanceData} />
      </ContentLayout>
    </PageContainer>
  );
};

export default PredictionPage;