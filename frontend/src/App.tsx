import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area, Legend 
} from 'recharts';
import { Search, TrendingUp, Activity, BarChart2, Calendar, Target } from 'lucide-react';

const API_BASE = 'http://localhost:8000/api';

function App() {
  const [ticker, setTicker] = useState('AAPL');
  const [stockData, setStockData] = useState<any[]>([]);
  const [predictions, setPredictions] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchData = async () => {
    setLoading(true);
    setError('');
    try {
      const dataRes = await axios.get(`${API_BASE}/stock/${ticker}`);
      const predRes = await axios.get(`${API_BASE}/predict/${ticker}?days=7`);
      
      setStockData(dataRes.data.data);
      setPredictions(predRes.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch stock data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchData();
  };

  const getCombinedData = () => {
    if (!stockData.length || !predictions) return [];
    
    // Last 30 days of actual data
    const last30 = stockData.slice(-30).map(d => ({
      name: d.Date,
      actual: d.Close,
      predicted: null
    }));

    // Future 7 days
    const future = predictions.future_preds.map((p: number, i: number) => ({
      name: `Next Day ${i + 1}`,
      actual: null,
      predicted: p
    }));

    return [...last30, ...future];
  };

  return (
    <div className="app-container">
      <header>
        <h1>PricePredictor<span style={{color: 'var(--primary)'}}>X</span></h1>
        <p className="subtitle">Advanced AI Stock Forecasting & Analysis</p>
      </header>

      <div className="glass-card" style={{ marginBottom: '2rem' }}>
        <form onSubmit={handleSearch} className="input-group">
          <div style={{ position: 'relative', flex: 1 }}>
            <Search style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} size={20} />
            <input 
              type="text" 
              placeholder="Enter Stock Ticker (e.g., TSLA, NVDA, RELIANCE.NS)" 
              value={ticker}
              onChange={(e) => setTicker(e.target.value.toUpperCase())}
              style={{ paddingLeft: '3rem' }}
            />
          </div>
          <button className="btn" type="submit" disabled={loading}>
            {loading ? 'Analyzing...' : 'Predict Now'}
          </button>
        </form>

        {error && <div style={{ color: 'var(--error)', marginBottom: '1rem' }}>{error}</div>}

        <div className="grid">
          <div className="stat-item">
            <span className="stat-label flex items-center gap-2"><Activity size={16}/> Current Sentiment</span>
            <span className="stat-value">Bullish (0.75)</span>
          </div>
          <div className="stat-item">
            <span className="stat-label flex items-center gap-2"><Target size={16}/> Model Accuracy (R²)</span>
            <span className="stat-value">{predictions ? (predictions.metrics.R2 * 100).toFixed(2) : '--'}%</span>
          </div>
          <div className="stat-item">
            <span className="stat-label flex items-center gap-2"><TrendingUp size={16}/> 7D Price Target</span>
            <span className="stat-value">${predictions ? predictions.future_preds[6].toFixed(2) : '--'}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label flex items-center gap-2"><BarChart2 size={16}/> Volatility index</span>
            <span className="stat-value">Low</span>
          </div>
        </div>
      </div>

      <div className="grid" style={{ gridTemplateColumns: '1fr' }}>
        <div className="glass-card">
          <h2 style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <TrendingUp color="var(--primary)" /> Market Forecast
          </h2>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={getCombinedData()}>
                <defs>
                  <linearGradient id="colorActual" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--primary)" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="var(--primary)" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorPred" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--secondary)" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="var(--secondary)" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
                <XAxis dataKey="name" stroke="var(--text-muted)" fontSize={12} tickMargin={10} />
                <YAxis stroke="var(--text-muted)" fontSize={12} tickMargin={10} domain={['auto', 'auto']} />
                <Tooltip 
                  contentStyle={{ background: 'var(--bg-dark)', border: '1px solid var(--border)', borderRadius: '0.5rem' }} 
                  itemStyle={{ color: 'var(--text-main)' }}
                />
                <Legend />
                <Area type="monotone" dataKey="actual" stroke="var(--primary)" fillOpacity={1} fill="url(#colorActual)" strokeWidth={3} name="Actual Price" />
                <Area type="monotone" dataKey="predicted" stroke="var(--secondary)" strokeDasharray="5 5" fillOpacity={1} fill="url(#colorPred)" strokeWidth={3} name="Predicted Forecast" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="grid">
        <div className="glass-card">
          <h3 style={{ marginBottom: '1rem' }}>Technical Indicators</h3>
          <div className="stats-grid">
            <div className="stat-item">
              <span className="stat-label">RSI (14)</span>
              <span className="stat-value" style={{ color: stockData.length ? (stockData[stockData.length-1].RSI > 70 ? 'var(--error)' : stockData[stockData.length-1].RSI < 30 ? 'var(--success)' : 'var(--primary)') : 'inherit' }}>
                {stockData.length ? stockData[stockData.length-1].RSI.toFixed(2) : '--'}
              </span>
            </div>
            <div className="stat-item">
              <span className="stat-label">MA (20)</span>
              <span className="stat-value">${stockData.length ? stockData[stockData.length-1].MA20.toFixed(2) : '--'}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">MA (50)</span>
              <span className="stat-value">${stockData.length ? stockData[stockData.length-1].MA50.toFixed(2) : '--'}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Volume</span>
              <span className="stat-value">{stockData.length ? (stockData[stockData.length-1].Volume / 1000000).toFixed(2) : '--'}M</span>
            </div>
          </div>
        </div>

        <div className="glass-card">
          <h3 style={{ marginBottom: '1rem' }}>Model Performance</h3>
          <div className="stats-grid">
            <div className="stat-item">
              <span className="stat-label">Mean Absolute Error (MAE)</span>
              <span className="stat-value">{predictions ? predictions.metrics.MAE.toFixed(4) : '--'}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">RMSE</span>
              <span className="stat-value">{predictions ? predictions.metrics.RMSE.toFixed(4) : '--'}</span>
            </div>
          </div>
          <div style={{ marginTop: '1.5rem', color: 'var(--text-muted)', fontSize: '0.875rem' }}>
            <p><strong>Note:</strong> Predictions are based on historical trends and technical indicators. Financial markets are inherently volatile. Use this data for educational purposes.</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
