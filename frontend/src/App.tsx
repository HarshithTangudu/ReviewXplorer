import { useState, useMemo } from 'react';
import axios from 'axios';
import './App.css';
import { EmotionChart, EmotionRadar } from './components/Dashboard/EmotionChart';
import { SentimentGauge, SentimentTimeline } from './components/Dashboard/SentimentCharts';
import { WordCloud } from './components/Dashboard/WordCloud';

// --- Types ---
interface CommentResult {
  text: string;
  sentiment: string;
  emotion: string;
  sarcastic: boolean;
  confidence: number;
}

interface AnalysisData {
  platform: string;
  total_comments: number;
  results: CommentResult[];
  summary: {
    sentiment_distribution: Record<string, number>;
    emotion_distribution: Record<string, number>;
    sarcasm_percentage: number;
  };
}

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<AnalysisData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [sentimentFilter, setSentimentFilter] = useState('All');
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

  const handleAnalyze = async () => {
    if (!url) return;
    setLoading(true);
    setError(null);
    setData(null);
    setSentimentFilter('All');
    setCurrentPage(1);

    try {
      const response = await axios.post(`${API_BASE_URL}/analyze`, { url });
      setData(response.data);
    } catch (err: any) {
      console.error('Analysis Error:', err);
      setError(err.response?.data?.detail || 'An error occurred while analyzing the link. Please make sure the backend is running at localhost:8000.');
    } finally {
      setLoading(false);
    }
  };

  const filteredResults = useMemo(() => {
    if (!data) return [];
    if (sentimentFilter === 'All') return data.results;
    return data.results.filter((res) => res.sentiment === sentimentFilter);
  }, [data, sentimentFilter]);


  // Pagination
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentComments = filteredResults.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(filteredResults.length / itemsPerPage) || 0;
  
  return (
    <div className={`container ${!data && !loading ? 'centered' : ''}`}>
      <header className="header-animate">
        <h1>ReviewXplorer</h1>
        <p className="subtitle">Sentiment, Emotion & Sarcasm Analysis for E-commerce & Social Media</p>
      </header>

      <div className="search-box glow-border">
        <input 
          type="text" 
          placeholder="Paste Amazon, Flipkart, YouTube or Reddit link here..." 
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleAnalyze()}
        />
        <button onClick={handleAnalyze} disabled={loading}>
          {loading ? '...' : 'Analyze'}
        </button>
      </div>

      {error && (
        <div className="card error-card glow-border-red" style={{marginTop: '2rem'}}>
          <p className="error-text">⚠️ {error}</p>
        </div>
      )}

      {loading && (
        <div className="loader">
          <div className="spinner"></div>
          <p className="loader-text">Scraping and analyzing reviews... This may take a minute.</p>
        </div>
      )}

      {data && !loading && (
        <div className="dashboard">
          <div className="stats-grid">
            <div className="card glow-card">
              <h3>Platform</h3>
              <p className="stat-value">{data.platform}</p>
            </div>
            <div className="card glow-card">
              <h3>Total Reviews</h3>
              <p className="stat-value">{data.total_comments}</p>
            </div>
            <div className="card glow-card">
              <h3>Sarcasm Rate</h3>
              <p className="stat-value">{data.summary.sarcasm_percentage.toFixed(1)}%</p>
            </div>
          </div>

          <div className="grid-2">
            <div className="card glow-card">
              <h3>Sentiment Distribution</h3>
              <SentimentGauge distribution={data.summary.sentiment_distribution} />
            </div>

            <div className="card glow-card">
              <h3>Emotion Breakdown</h3>
              <EmotionChart distribution={data.summary.emotion_distribution} rawResults={data.results} />
            </div>

            <div className="card glow-card">
              <h3>Emotion Profile</h3>
              <EmotionRadar distribution={data.summary.emotion_distribution} rawResults={data.results} />
            </div>

            <div className="card glow-card">
              <h3>Top Keywords</h3>
              <WordCloud texts={data.results.map(r => r.text)} />
            </div>
          </div>
          
          <div className="card glow-card" style={{ marginTop: '1.5rem', marginBottom: '1.5rem' }}>
            <h3>Sentiment Timeline</h3>
            <SentimentTimeline rawResults={data.results} />
          </div>

          <div className="filter-section card glow-card">
            <h3>Filter by Sentiment</h3>
            <div className="filter-buttons">
              {['All', 'Positive', 'Neutral', 'Negative'].map(filter => (
                <button 
                  key={filter}
                  className={`filter-btn ${sentimentFilter === filter ? 'active' : ''}`}
                  onClick={() => {
                    setSentimentFilter(filter);
                    setCurrentPage(1);
                  }}
                >
                  {filter}
                </button>
              ))}
            </div>
          </div>

          <div className="comment-list">
            <div className="list-header">
              <h3>Analyzed Reviews</h3>
              <div className="pagination">
                <button 
                  onClick={() => setCurrentPage(p => Math.max(1, p - 1))} 
                  disabled={currentPage === 1}
                >
                  &lt;
                </button>
                <span className="page-info">Page {currentPage} of {totalPages}</span>
                <button 
                  onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))} 
                  disabled={currentPage === totalPages}
                >
                  &gt;
                </button>
              </div>
            </div>
            {currentComments.map((res, idx) => (
              <div key={idx} className="comment-card glow-card">
                <p className="comment-text">{res.text}</p>
                <div className="badges">
                  <span className={`badge badge-${res.sentiment.toLowerCase()}`}>{res.sentiment}</span>
                  <span className="badge badge-emotion">{res.emotion}</span>
                  {res.sarcastic && <span className="badge badge-sarcasm">Sarcastic</span>}
                </div>
              </div>
            ))}
            {currentComments.length === 0 && <p style={{textAlign: 'center', opacity: 0.5}}>No reviews found for this filter.</p>}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
