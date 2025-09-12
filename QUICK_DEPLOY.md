# 🚀 Quick Deployment Instructions
## AI-Powered Shipment Route Optimization System
**Created by: Zayeem Khateeb**

## ⚡ Instant Deploy Options

### Option 1: Heroku (Recommended - Free Tier Available)
```bash
# 1. Install Heroku CLI from: https://devcenter.heroku.com/articles/heroku-cli
# 2. Login and create app
heroku login
heroku create ai-shipment-optimizer-[your-name]

# 3. Set environment variables
heroku config:set FLASK_ENV=production

## 🌨️ Step 1: Set Up Snowflake

### 1.1 Create Snowflake Account
```sql
-- After signing up, run these commands in Snowflake worksheet:

-- Create database and schema
CREATE DATABASE GREENPATH;
CREATE SCHEMA GREENPATH.EMISSIONS;

-- Create warehouse
CREATE WAREHOUSE COMPUTE_WH WITH
  WAREHOUSE_SIZE = 'X-SMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE;

-- Grant permissions
GRANT USAGE ON DATABASE GREENPATH TO ROLE ACCOUNTADMIN;
GRANT USAGE ON SCHEMA GREENPATH.EMISSIONS TO ROLE ACCOUNTADMIN;
GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE ACCOUNTADMIN;
```

### 1.2 Get Snowflake Connection Details
- **Account**: `your_account.region.cloud` (from Snowflake URL)
- **Username**: Your Snowflake username
- **Password**: Your Snowflake password

## 🌐 Step 2: Deploy to Streamlit Cloud

### 2.1 Push Latest Code to GitHub
```bash
# Commit Snowflake integration
git add .
git commit -m "Add Snowflake integration for enterprise deployment"
git push origin main
```

### 2.2 Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Connect your GitHub account
4. Select repository: `zayeemskhateeb-cloud/greenpath-ai-emission-tracker`
5. Main file path: `streamlit_app.py`
6. Advanced settings → Python version: `3.9`
7. Click **"Deploy!"**

### 2.3 Configure Secrets
In Streamlit Cloud dashboard → App settings → Secrets:

```toml
[snowflake]
account = "your_account.region.cloud"
user = "your_username"
password = "your_password"
database = "GREENPATH"
schema = "EMISSIONS"
warehouse = "COMPUTE_WH"
role = "ACCOUNTADMIN"

[openroute]
api_key = "your_openroute_api_key"  # Optional

[app]
carbon_tax_rate = "50.0"
```

## 🎯 Step 3: Verify Deployment

### 3.1 Your Live Application
- **URL**: `https://your-app-name.streamlit.app`
- **Features**: All GreenPath functionality with Snowflake backend

### 3.2 Test Checklist
- ✅ Dashboard loads with emission metrics
- ✅ CO₂ Calculator works with all transport modes
- ✅ Route Optimizer provides recommendations
- ✅ Business Impact Simulation runs scenarios
- ✅ Analytics display interactive charts
- ✅ Data persists in Snowflake (if configured)

## 🔧 Optional Enhancements

### Enable Snowflake Data Persistence
Update `streamlit_app.py` to use Snowflake models:

```python
# Add at top of streamlit_app.py
import os
if os.getenv('USE_SNOWFLAKE', 'false').lower() == 'true':
    from src.database.snowflake_models import SnowflakeDataManager
    data_manager = SnowflakeDataManager()
```

### Custom Domain (Optional)
- Upgrade to Streamlit Cloud Pro for custom domain
- Configure DNS to point to your Streamlit app

1. **Python not found**: Install Python 3.11+ from python.org
2. **Dependencies fail**: Use `pip install --upgrade pip` first
3. **Port in use**: Change PORT in environment variables
4. **Database issues**: System works with SQLite by default

Your AI-Powered Shipment Route Optimization System is ready to deploy! 🎉

**Created with ❤️ by Zayeem Khateeb**
