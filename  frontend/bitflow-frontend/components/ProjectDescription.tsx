import styled from 'styled-components';

const Container = styled.div`
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
`;

const TitleContainer = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  
  h2 {
    margin: 0;  // Remove default margin
    font-weight: bold; 
  }
`;

const GroupTag = styled.span`
  background: #e8f5e9;
  color: #2e7d32;
  padding: 0.25rem 0.75rem;
  border-radius: 16px;
  font-size: 0.875rem;
`;

const Row = styled.div`
  display: flex;
  align-items: flex-start;  // 改为顶部对齐
  justify-content: flex-start;  // 改为左对齐
  gap: 20px;  // Label 和内容之间的间距
  margin-bottom: 16px;
`;

const Label = styled.div`
  min-width: 150px;  // 给 Label 一个固定宽度
  font-weight: 500;
  color: #666;
  text-align: left;  // Label 文字左对齐
`;

const ModelTags = styled.div`
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
`;

const ModelTag = styled.span<{ color: string }>`
  background: ${props => props.color};
  padding: 0.25rem 0.75rem;
  border-radius: 16px;
  font-size: 0.875rem;
`;

interface ProjectDescriptionProps {
  data: {
    name: string;
    group: string;
    trainingStartDate: string;
    trainingEndDate: string;
    trainingFeatures: string;
    predictTarget: string;
    models: string[];
    members: string[];
  };
}

const ProjectDescription = ({ data }: ProjectDescriptionProps) => {
  const getModelColor = (model: string) => {
    const colors: { [key: string]: string } = {
      LSTM: '#ffebee',
      Prophet: '#fff3e0',
      XGBoost: '#f1f8e9',
      'Random Forest': '#e3f2fd',
      Arima: '#f3e5f5',
    };
    return colors[model] || '#f5f5f5';
  };

  return (
    <Container>
      <TitleContainer>
        <h2>{data.name}</h2>
        <GroupTag>group {data.group}</GroupTag>
      </TitleContainer>
      
      <Row>
        <Label>Training Features</Label>
        <div>{data.trainingFeatures}</div>
      </Row>
      
      <Row>
        <Label>Training Date</Label>
        <div>{data.trainingStartDate} - {data.trainingEndDate}</div>
      </Row>

      <Row>
        <Label>Predict Target</Label>
        <div>{data.predictTarget}</div>
      </Row>
      
      <Row>
        <Label>Model</Label>
        <ModelTags>
          {data.models.map((model, index) => (
            <ModelTag key={index} color={getModelColor(model)}>
              {model}
            </ModelTag>
          ))}
        </ModelTags>
      </Row>
      
      <Row>
        <Label>Members</Label>
        <div>{data.members.join(', ')}</div>
      </Row>
    </Container>
  );
};

export default ProjectDescription;