 Price History & AI Market Analyzer

A full-stack web application that fetches live stock/commodity prices, stores historical data, and generates AI-powered market analysis using Google Gemini with real-time search grounding.

## 🚀 What It Does

- **Live Price Fetching** – Gets current prices for any ticker symbol via `yfinance`
- **Historical Tracking** – Saves every price lookup to a local SQLite database with timestamps
- **AI-Powered Analysis** – Generates a 4-part market report using Gemini with real-time Google Search grounding (current news/events, not just training data)
- **React Frontend** – Clean UI for entering symbols and viewing analysis
- **Full-Stack Architecture** – FastAPI backend + React frontend with CORS support

## 🛠️ Tech Stack

### Backend
- FastAPI – Python web framework
- Uvicorn – ASGI server
- SQLite – Lightweight database for price history
- yfinance – Yahoo Finance API wrapper
- Google Gemini API – AI analysis with Search grounding
- python-dotenv – Environment variable management

### Frontend
- React – UI framework
- Axios – HTTP client for API calls
- Create React App – Build tool

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/price-tracker-ai.git
cd price-tracker-ai
```

### 2. Backend Setup

Create a virtual environment and install dependencies:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

pip install fastapi uvicorn python-dotenv yfinance google-genai fastapi-cors
```

Create a `.env` file in the project root with your Gemini API key:
```env
GEMINI_API_KEY=your_api_key_here
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

## 🏃‍♂️ Running the Application

### Start the Backend
```bash
# From the project root
uvicorn main:app --reload
```
Server runs at `http://127.0.0.1:8000`

### Start the Frontend
```bash
# In a new terminal
cd frontend
npm start
```
App runs at `http://localhost:3000`

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/price/{symbol}` | Fetches current price for a ticker and saves to database |
| GET | `/history` | Returns last 10 saved price entries |
| GET | `/analyze/{symbol}` | Generates AI market report (live price + historical context + real-time news) |

### Example Responses

**GET /price/AAPL**
```json
{
  "symbol": "AAPL",
  "price": 189.84,
  "saved": true
}
```

**GET /analyze/AAPL**
```json
{
  "symbol": "AAPL",
  "current_saved_price": 189.84,
  "market_outlook": "1. WHAT'S HAPPENING: ..."
}
```

## 🎯 How It Works

1. User enters a stock symbol in the React frontend
2. Frontend sends GET request to FastAPI backend
3. Backend fetches live price from Yahoo Finance
4. Price is saved to SQLite for historical tracking
5. Backend retrieves last 5 prices for trend context
6. Gemini API generates analysis using:
   - Current price
   - Historical trend data
   - Real-time Google Search results (news, events, sentiment)
7. Analysis is returned to React frontend for display

## 📁 Project Structure

```
price-tracker-ai/
├── main.py              # FastAPI application
├── price_history.db     # SQLite database (auto-created)
├── frontend/
│   ├── src/
│   │   ├── App.js       # Main React component
│   │   └── index.js     # React entry point
│   ├── package.json     # Frontend dependencies
│   └── node_modules/
├── .env                 # API keys (don't commit!)
└── README.md
```

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

**Important:** Never commit `.env` to version control. It's already in `.gitignore`.

## 🧪 Testing

### Test the Backend
```bash
# In your browser or using curl
curl http://127.0.0.1:8000/analyze/META
```

### Test the Frontend
1. Open `http://localhost:3000`
2. Enter a stock symbol (e.g., AAPL, META, NVDA)
3. Click "Analyze"
4. View the AI-generated report

## 🚧 Future Improvements

- [ ] Add price history chart (Chart.js/Recharts)
- [ ] Save multiple symbols to a watchlist
- [ ] Export analysis as PDF
- [ ] Dark/Light mode toggle
- [ ] Add support for cryptocurrencies
- [ ] Deploy to cloud (Render/Railway)

## 📝 Notes

- The `/analyze/` endpoint automatically fetches live prices and saves them to the database – no need to call `/price/` first
- SQLite database is created automatically when you run the app
- Gemini uses Google Search grounding for real-time news and events, not just training data
