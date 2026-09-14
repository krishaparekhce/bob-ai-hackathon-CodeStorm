# 🚀 MissionGuard AI.
## Explainable Mission Readiness & Predictive Maintenance Copilot
---

## 👥 Team

| **Team Name** | [CodeStorm] |
| **Track** | [AI / DevOps / Sustainability / Open] |
| **Team Lead** | [Khushi Laddha] — [26ce043@charusat.edu.in] |
| **Members** | [Krisha Parekh], [Varsha Karavadra], [Aarvi Pavasiya] |

---

## 🎯 Problem Statement
Military organizations can face challenges in determining the readiness of their assets when sensor data and maintenance records are not analyzed together.

Maintenance may rely heavily on scheduled servicing, making it difficult to identify developing issues between maintenance cycles.

The challenge is to analyze asset health and maintenance data to identify non-ready assets, detect potential failure risks, explain the reasons behind those risks, and prioritize maintenance actions.

---

## 💡 Solution

MissionGuard AI is an explainable predictive-maintenance copilot that combines asset sensor data with maintenance history to evaluate overall asset readiness.

It identifies abnormal conditions, generates a readiness status and risk score, explains why an asset is at risk, and recommends prioritized maintenance actions.

The complete flow is:

Asset Data → Health Analysis → Readiness → Risk → Explanation → Maintenance Action

---

## ✨ Key Features

- **Feature 1:**Mission Readiness Assessment** — Classifies assets as READY, CAUTION, or NOT READY.
- **Feature 2:**Sensor Health Analysis** — Analyzes vibration, temperature, and pressure conditions.
- **Feature 3:**Risk Scoring** — Generates a 0–100 risk score and LOW, MEDIUM, or HIGH risk level.
- **Feature 4:**Explainable Risk Analysis** — Shows the detected conditions responsible for the asset's risk.
- **Feature 5:**Maintenance Recommendations** — Suggests prioritized actions based on detected issues.

---

## 🛠️ Tech Stack
Languages  | Python, JavaScript, HTML, CSS
Frameworks  | Flask
IBM Technologies  | IBM Bob
Databases  | CSV-based synthetic dataset
Other  | GitHub, VS Code

---

## 📁 Repository Structure

```text
src/
├── app.py
├── data/
│   └── assets.csv
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js

docs/
demo/
presentation/

README.md
submission.yaml
.gitignore
CONTRIBUTING.md


## ⚡ How to Run

    # 1. Clone the repo
    git clone https://github.com/krishaparekhce/bob-ai-hackathon-CodeStorm.git
    cd bob-ai-hackathon-CodeStorm

    # 2. Install dependencies
    pip install flask

    # 3. Configure environment
    cp .env.example .env
    # No additional environment variables are required for the current prototype

    # 4. Run the project
    python src/app.py

## 🖥️ Demo
📹 Demo Video  | See demo/demo-video-link.txt
🌐 Live Demo  | See demo/live-demo-url.txt
🖼️ Screenshots  | See demo/screenshots/
📊 Presentation  | See presentation/slides.pdf


## ⚠️ Known Limitations
  * The prototype uses synthetic asset data for demonstration.
  * Readiness and risk scores are proof-of-concept indicators and are not validated against real operational data.
  * The prototype is intended for decision-support demonstration and not for autonomous real-world mission decisions.

## 🏅 What We're Most Proud Of

MissionGuard AI brings asset health, mission readiness, risk analysis, explainability, and maintenance prioritization together in one workflow. Instead of only identifying a risky asset, the prototype explains the detected conditions and converts them into prioritized maintenance recommendations, making the result easier to understand and act upon.
