import React from 'react';

interface StatsGridProps {
  platform: string;
  totalReviews: number;
  sarcasmRate: number;
}

const StatsGrid: React.FC<StatsGridProps> = ({ platform, totalReviews, sarcasmRate }) => {
  return (
    <div className="stats-grid">
      <div className="card glow-card">
        <h3>Platform</h3>
        <p className="stat-value">{platform}</p>
      </div>
      <div className="card glow-card">
        <h3>Total Reviews</h3>
        <p className="stat-value">{totalReviews}</p>
      </div>
      <div className="card glow-card">
        <h3>Sarcasm Rate</h3>
        <p className="stat-value">{sarcasmRate.toFixed(1)}%</p>
      </div>
    </div>
  );
};

export default StatsGrid;
