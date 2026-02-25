#!/usr/bin/env bash
# start.sh — One-command local deployment for the Rooftop Solar Estimator
# Usage:  bash start.sh
#         bash start.sh --port 8080   (optional port, default: 8000)

set -e

PORT=8000
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --port) PORT="$2"; shift ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
  shift
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "======================================"
echo "  🌞 Rooftop Solar Estimator"
echo "======================================"
echo ""

# ── 1. Create virtual environment if it doesn't exist ──────────────────────
if [ ! -d "venv" ]; then
  echo "📦 Creating virtual environment..."
  python3 -m venv venv
fi

# ── 2. Activate virtual environment ────────────────────────────────────────
# shellcheck disable=SC1091
source venv/bin/activate

# ── 3. Install / upgrade dependencies ──────────────────────────────────────
echo "📥 Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# ── 4. Launch the server ───────────────────────────────────────────────────
echo ""
echo "🚀 Starting server on http://localhost:${PORT}"
echo ""
echo "  Frontend UI  →  http://localhost:${PORT}"
echo "  API docs     →  http://localhost:${PORT}/docs"
echo "  Health check →  http://localhost:${PORT}/health"
echo ""
echo "Press Ctrl+C to stop."
echo ""

exec uvicorn main:app --host 0.0.0.0 --port "$PORT" --reload
