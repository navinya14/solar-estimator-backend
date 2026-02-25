# models.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional


class EstimateRequest(BaseModel):
    monthly_electricity_units: float = Field(
        ..., gt=0,
        description="Monthly electricity consumption in kWh (must be > 0)",
        example=300.0,
    )
    city: Optional[str] = Field(
        default=None,
        description="Indian city name (case-insensitive).",
        example="Nagpur",
    )
    monthly_bill_amount: Optional[float] = Field(
        default=None, ge=0,
        description="Monthly electricity bill in INR.",
        example=2100.0,
    )

    @field_validator("city")
    @classmethod
    def strip_city(cls, v):
        return v.strip() if v else v


class TierEstimate(BaseModel):
    cost_inr: float
    payback_years: float


class CostEstimates(BaseModel):
    budget: TierEstimate
    mid: TierEstimate
    premium: TierEstimate


class AssumptionsUsed(BaseModel):
    avg_units_per_kw_per_month: float
    coverage_factor_percent: int
    cost_per_kw_budget_inr: int
    cost_per_kw_mid_inr: int
    cost_per_kw_premium_inr: int
    per_unit_electricity_rate_inr: float
    city_matched: str


class EstimateResponse(BaseModel):
    estimated_system_size_kw: float
    cost_estimates: CostEstimates
    estimated_monthly_savings_inr: float
    estimated_units_offset_per_month: float
    assumptions_used: AssumptionsUsed
