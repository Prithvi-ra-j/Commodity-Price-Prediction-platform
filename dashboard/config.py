import os

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Dashboard Configuration
DASHBOARD_TITLE = "Commodity Price Monitor"
DASHBOARD_ICON = "📈"

# Chart Configuration
CHART_HEIGHT = 400
CHART_TEMPLATE = "plotly_white"

# Refresh Configuration
AUTO_REFRESH_INTERVAL = 30  # seconds 