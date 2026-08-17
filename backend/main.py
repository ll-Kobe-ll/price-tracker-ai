import os
import uvicorn
import sqlite3
import yfinance as yf
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from datetime import datetime
from google import genai
from google.genai import types

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React's address
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# This looks for the .env file and loads the variables
load_dotenv()

# This grabs the key from your computer's memory, NOT the code
client = genai.Client()

# 1. Connect to the database (it creates the file if it doesn't exist)
def init_db():
    conn = sqlite3.connect("price_history.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            price REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.get("/price/{symbol}")
def get_and_save_price(symbol: str):
    symbol = symbol.upper().strip()
    ticker = yf.Ticker(symbol)
    data = ticker.history(period='1d')
    
    if data.empty:
        return {"error": "Symbol not found"}
        
    price = round(float(data['Close'].iloc[-1]), 2)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 2. SAVE the data to your local file
    conn = sqlite3.connect("price_history.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO prices (symbol, price, timestamp) VALUES (?, ?, ?)", 
                   (symbol.upper(), price, timestamp))
    conn.commit()
    conn.close()

    return {"symbol": symbol.upper(), "price": price, "saved": True}

@app.get("/history")
def get_history():
    # 3. READ the data back
    conn = sqlite3.connect("price_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prices ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    return {"history": rows}

@app.get("/analyze/{symbol}")
def analyze_stock(symbol: str):
    symbol = symbol.upper().strip()
    
    # 1. FIRST: Get the live price from yfinance (NOT from database)
    ticker = yf.Ticker(symbol)
    data = ticker.history(period='1d')
    
    if data.empty:
        return {"error": "Symbol not found"}
    
    current_price = round(float(data['Close'].iloc[-1]), 2)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 2. SECOND: Save the live price to SQLite (for history)
    conn = sqlite3.connect("price_history.db")
    cursor = conn.cursor()
    
    # Save the new price
    cursor.execute("INSERT INTO prices (symbol, price, timestamp) VALUES (?, ?, ?)", 
                   (symbol, current_price, timestamp))
    conn.commit()
    
    # 3. THIRD: Get last 5 prices (including the one we just saved)
    cursor.execute("SELECT price, timestamp FROM prices WHERE symbol = ? ORDER BY id DESC LIMIT 5", (symbol,))
    recent = cursor.fetchall()
    conn.close()
    
    # Build history text for Gemini
    history_text = "\n".join([f"{ts}: ${p}" for p, ts in recent])
    
    # 4. FOURTH: Feed it to Gemini with BOTH current and historical data
    prompt = (
        f"You are a sharp, no-nonsense market analyst. Use real-time search to check current "
        f"news, sentiment, and events for {symbol} before answering.\n\n"
        f"Current live price for {symbol}: ${current_price}\n"
        f"Recent price history (last 5 records):\n{history_text}\n\n"
        "Write a report with these exact sections, plain and direct, no buzzwords or filler "
        "phrases (no 'robust', 'well-positioned', 'headwinds', 'strategic accumulation'):\n\n"
        "1. WHAT'S HAPPENING: 1-2 sentences on the current price trend and why, based on real "
        "current events/news you find, not general knowledge.\n"
        "2. CROWD CHECK: Is money already piled into this (late/hot, risk of pullback) or is "
        "this early before the crowd notices? Say which, and why, plainly.\n"
        f"3. SUPPLY CHAIN ANGLE: Name 2-4 real, specific tickers for companies that supply "
        f"critical components, materials, or software to {symbol} or its sector, that could "
        "move on the same trend before it's obvious. Say why each is relevant, briefly.\n"
        "4. BOTTOM LINE: One direct sentence — get in now, wait for a pullback, or avoid, and why.\n\n"
        "Be confident and specific. If unsure, say so directly instead of hedging."
    )
    
    # 5. Call Gemini
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())]
        )
    )
    
    # 6. Return with the live price
    return {
        "symbol": symbol,
        "current_saved_price": current_price,  # Now this is live!
        "market_outlook": response.text
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)