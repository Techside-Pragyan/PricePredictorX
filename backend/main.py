from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.stock_routes import router as stock_router

app = FastAPI(title="PricePredictorX API", description="AI-powered Stock Price Prediction System")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to PricePredictorX API"}

app.include_router(stock_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
