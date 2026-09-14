from flask import Flask, jsonify, render_template
import csv
import os

app = Flask(__name__)

DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "data",
    "assets.csv"
)


def load_assets():
    with open(DATA_FILE, newline="") as file:
        return list(csv.DictReader(file))


def assess_readiness(asset):
    vibration = float(asset["vibration"])
    temperature = float(asset["temperature"])
    pressure = float(asset["pressure"])
    last_service = int(asset["last_service_days"])

    issues = []

    if vibration > 6:
        issues.append("High vibration detected")

    if temperature > 90:
        issues.append("High temperature detected")

    if pressure > 115:
        issues.append("Pressure reading is elevated")

    if last_service > 150:
        issues.append("Service interval is overdue")

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

    if not recommendations:
        recommendations.append(
            "Continue routine monitoring"
        )

    return recommendations


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
    return jsonify(load_assets())


@app.route("/api/readiness")
def readiness():
    assets = load_assets()

    results = []

    for asset in assets:
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
    assets = load_assets()

    results = []

    for asset in assets:
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
    assets = load_assets()

    results = []

    for asset in assets:
        recommendations = recommend_maintenance(asset)

        results.append({
            "asset_id": asset["asset_id"],
            "asset_name": asset["asset_name"],
            "recommendations": recommendations
        })

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
