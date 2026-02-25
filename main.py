# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import EstimateRequest, EstimateResponse
from estimator import calculate_estimate
from city_data import CITY_SOLAR_DATA

app = FastAPI(
    title="Rooftop Solar Estimator API",
    description="A free solar estimation engine for Indian households.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Utility"])
def health_check():
    return {"status": "ok"}


@app.get("/cities", tags=["Utility"])
def list_cities():
    supported = sorted(city.title() for city in CITY_SOLAR_DATA.keys())
    return {
        "supported_cities": supported,
        "note": "City matching is case-insensitive. Unlisted cities use the national average (120 units/kW/month).",
    }


@app.post("/estimate", response_model=EstimateResponse, tags=["Estimation"])
def estimate_solar(request: EstimateRequest):
    try:
        result = calculate_estimate(
            monthly_electricity_units=request.monthly_electricity_units,
            city=request.city,
            monthly_bill_amount=request.monthly_bill_amount,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")
    return EstimateResponse(**result)
