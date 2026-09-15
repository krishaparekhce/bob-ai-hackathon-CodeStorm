from flask import Flask, jsonify, render_template
import csv
import os

app = Flask(__name__)

DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "data",
    "assets.csv"
)


# Fix 4: wrap file I/O so callers receive a clean exception message
def load_assets():
    try:
        with open(DATA_FILE, newline="") as file:
            rows = list(csv.DictReader(file))
        if not rows:
            raise ValueError("Asset data file is empty.")
        return rows
    except FileNotFoundError:
        raise RuntimeError(f"Data file not found: {DATA_FILE}")
    except Exception as exc:
        raise RuntimeError(f"Failed to load asset data: {exc}") from exc


def assess_readiness(asset):
    vibration = float(asset["vibration"])
    temperature = float(asset["temperature"])
    pressure = float(asset["pressure"])
    last_service = int(asset["last_service_days"])
    # Fix 7: usage_hours contributes a lightweight wear signal
    usage_hours = int(asset["usage_hours"])

    issues = []

    if vibration > 6:
        issues.append("High vibration detected")

    if temperature > 90:
        issues.append("High temperature detected")

    if pressure > 115:
        issues.append("Pressure reading is elevated")

    if last_service > 150:
        issues.append("Service interval is overdue")

    # Fix 7: flag assets with very high accumulated usage
    if usage_hours > 800:
        issues.append("High accumulated usage hours")

    if len(issues) >= 3:
        status = "NOT READY"
    elif len(issues) >= 1:
        status = "CAUTION"
    else:
        status = "READY"

    return status, issues


def calculate_risk(asset):
    vibration = float(asset["vibration"])
    temperature = float(asset["temperature"])
    pressure = float(asset["pressure"])
    last_service = int(asset["last_service_days"])
    # Fix 7: incorporate usage_hours and maintenance_count into risk score
    usage_hours = int(asset["usage_hours"])
    maintenance_count = int(asset["maintenance_count"])

    score = 0

    if vibration > 6:
        score += 30
    elif vibration > 4:
        score += 15

    if temperature > 90:
        score += 30
    elif temperature > 80:
        score += 15

    if pressure > 115:
        score += 25
    elif pressure > 110:
        score += 10

    if last_service > 150:
        score += 15
    elif last_service > 100:
        score += 8

    # Fix 7: high usage hours adds a wear-accumulation signal (max +10)
    if usage_hours > 800:
        score += 10
    elif usage_hours > 600:
        score += 5

    # Fix 7: high maintenance count suggests a history of recurring issues (+5)
    if maintenance_count >= 7:
        score += 5

    score = min(score, 100)

    if score >= 60:
        risk = "HIGH"
    elif score >= 30:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return score, risk


def recommend_maintenance(asset):
    vibration = float(asset["vibration"])
    temperature = float(asset["temperature"])
    pressure = float(asset["pressure"])
    last_service = int(asset["last_service_days"])
    # Fix 7: usage_hours informs maintenance recommendations
    usage_hours = int(asset["usage_hours"])

    recommendations = []

    if vibration > 6:
        recommendations.append(
            "Inspect vibration-producing components"
        )
    elif vibration > 4:
        recommendations.append(
            "Monitor vibration trend closely"
        )

    if temperature > 90:
        recommendations.append(
            "Inspect thermal and cooling systems"
        )
    elif temperature > 80:
        recommendations.append(
            "Monitor temperature trend"
        )

    if pressure > 115:
        recommendations.append(
            "Inspect pressure-related components"
        )
    elif pressure > 110:
        recommendations.append(
            "Monitor pressure trend"
        )

    if last_service > 150:
        recommendations.append(
            "Schedule overdue maintenance review"
        )
    elif last_service > 100:
        recommendations.append(
            "Review upcoming maintenance schedule"
        )

    # Fix 7: recommend inspection when usage hours are high
    if usage_hours > 800:
        recommendations.append(
            "Conduct wear inspection due to high usage hours"
        )
    elif usage_hours > 600:
        recommendations.append(
            "Monitor wear indicators — usage hours are elevated"
        )

    if not recommendations:
        recommendations.append(
            "Continue routine monitoring"
        )

    return recommendations


# B4 fix: always returns exactly 2 values — (list, None) on success or
# (None, Response) on failure.  The error response is built with the
# correct HTTP status code via make_response so callers can simply
# `return err` without needing a third tuple element.
def _get_assets_or_error():
    try:
        return load_assets(), None
    except RuntimeError as exc:
        from flask import make_response
        return None, make_response(jsonify({"error": str(exc)}), 500)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "message": "MissionGuard AI API is running"
    })


@app.route("/api/assets")
def assets():
    data, err = _get_assets_or_error()
    if err is not None:
        return err
    return jsonify(data)


@app.route("/api/readiness")
def readiness():
    data, err = _get_assets_or_error()
    if err is not None:
        return err

    results = []

    for asset in data:
        status, issues = assess_readiness(asset)

        results.append({
            "asset_id": asset["asset_id"],
            "asset_name": asset["asset_name"],
            "readiness": status,
            "issues": issues
        })

    return jsonify(results)


@app.route("/api/risk")
def risk():
    data, err = _get_assets_or_error()
    if err is not None:
        return err

    results = []

    for asset in data:
        score, risk_level = calculate_risk(asset)

        results.append({
            "asset_id": asset["asset_id"],
            "asset_name": asset["asset_name"],
            "risk_score": score,
            "risk_level": risk_level
        })

    return jsonify(results)


@app.route("/api/maintenance")
def maintenance():
    data, err = _get_assets_or_error()
    if err is not None:
        return err

    results = []

    for asset in data:
        recommendations = recommend_maintenance(asset)

        results.append({
            "asset_id": asset["asset_id"],
            "asset_name": asset["asset_name"],
            "recommendations": recommendations
        })

    return jsonify(results)


# Fix 5: debug=False for normal runs; set FLASK_DEBUG=1 env var for dev reloading
if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug_mode)
