import React from 'react';

interface ChartsSectionProps {
  sentimentData: { name: string; value: number }[];
  emotionData: { name: string; value: number }[];
  colors?: string[];
}

const ChartsSection: React.FC<ChartsSectionProps> = ({ sentimentData, emotionData }) => {
  const maxSentiment = Math.max(...sentimentData.map(d => d.value), 1);
  const maxEmotion = Math.max(...emotionData.map(d => d.value), 1);

  return (
    <div className="grid-2">
      <div className="card glow-card">
        <h3>Sentiment Distribution</h3>
        <div className="simple-bar-chart">
          {sentimentData.map((item, idx) => (
            <div key={idx} className="bar-item">
              <div className="bar-label">
                <span>{item.name}</span>
                <span>{item.value}</span>
              </div>
              <div className="bar-bg">
                <div 
                  className="bar-fill" 
                  style={{ width: `${(item.value / maxSentiment) * 100}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="card glow-card">
        <h3>Emotion Breakdown</h3>
        <div className="simple-bar-chart">
          {emotionData.map((item, idx) => (
            <div key={idx} className="bar-item">
              <div className="bar-label">
                <span>{item.name}</span>
                <span>{item.value}</span>
              </div>
              <div className="bar-bg">
                <div 
                  className="bar-fill emotion-bar" 
                  style={{ width: `${(item.value / maxEmotion) * 100}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ChartsSection;
