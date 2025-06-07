from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
from calculations.edenred import calculate_optimal_payment

app = FastAPI(
    title="Lounarilaskuri API",
    description="API for calculating optimal Edenred lunch card payments",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PaymentRequest(BaseModel):
    total_price: float = Field(..., gt=0, description="Total price of food to pay")

class CardPayment(BaseModel):
    amount: float
    
class PaymentResponse(BaseModel):
    card_payments: List[float]
    cash_payment: float
    total_cash_amount: float
    total_card_amount: float
    card_uses: int
    total_amount: float

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Lounarilaskuri API is running!"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/calculate-payment", response_model=PaymentResponse)
async def calculate_payment(request: PaymentRequest):
    """
    Calculate the optimal way to pay for food using Edenred lunch cards.
    
    This endpoint calculates how to minimize cash payments by optimally using
    lunch card payments within the daily limits.
    """
    try:
        result = calculate_optimal_payment(request.total_price)
        return PaymentResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Calculation error: {str(e)}")

@app.get("/payment-limits")
async def get_payment_limits():
    """
    Get the current Edenred payment limits and rules.
    """
    from calculations.edenred import (
        minimum_lunch_card_payment,
        maximum_lunch_card_payment,
        maximum_card_payment_times_per_day
    )
    
    return {
        "minimum_payment": minimum_lunch_card_payment,
        "maximum_payment": maximum_lunch_card_payment,
        "max_uses_per_day": maximum_card_payment_times_per_day
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
