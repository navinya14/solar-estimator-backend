# city_data.py
# Lookup table for average solar units generated per kW per month
# across major Indian cities.

CITY_SOLAR_DATA: dict[str, float] = {
    "nagpur":     130.0,
    "delhi":      120.0,
    "bangalore":  125.0,
    "bengaluru":  125.0,
    "mumbai":     115.0,
    "chennai":    130.0,
    "hyderabad":  128.0,
    "pune":       125.0,
    "jaipur":     135.0,
    "ahmedabad":  132.0,
    "kolkata":    110.0,
}

DEFAULT_AVG_UNITS_PER_KW: float = 120.0
