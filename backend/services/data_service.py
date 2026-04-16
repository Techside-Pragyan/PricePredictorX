import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as ta

class DataService:
    @staticmethod
    def fetch_stock_data(ticker, period="2y", interval="1d"):
        """
        Fetch historical stock data using Yahoo Finance API
        """
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period, interval=interval)
            
            if df.empty:
                return None
            
            # Reset index to make Date a column
            df = df.reset_index()
            return df
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None

    @staticmethod
    def preprocess_data(df):
        """
        Add technical indicators and handle missing values
        """
        if df is None or df.empty:
            return None
        
        # Ensure column names are consistently capitalized for pandas_ta
        df.columns = [col.capitalize() for col in df.columns]
        
        # Add Technical Indicators
        # Moving Averages
        df['MA20'] = ta.sma(df['Close'], length=20)
        df['MA50'] = ta.sma(df['Close'], length=50)
        
        # Exponential Moving Averages
        df['EMA20'] = ta.ema(df['Close'], length=20)
        
        # RSI
        df['RSI'] = ta.rsi(df['Close'], length=14)
        
        # MACD
        macd = ta.macd(df['Close'])
        df = pd.concat([df, macd], axis=1)
        
        # Handle missing values created by indicators
        df = df.dropna()
        
        return df

    @staticmethod
    def prepare_sequences(data, seq_length=60):
        """
        Convert time-series data into supervised learning format (sequences)
        """
        X, y = [], []
        for i in range(seq_length, len(data)):
            X.append(data[i-seq_length:i])
            y.append(data[i, 0]) # Predicting the 'Close' price (assuming it's at index 0)
        
        return np.array(X), np.array(y)
