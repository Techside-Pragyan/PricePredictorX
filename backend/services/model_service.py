import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import joblib
import os

class ModelService:
    def __init__(self, models_dir="models"):
        self.models_dir = models_dir
        if not os.path.exists(models_dir):
            os.makedirs(models_dir)
        self.scaler = MinMaxScaler(feature_range=(0, 1))

    def train_ml_models(self, df):
        """
        Train Traditional ML Models (Linear Regression, Random Forest)
        """
        # Features: MA20, MA50, EMA20, RSI, MACD_12_26_9
        features = ['MA20', 'MA50', 'EMA20', 'RSI']
        X = df[features]
        y = df['Close']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

        # Linear Regression
        lr_model = LinearRegression()
        lr_model.fit(X_train, y_train)
        lr_preds = lr_model.predict(X_test)

        # Random Forest
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train)
        rf_preds = rf_model.predict(X_test)

        results = {
            "LR": {
                "model": lr_model,
                "metrics": self._evaluate(y_test, lr_preds)
            },
            "RF": {
                "model": rf_model,
                "metrics": self._evaluate(y_test, rf_preds)
            }
        }
        
        return results

    def _evaluate(self, y_true, y_pred):
        return {
            "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
            "MAE": mean_absolute_error(y_true, y_pred),
            "R2": r2_score(y_true, y_pred)
        }

    def train_lstm_model(self, df, seq_length=60):
        """
        Train LSTM Model for time-series forecasting
        """
        data = df[['Close']].values
        scaled_data = self.scaler.fit_transform(data)

        X, y = [], []
        for i in range(seq_length, len(scaled_data)):
            X.append(scaled_data[i-seq_length:i, 0])
            y.append(scaled_data[i, 0])
        
        X, y = np.array(X), np.array(y)
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))

        # Split data
        train_size = int(len(X) * 0.8)
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]

        # Build LSTM
        model = Sequential([
            LSTM(units=50, return_sequences=True, input_shape=(X.shape[1], 1)),
            Dropout(0.2),
            LSTM(units=50, return_sequences=False),
            Dropout(0.2),
            Dense(units=25),
            Dense(units=1)
        ])

        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(X_train, y_train, batch_size=32, epochs=10, verbose=0)

        # Evaluate
        predictions = model.predict(X_test)
        predictions = self.scaler.inverse_transform(predictions)
        y_test_unscaled = self.scaler.inverse_transform(y_test.reshape(-1, 1))

        metrics = self._evaluate(y_test_unscaled, predictions)
        
        return model, metrics, predictions, y_test_unscaled

    def predict_future(self, model, last_sequences, days_to_predict, scaler):
        """
        Predict future prices
        """
        future_predictions = []
        current_seq = last_sequences.copy()

        for _ in range(days_to_predict):
            prediction = model.predict(current_seq.reshape(1, current_seq.shape[0], 1), verbose=0)
            future_predictions.append(prediction[0, 0])
            
            # Update sequence: remove oldest, add new prediction
            current_seq = np.append(current_seq[1:], prediction)
        
        return scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))
