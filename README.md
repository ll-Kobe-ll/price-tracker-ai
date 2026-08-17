# Price History & AI Market Analyzer
A FastAPI backend that fetches live stock/commodity prices, saves them to a local SQLite database, and generates AI-powered market analysis using Google Gemini with real-time search grounding.

## What it does
- Fetches live prices for any ticker symbol via yfinance
- Saves every price lookup to a local SQLite database with a timestamp
- Serves your recent price history back as JSON
- Analyzes a symbol's price trend using Gemini, grounded in real-time search results (current news/events, not just training data)

## Setup
1. Clone or download this project
2. Create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   python -m pip install fastapi uvicorn python-dotenv yfinance google-genai
   ```
4. Create a `.env` file in the project root with your Gemini API key:
   ```
   GEMINI_API_KEY=your_key_here
   ```

## Running it
```
python -m uvicorn main:app --reload
```

Server runs at `http://127.0.0.1:8000`

## Endpoints
- `GET /price/{symbol}` — fetches the current price for a ticker and saves it to the database
- `GET /history` — returns the last 10 saved price entries
- `GET /analyze/{symbol}` — pulls recent price history for a symbol and generates a 4-part AI market report (trend, crowd positioning, supply-chain angle, bottom line), grounded in real-time search

## Example
```
GET /price/AAPL
GET /analyze/AAPL
```

## Tech stack
- FastAPI (backend framework)
- Uvicorn (server)
- SQLite (database)
- yfinance (price data)
- Google Gemini API with Search grounding (AI analysis)
