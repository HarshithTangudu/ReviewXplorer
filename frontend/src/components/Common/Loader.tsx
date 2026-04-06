import React from 'react';

const Loader: React.FC = () => {
  return (
    <div className="loader">
      <div className="spinner"></div>
      <p className="loader-text">Scraping and analyzing all reviews... This may take a minute.</p>
    </div>
  );
};

export default Loader;
