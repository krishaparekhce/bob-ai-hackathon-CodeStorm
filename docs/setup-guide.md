# Setup Guide

> MissionGuard AI is a Flask-based proof-of-concept dashboard using synthetic asset sensor and maintenance data.

## Prerequisites

Before you begin, ensure you have the following installed:
- [ Python 3.10+ ]
- [ pip ]
- [ Git ]
- [ A modern web browser ]

  
## Environment Variables

The current prototype does not require any API keys or additional environment variables.
The `.env.example` file is included in the repository for environment configuration.

```bash
cp .env.example .env
```

| Variable | Description | Required |
|---|---|---|
| `None` | No environment variables are required for the current prototype | No |

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/krishaparekhce/bob-ai-hackathon-CodeStorm.git
cd bob-ai-hackathon-CodeStorm

# 2. Install backend dependencies
pip install flask

# 3. Install frontend dependencies
# No separate frontend installation is required.

# 4. Set up the database
# No external database is required.
# The prototype uses a CSV-based synthetic dataset.
```

## Running the Application

```bash
# Start the application
python src/app.py
```

The application will be available at: http://127.0.0.1:5000

## Running Tests

```bash
The current prototype does not include a separate automated test suite.

The application can be manually verified using the following endpoints:

/api/health
/api/assets
/api/readiness
/api/risk
/api/maintenance
```

## Quick Demo (Optional)

```bash
1. Start the Flask application.
2. Open http://127.0.0.1:5000
3. Review the Mission Overview.
4. Select an asset from the dashboard.
5. View its readiness status and risk score.
6. Review the detected issues.
7. Review the recommended maintenance actions.]
```

## Troubleshooting

| Issue | Solution |
|---|---|
| [ModuleNotFoundError: No module named 'flask'] | [Run pip install flask and restart the application] |
| [Port 5000 is already in use] | [Stop the existing Flask/Python process and restart the application] |
| [Dashboard does not load] | [Confirm that python src/app.py is running] |
| [Asset data is missing] | [Confirm that src/data/assets.csv exists] |
| [Changes are not visible] | [Refresh the browser and restart the Flask application] |


