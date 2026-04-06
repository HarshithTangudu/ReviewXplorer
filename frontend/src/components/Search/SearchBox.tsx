import React from 'react';
import { Loader2 } from 'lucide-react';

interface SearchBoxProps {
  url: string;
  setUrl: (url: string) => void;
  onAnalyze: () => void;
  loading: boolean;
}

const SearchBox: React.FC<SearchBoxProps> = ({ url, setUrl, onAnalyze, loading }) => {
  return (
    <div className="search-box glow-border">
      <input 
        type="text" 
        placeholder="Paste Amazon, Flipkart, YouTube or Reddit link here..." 
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && onAnalyze()}
      />
      <button onClick={onAnalyze} disabled={loading}>
        {loading ? <Loader2 className="spinner-icon" /> : 'Analyze'}
      </button>
    </div>
  );
};

export default SearchBox;
