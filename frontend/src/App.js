import React, { useState } from 'react';
import axios from 'axios';

function App() {
  // State variables - these store data that changes
  const [symbol, setSymbol] = useState('');        // What user types
  const [data, setData] = useState(null);          // API response
  const [loading, setLoading] = useState(false);   // Loading state
  const [error, setError] = useState('');          // Error message

  // This function runs when user clicks "Analyze"
  const analyzeStock = async () => {
    // 1. Reset previous data and show loading
    setLoading(true);
    setError('');
    setData(null);

    try {
      // 2. Send GET request to your FastAPI backend
      const response = await axios.get(`http://localhost:8000/analyze/${symbol}`);
      
      // 3. Store the response data
      setData(response.data);
    } catch (err) {
      // 4. If something goes wrong, show error
      setError('Failed to fetch data. Is the backend running?');
      console.error(err);
    } finally {
      // 5. Always turn off loading, whether success or error
      setLoading(false);
    }
  };

  // This is what renders on the screen
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>📊 AI Stock Analyzer</h1>
      
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        <input
          type="text"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value.toUpperCase())}
          placeholder="Enter stock symbol (e.g., META)"
          style={{
            padding: '10px',
            fontSize: '16px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            flex: 1,
            maxWidth: '300px'
          }}
        />
        <button
          onClick={analyzeStock}
          disabled={loading}
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            backgroundColor: loading ? '#6c757d' : '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </div>

      {/* Show error message if there is one */}
      {error && (
        <div style={{ color: 'red', marginBottom: '20px' }}>
          ❌ {error}
        </div>
      )}

      {/* Show results when data exists */}
      {data && (
        <div style={{
          backgroundColor: '#f8f9fa',
          padding: '20px',
          borderRadius: '8px',
          border: '1px solid #dee2e6'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h2 style={{ margin: 0 }}>{data.symbol}</h2>
            <span style={{ fontSize: '24px', fontWeight: 'bold', color: '#28a745' }}>
              ${data.current_saved_price}
            </span>
          </div>
          <div style={{ marginTop: '20px', whiteSpace: 'pre-wrap' }}>
            {data.market_outlook}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;