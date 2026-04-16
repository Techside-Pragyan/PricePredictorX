# PricePredictorX 📈

An end-to-end Stock Price Prediction System using Machine Learning (Random Forest) and Deep Learning (LSTM) techniques. Features a premium dashboard for real-time analysis and forecasting.

## 🚀 Features

- **Data Collection**: Fetch real-time and historical stock data via Yahoo Finance.
- **Advanced Preprocessing**: Automatic calculation of MA, EMA, RSI, and MACD.
- **Machine Learning**: Linear Regression and Random Forest Regressor models.
- **Deep Learning**: Multi-layered LSTM (Long Short-Term Memory) for time-series forecasting.
- **Interactive Dashboard**: Premium UI built with React & Recharts featuring Glassmorphism.
- **Model Evaluation**: Track RMSE, MAE, and R² Score for all predictions.

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React (TypeScript, Vite)
- **ML/DL**: TensorFlow, Scikit-learn, Pandas, NumPy
- **Visuals**: Recharts, Lucide Icons, Framer Motion
- **Data Source**: yfinance

## 📁 Project Structure

```bash
PricePredictorX/
├── backend/            # FastAPI Backend
│   ├── routes/         # API Routes
│   ├── services/       # ML & Data Logic
│   └── main.py         # Entry point
├── frontend/           # React Frontend (Dashboard)
├── models/             # Saved ML models
├── data/               # Local data storage/cache
├── requirements.txt    # Python dependencies
└── README.md
```

## 🏁 Getting Started

### 1. Setup Backend
```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python -m backend.main
```

### 2. Setup Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📊 Evaluation Metrics
The system evaluates models based on:
- **RMSE**: Root Mean Squared Error
- **MAE**: Mean Absolute Error
- **R² Score**: Coefficient of Determination

## ⚠️ Disclaimer
This project is for educational purposes only. Do not use for actual financial trading decisions.

---
Built with ❤️ by Antigravity
