# Solution Overview

## What We Built

MissionGuard AI is an explainable predictive maintenance copilot that evaluates asset health and readiness using synthetic sensor readings and maintenance history. It provides a readiness status, risk score, explanation of detected issues, and prioritized maintenance recommendations through a simple dashboard.

## How It Works

1. The system loads synthetic asset sensor data and maintenance history from a CSV dataset.
2. The system analyzes vibration, temperature, pressure, and maintenance information to identify abnormal conditions.
3. A readiness engine classifies each asset as READY, CAUTION, or NOT READY.
4. A risk engine calculates a proof-of-concept risk score and assigns LOW, MEDIUM, or HIGH risk.
5. The system explains the conditions contributing to an asset's risk.
6. The maintenance module generates prioritized recommendations based on the detected conditions.
7. The dashboard presents the results so users can quickly identify assets requiring attention.

## Architecture Diagram

> See [`architecture.md`](architecture.md) for the detailed diagram.

```
[CSV Sensor & Maintenance Data]
              ↓
      [Flask Backend]
              ↓
       [Health Analysis]
              ↓
       [Readiness Engine]
         ↙           ↘
[Readiness Status]  [Risk Engine]
                         ↓
                 [Explainability]
                         ↓
              [Maintenance Recommendations]
                         ↓
                  [Web Dashboard]
```

## Key Design Decisions

| Decision | Rationale |
|---|---|
| Used a lightweight Flask backend | Simple and suitable for building and demonstrating the prototype quickly |
| Used a CSV-based synthetic dataset | Allows safe demonstration without using real operational or military data |
| Used rule-based readiness and risk logic | Provides transparent and explainable proof-of-concept results |
| Combined risk explanation with maintenance recommendations | Helps users understand not only which asset is at risk, but also what action is recommended |

## IBM Technologies Used

IBM Bob: Used as the required AI development environment and copilot for building and working on the project.

- **[IBM Tech 1, e.g., watsonx.ai]:** [How it was used — e.g., "Used the `ibm/granite-13b-instruct-v2` model via the Python SDK to classify anomaly types from log text."]
- **[IBM Tech 2]:** [How it was used]
