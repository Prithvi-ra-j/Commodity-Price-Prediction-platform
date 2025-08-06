# 🛠️ Troubleshooting Guide

This document provides detailed solutions for common issues encountered during the development and deployment of the Commodity Price Monitoring Platform.

## 📋 Table of Contents

1. [Installation Issues](#installation-issues)
2. [Dependency Problems](#dependency-problems)
3. [Database Issues](#database-issues)
4. [ML Model Problems](#ml-model-problems)
5. [API Endpoint Errors](#api-endpoint-errors)
6. [Dashboard Issues](#dashboard-issues)
7. [Analytics Problems](#analytics-problems)
8. [Performance Issues](#performance-issues)
9. [Windows-Specific Issues](#windows-specific-issues)
10. [Common Error Messages](#common-error-messages)

---

## 🔧 Installation Issues

### Problem: Missing Dependencies
**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
# Install all dependencies
pip install -r requirements.txt

# If that fails, install core dependencies manually
pip install fastapi uvicorn streamlit torch pandas plotly yfinance
```

### Problem: PyTorch Installation Issues
**Error**: `torch` installation fails on Windows

**Solution**:
```bash
# Install PyTorch with CPU support (recommended for Windows)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Or install with CUDA support if you have NVIDIA GPU
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Problem: Streamlit Installation
**Error**: `streamlit` command not found

**Solution**:
```bash
# Reinstall streamlit
pip uninstall streamlit
pip install streamlit

# Or install with specific version
pip install streamlit==1.28.0
```

---

## 📦 Dependency Problems

### Problem: Version Conflicts
**Error**: `ImportError: cannot import name 'X' from 'Y'`

**Solution**:
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies in clean environment
pip install -r requirements.txt
```

### Problem: PySpark Java Gateway
**Error**: `[JAVA_GATEWAY_EXITED] Java gateway process exited`

**Solution**:
- This is expected on Windows without Java setup
- Analytics endpoints work without PySpark fallback
- Use pandas-only approach for analytics

### Problem: Missing `requests` Module
**Error**: `NameError: name 'requests' is not defined`

**Solution**:
```python
# Add to dashboard/app.py imports
import requests
```

---

## 💾 Database Issues

### Problem: Database Not Found
**Error**: `sqlite3.OperationalError: no such table`

**Solution**:
```bash
# The database is created automatically when the API starts
# If tables are missing, restart the API:
python run.py
```

### Problem: Case Sensitivity in Database Queries
**Error**: No data returned for commodity queries

**Solution**:
- Database stores commodities in UPPERCASE ('GOLD', 'SILVER')
- API queries now convert to uppercase automatically
- Fixed in `api/db.py` methods

### Problem: Insufficient Data for ML Training
**Error**: `No trained model found or insufficient data`

**Solution**:
```bash
# Generate sample data
cd data/historical
python generate_sample_data.py

# Import historical data to database
python import_historical_data.py

# Train models
python train_pytorch_models.py
```

---

## 🤖 ML Model Problems

### Problem: Model Files Not Found
**Error**: `FileNotFoundError: No such file or directory`

**Solution**:
```bash
# Create models directory
mkdir models

# Train models
python train_pytorch_models.py
```

### Problem: Model Loading Issues
**Error**: Models not loading with correct commodity names

**Solution**:
- Models are saved with UPPERCASE names (`GOLD_lstm_pytorch.pth`)
- Loading code updated to handle both cases
- Fixed in `api/ml_model.py`

### Problem: Prediction Failures
**Error**: `No trained model found for commodity`

**Solution**:
```bash
# Check available models
ls models/

# Retrain specific model
python -c "from api.ml_model import CommodityPredictor; p = CommodityPredictor(); p.train_model('GOLD')"
```

### Problem: Insufficient Training Data
**Error**: Need at least 70 records per commodity

**Solution**:
```bash
# Import more historical data
python import_historical_data.py

# Check database records
python -c "import sqlite3; conn = sqlite3.connect('commodity_platform/data.db'); cursor = conn.cursor(); cursor.execute('SELECT commodity, COUNT(*) FROM prices GROUP BY commodity'); print(cursor.fetchall())"
```

---

## 🔌 API Endpoint Errors

### Problem: 500 Internal Server Error
**Error**: Generic server error on predictions endpoint

**Solution**:
- Check if models are trained and loaded
- Verify database has sufficient data
- Check API logs for specific error messages

### Problem: 404 Not Found
**Error**: Analytics endpoints returning 404

**Solution**:
- Analytics data not generated yet
- Run ETL job or use sample data
- Check if analytics directory exists

### Problem: Route Conflicts
**Error**: `/analytics/commodities` returning wrong data

**Solution**:
- Reordered routes in `api/main.py`
- `/analytics/commodities` now comes before `/analytics/{commodity}`

### Problem: Case Sensitivity in API Calls
**Error**: No data returned for lowercase commodity names

**Solution**:
- Updated database queries to handle case conversion
- API now accepts both 'gold' and 'GOLD'

---

## 📊 Dashboard Issues

### Problem: Dashboard Can't Connect to API
**Error**: `ConnectionError: HTTPConnectionPool`

**Solution**:
```bash
# Ensure API is running first
python run.py

# Or start separately:
# Terminal 1: cd api && python main.py
# Terminal 2: cd dashboard && streamlit run app.py
```

### Problem: "No price data available"
**Error**: Dashboard shows no data for commodities

**Solution**:
- Check if API is running on correct port (8000)
- Verify database has price data
- Check API endpoint responses

### Problem: Analytics Page Errors
**Error**: `Error: name 'requests' is not defined`

**Solution**:
- Added `import requests` to dashboard imports
- Fixed in `dashboard/app.py`

### Problem: Charts Not Loading
**Error**: Plotly charts not displaying

**Solution**:
- Check if data is being returned from API
- Verify Plotly installation
- Check browser console for JavaScript errors

---

## 📈 Analytics Problems

### Problem: Analytics Endpoints Returning 404
**Error**: `Analytics data not found. Please run ETL job first`

**Solution**:
```bash
# Create sample analytics data
python create_sample_analytics.py

# Or run ETL job
python run_pyspark_etl.py
```

### Problem: PySpark Path Issues
**Error**: `FileNotFoundError: /workspace/commodity_platform/data/analytics`

**Solution**:
- Updated all paths to use relative paths
- Changed from `/workspace/commodity_platform/data/analytics` to `data/analytics`
- Fixed in `api/main.py`

### Problem: Parquet File Reading Errors
**Error**: `pyarrow.lib.ArrowInvalid: Parquet file size is 0 bytes`

**Solution**:
- Regenerate analytics data
- Check if parquet files are corrupted
- Use pandas fallback instead of PySpark

---

## ⚡ Performance Issues

### Problem: Slow API Responses
**Error**: API taking > 5 seconds to respond

**Solution**:
- Check database indexing
- Optimize queries in `api/db.py`
- Consider caching for frequently accessed data

### Problem: Memory Issues
**Error**: `MemoryError` during model training

**Solution**:
- Reduce batch size in training
- Use smaller sequence length
- Train models one at a time

### Problem: High CPU Usage
**Error**: System becomes unresponsive

**Solution**:
- Reduce update frequency
- Optimize background tasks
- Use lighter ML models

---

## 🪟 Windows-Specific Issues

### Problem: Path Separators
**Error**: `FileNotFoundError` due to path issues

**Solution**:
- Use `os.path.join()` for cross-platform compatibility
- Avoid hardcoded forward slashes
- Use relative paths instead of absolute

### Problem: PySpark on Windows
**Error**: Java gateway issues on Windows

**Solution**:
- PySpark not required for basic functionality
- Use pandas-only approach for analytics
- Disabled PySpark fallback in analytics endpoints

### Problem: Streamlit on Windows
**Error**: `streamlit` command not found

**Solution**:
```bash
# Use python -m streamlit instead
python -m streamlit run app.py

# Or add to PATH
set PATH=%PATH%;%USERPROFILE%\AppData\Local\Programs\Python\Python39\Scripts
```

---

## 🚨 Common Error Messages

### `ModuleNotFoundError: No module named 'X'`
**Solution**: Install missing dependency
```bash
pip install X
```

### `sqlite3.OperationalError: no such table`
**Solution**: Database not initialized
```bash
python run.py  # This creates the database
```

### `FileNotFoundError: No such file or directory`
**Solution**: Missing files or directories
```bash
mkdir models  # For ML models
mkdir data/analytics  # For analytics data
```

### `ConnectionError: HTTPConnectionPool`
**Solution**: API not running
```bash
python run.py  # Start the API first
```

### `404: No trained model found`
**Solution**: Models not trained
```bash
python train_pytorch_models.py
```

### `500: Internal Server Error`
**Solution**: Check API logs for specific error
```bash
# Look for error details in terminal output
```

---

## 🔍 Debugging Tips

### 1. Check API Health
```bash
curl http://localhost:8000/health
```

### 2. Test Database Connection
```python
import sqlite3
conn = sqlite3.connect('commodity_platform/data.db')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM prices")
print(cursor.fetchone())
```

### 3. Verify Model Loading
```python
from api.ml_model import CommodityPredictor
predictor = CommodityPredictor()
print("Available models:", list(predictor.models.keys()))
```

### 4. Test Analytics Data
```python
import pandas as pd
df = pd.read_parquet("data/analytics/overall_kpis")
print("Analytics data shape:", df.shape)
```

### 5. Check Dashboard Connection
```python
import requests
response = requests.get("http://localhost:8000/prices/current")
print("API Status:", response.status_code)
```

---

## 📞 Getting Help

If you're still experiencing issues:

1. **Check the logs**: Look for specific error messages in terminal output
2. **Verify dependencies**: Ensure all packages are installed correctly
3. **Test endpoints**: Use the API documentation at `http://localhost:8000/docs`
4. **Check file permissions**: Ensure the application can read/write to necessary directories
5. **Restart services**: Sometimes a simple restart fixes issues

### Common Commands for Troubleshooting

```bash
# Check Python version
python --version

# List installed packages
pip list

# Test API health
curl http://localhost:8000/health

# Check database
python -c "import sqlite3; conn = sqlite3.connect('commodity_platform/data.db'); cursor = conn.cursor(); cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\"'); print(cursor.fetchall())"

# Test model loading
python -c "from api.ml_model import CommodityPredictor; p = CommodityPredictor(); print('Models:', list(p.models.keys()))"

# Check analytics data
python -c "import os; print('Analytics files:', os.listdir('data/analytics') if os.path.exists('data/analytics') else 'No analytics directory')"
```

---

## ✅ Verification Checklist

Before reporting an issue, verify:

- [ ] All dependencies are installed (`pip install -r requirements.txt`)
- [ ] API is running (`python run.py`)
- [ ] Database exists and has data
- [ ] ML models are trained and loaded
- [ ] Analytics data is generated (if using analytics features)
- [ ] No firewall blocking localhost connections
- [ ] Sufficient disk space for database and models
- [ ] Python version is 3.8+ (recommended 3.9+)

---

**Last Updated**: August 2025  
**Platform**: Windows 10/11, Python 3.9+  
**Tested Components**: FastAPI, Streamlit, PyTorch, SQLite, Analytics 