# Rooftop Solar Estimator

A free, beginner-friendly **solar estimation app** for Indian households — FastAPI backend + plain HTML/CSS/JS frontend. No paid APIs, no external HTTP calls, no build tools required.

---

## Features

- 🌞 **Browser UI** — open `http://localhost:8000` and fill in the form
- 🌆 Supports **11 major Indian cities** with city-specific solar generation data
- 💰 Returns **3 cost tiers** (Budget / Mid / Premium) with installation cost estimates
- 📊 Calculates **monthly savings** and **payback period** based on your electricity bill
- ✅ Input validation with helpful error messages (HTTP 422 for invalid input)
- 🔓 CORS-enabled — ready to integrate with any frontend
- 📖 Interactive API docs at `/docs` (Swagger UI)

---

## Project Structure

```
├── start.sh          # ⚡ One-command local deploy script
├── index.html        # Single-page frontend (no build step required)
├── main.py           # FastAPI app with all 3 endpoints + serves index.html
├── estimator.py      # Pure calculation logic (no FastAPI imports)
├── city_data.py      # City solar generation lookup table
├── models.py         # Pydantic request/response models
├── requirements.txt  # fastapi, uvicorn, pydantic
└── README.md         # Setup instructions + example curl commands
```

---

## ⚡ Quick Start (One Command)

```bash
git clone https://github.com/navinya14/solar-estimator-backend.git
cd solar-estimator-backend
bash start.sh
```

`start.sh` automatically:
1. Creates a Python virtual environment (`venv/`)
2. Installs all dependencies from `requirements.txt`
3. Starts the server at **http://localhost:8000**

> **Custom port:** `bash start.sh --port 8080`

Then open your browser at:
- 🌞 **Frontend UI** → http://localhost:8000
- 📖 **Swagger API docs** → http://localhost:8000/docs

Press `Ctrl+C` to stop the server.

---

## Manual Setup (Step-by-Step)

```bash
# 1. Clone the repository
git clone https://github.com/navinya14/solar-estimator-backend.git
cd solar-estimator-backend

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the development server
uvicorn main:app --reload
```

---

## API Endpoints

| Method | Endpoint    | Description                                      |
|--------|-------------|--------------------------------------------------|
| GET    | `/health`   | Health check — returns `{"status": "ok"}`        |
| GET    | `/cities`   | List all supported cities                        |
| POST   | `/estimate` | Estimate solar system size, cost, and savings    |

---

## Example Usage

### Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{"status": "ok"}
```

---

### List Supported Cities

```bash
curl http://localhost:8000/cities
```

---

### Estimate Solar Requirements

```bash
curl -X POST http://localhost:8000/estimate \
  -H "Content-Type: application/json" \
  -d '{"monthly_electricity_units": 300, "city": "Nagpur", "monthly_bill_amount": 2100}'
```

Example JSON response:
```json
{
  "estimated_system_size_kw": 2.0,
  "cost_estimates": {
    "budget": {
      "cost_inr": 90000.0,
      "payback_years": 4.29
    },
    "mid": {
      "cost_inr": 110000.0,
      "payback_years": 5.24
    },
    "premium": {
      "cost_inr": 130000.0,
      "payback_years": 6.19
    }
  },
  "estimated_monthly_savings_inr": 1750.0,
  "estimated_units_offset_per_month": 260.0,
  "assumptions_used": {
    "avg_units_per_kw_per_month": 130.0,
    "coverage_factor_percent": 80,
    "cost_per_kw_budget_inr": 45000,
    "cost_per_kw_mid_inr": 55000,
    "cost_per_kw_premium_inr": 65000,
    "per_unit_electricity_rate_inr": 7.0,
    "city_matched": "Nagpur"
  }
}
```

---

## Supported Cities

| City        | Avg Units / kW / Month |
|-------------|------------------------|
| Ahmedabad   | 132.0                  |
| Bangalore   | 125.0                  |
| Bengaluru   | 125.0                  |
| Chennai     | 130.0                  |
| Delhi       | 120.0                  |
| Hyderabad   | 128.0                  |
| Jaipur      | 135.0                  |
| Kolkata     | 110.0                  |
| Mumbai      | 115.0                  |
| Nagpur      | 130.0                  |
| Pune        | 125.0                  |

Cities not in this list use the **national average of 120 units/kW/month**.

---

## Calculation Logic

| Step | Formula |
|------|---------|
| Raw system size | `(monthly_units × 0.80) / avg_units_per_kw` |
| System size (kW) | Rounded up to nearest bucket: 1, 2, 3, 5, 7, or 10 kW |
| Units offset/month | `avg_units_per_kw × system_size_kw` |
| Monthly savings (INR) | `units_offset × per_unit_rate` |
| Payback period (years) | `total_cost / (monthly_savings × 12)` |
| Per-unit rate | Derived from bill ÷ units if bill provided, else ₹7.00/unit |

**Coverage factor**: 80% — accounts for panel efficiency, shading, and system losses.

---

## Disclaimer

> ⚠️ All estimates are **approximate** and intended for planning purposes only. Actual system size, cost, and savings may vary based on roof area, local electricity tariffs, government subsidies, panel efficiency, and installation conditions. Consult a certified solar installer for a precise quote.
