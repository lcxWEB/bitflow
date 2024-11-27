import styled from 'styled-components';
import ProjectDescription from '../components/ProjectDescription';
import PredictPerformance from '../components/PredictPerformance';

const PageContainer = styled.div`
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
`;

const ContentLayout = styled.div`
  width: 100%;
  max-width: 1200px;
  margin: 2rem auto 0;
`;

const PredictionPage = () => {  
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

  return (
    <PageContainer>
      <ProjectDescription data={projectData} />
      <ContentLayout>
        <PredictPerformance />
      </ContentLayout>
    </PageContainer>
  );
};

export default PredictionPage;