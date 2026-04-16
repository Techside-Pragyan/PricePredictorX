from fastapi import APIRouter, HTTPException
from backend.services.data_service import DataService
from backend.services.model_service import ModelService
import pandas as pd
import numpy as np

router = APIRouter()
data_service = DataService()
model_service = ModelService()

@router.get("/stock/{ticker}")
async def get_stock_data(ticker: str, period: str = "2y"):
    df = data_service.fetch_stock_data(ticker, period=period)
    if df is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    df_preprocessed = data_service.preprocess_data(df)
    
    # Convert to list of dicts for JSON response
    # Only return essential data for visualization to keep response size manageable
    chart_data = df_preprocessed[['Date', 'Close', 'MA20', 'MA50', 'Volume', 'RSI']].copy()
    chart_data['Date'] = chart_data['Date'].dt.strftime('%Y-%m-%d')
    
    return {
        "ticker": ticker,
        "data": chart_data.to_dict(orient="records")
    }

@router.get("/predict/{ticker}")
async def predict_stock(ticker: str, days: int = 7):
    df = data_service.fetch_stock_data(ticker, period="2y")
    if df is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    df_preprocessed = data_service.preprocess_data(df)
    
    # Train ML Models (LR, RF)
    ml_results = model_service.train_ml_models(df_preprocessed)
    
    # Train/Get LSTM prediction
    lstm_model, lstm_metrics, test_preds, test_actual = model_service.train_lstm_model(df_preprocessed)
    
    # Prepare last sequence for future prediction
    scaled_data = model_service.scaler.transform(df_preprocessed[['Close']].values)
    last_sequence = scaled_data[-60:]
    
    future_preds = model_service.predict_future(lstm_model, last_sequence, days, model_service.scaler)
    
    return {
        "ticker": ticker,
        "metrics": {
            "LSTM": lstm_metrics,
            "LinearRegression": ml_results["LR"]["metrics"],
            "RandomForest": ml_results["RF"]["metrics"]
        },
        "test_actual": test_actual.flatten().tolist(),
        "test_preds": test_preds.flatten().tolist(),
        "future_preds": future_preds.flatten().tolist()
    }
