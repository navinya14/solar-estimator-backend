# estimator.py
# Pure calculation logic — no FastAPI imports.

from city_data import CITY_SOLAR_DATA, DEFAULT_AVG_UNITS_PER_KW

COVERAGE_FACTOR: float = 0.80
SIZE_BUCKETS: list[float] = [1, 2, 3, 5, 7, 10]
COST_PER_KW: dict[str, float] = {
    "budget":  45_000,
    "mid":     55_000,
    "premium": 65_000,
}
DEFAULT_PER_UNIT_RATE: float = 7.0


def get_avg_units_per_kw(city: str | None) -> tuple[float, str]:
    if city:
        key = city.strip().lower()
        if key in CITY_SOLAR_DATA:
            return CITY_SOLAR_DATA[key], city.strip().title()
    return DEFAULT_AVG_UNITS_PER_KW, "Default (national average)"


def round_up_to_bucket(required_kw: float) -> float:
    for bucket in SIZE_BUCKETS:
        if required_kw <= bucket:
            return float(bucket)
    return float(SIZE_BUCKETS[-1])


def calculate_per_unit_rate(monthly_bill_amount, monthly_electricity_units):
    if monthly_bill_amount and monthly_bill_amount > 0:
        return round(monthly_bill_amount / monthly_electricity_units, 4)
    return DEFAULT_PER_UNIT_RATE


def calculate_estimate(monthly_electricity_units, city, monthly_bill_amount):
    avg_units_per_kw, city_label = get_avg_units_per_kw(city)
    raw_kw = (monthly_electricity_units * COVERAGE_FACTOR) / avg_units_per_kw
    system_size_kw = round_up_to_bucket(raw_kw)
    per_unit_rate = calculate_per_unit_rate(monthly_bill_amount, monthly_electricity_units)
    units_offset = avg_units_per_kw * system_size_kw
    monthly_savings = units_offset * per_unit_rate
    annual_savings = monthly_savings * 12
    cost_estimates = {}
    for tier, rate in COST_PER_KW.items():
        total_cost = rate * system_size_kw
        payback_years = round(total_cost / annual_savings, 2) if annual_savings > 0 else None
        cost_estimates[tier] = {"cost_inr": round(total_cost, 2), "payback_years": payback_years}
    return {
        "estimated_system_size_kw": system_size_kw,
        "cost_estimates": cost_estimates,
        "estimated_monthly_savings_inr": round(monthly_savings, 2),
        "estimated_units_offset_per_month": round(units_offset, 2),
        "assumptions_used": {
            "avg_units_per_kw_per_month": avg_units_per_kw,
            "coverage_factor_percent": int(COVERAGE_FACTOR * 100),
            "cost_per_kw_budget_inr": int(COST_PER_KW["budget"]),
            "cost_per_kw_mid_inr": int(COST_PER_KW["mid"]),
            "cost_per_kw_premium_inr": int(COST_PER_KW["premium"]),
            "per_unit_electricity_rate_inr": per_unit_rate,
            "city_matched": city_label,
        },
    }
