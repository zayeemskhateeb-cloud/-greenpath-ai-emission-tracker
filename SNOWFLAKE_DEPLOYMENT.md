# 🌨️ Snowflake Integration for GreenPath Platform

## Overview

This guide explains how to integrate Snowflake as the data warehouse backend for the GreenPath AI CO₂ Emission Reduction Platform. Snowflake will store emission data, analytics, and provide enterprise-scale data processing capabilities.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │    FastAPI      │    │   Snowflake     │
│   Frontend      │◄──►│    Backend      │◄──►│  Data Warehouse │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Deployment Options

### Option 1: Snowflake as Data Backend (Recommended)
Deploy the web app on cloud platforms while using Snowflake for data storage:

**Web App Hosting:**
- **Streamlit Cloud**: Free hosting for Streamlit apps
- **Heroku**: Full-stack deployment
- **AWS/GCP/Azure**: Enterprise deployment

**Data Storage:**
- **Snowflake**: Enterprise data warehouse for emission data, analytics

### Option 2: Snowflake Native Apps (Advanced)
Deploy as a Snowflake Native App (requires Snowflake Native App Framework):

## 📋 Prerequisites

1. **Snowflake Account**: Sign up at [snowflake.com](https://snowflake.com)
2. **Database Setup**: Create database and schema
3. **Credentials**: Obtain account identifier, username, password

## 🔧 Setup Instructions

### Step 1: Snowflake Account Setup

```sql
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

### Step 2: Environment Configuration

```bash
# Copy Snowflake environment template
cp .env.snowflake .env

# Edit .env with your Snowflake credentials
SNOWFLAKE_ACCOUNT=your_account.region.cloud
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
```

### Step 3: Install Dependencies

```bash
pip install snowflake-connector-python snowflake-sqlalchemy
```

### Step 4: Initialize Database Tables

```python
from src.database.snowflake_models import SnowflakeDataManager

# Initialize Snowflake connection and create tables
manager = SnowflakeDataManager()
manager.create_tables()
```

## 🌐 Deployment Scenarios

### Scenario A: Streamlit Cloud + Snowflake

1. **Deploy to Streamlit Cloud:**
   ```bash
   # Push to GitHub
   git add .
   git commit -m "Add Snowflake integration"
   git push origin main
   
   # Deploy via Streamlit Cloud dashboard
   # Connect GitHub repository
   # Add Snowflake credentials to secrets
   ```

2. **Configure Secrets in Streamlit Cloud:**
   ```toml
   # .streamlit/secrets.toml
   [snowflake]
   account = "your_account.region.cloud"
   user = "your_username"
   password = "your_password"
   database = "GREENPATH"
   schema = "EMISSIONS"
   warehouse = "COMPUTE_WH"
   ```

### Scenario B: Heroku + Snowflake

1. **Create Heroku App:**
   ```bash
   heroku create greenpath-emissions
   ```

2. **Set Environment Variables:**
   ```bash
   heroku config:set SNOWFLAKE_ACCOUNT=your_account.region.cloud
   heroku config:set SNOWFLAKE_USER=your_username
   heroku config:set SNOWFLAKE_PASSWORD=your_password
   heroku config:set SNOWFLAKE_DATABASE=GREENPATH
   heroku config:set SNOWFLAKE_SCHEMA=EMISSIONS
   heroku config:set SNOWFLAKE_WAREHOUSE=COMPUTE_WH
   ```

3. **Deploy:**
   ```bash
   git push heroku main
   ```

### Scenario C: Docker + Snowflake

1. **Update docker-compose.yml:**
   ```yaml
   version: '3.8'
   services:
     streamlit:
       build:
         context: .
         dockerfile: Dockerfile.streamlit
       ports:
         - "8501:8501"
       environment:
         - SNOWFLAKE_ACCOUNT=${SNOWFLAKE_ACCOUNT}
         - SNOWFLAKE_USER=${SNOWFLAKE_USER}
         - SNOWFLAKE_PASSWORD=${SNOWFLAKE_PASSWORD}
         - SNOWFLAKE_DATABASE=GREENPATH
         - SNOWFLAKE_SCHEMA=EMISSIONS
         - SNOWFLAKE_WAREHOUSE=COMPUTE_WH
   ```

2. **Deploy:**
   ```bash
   docker-compose up --build
   ```

## 📊 Data Models

### Shipments Table
```sql
CREATE TABLE shipments (
    id STRING PRIMARY KEY,
    origin STRING,
    destination STRING,
    distance_km FLOAT,
    weight_tonnes FLOAT,
    transport_mode STRING,
    co2_emissions_kg FLOAT,
    carbon_tax_cost_usd FLOAT,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
```

### Route Optimizations Table
```sql
CREATE TABLE route_optimizations (
    id STRING PRIMARY KEY,
    shipment_id STRING,
    original_emissions_kg FLOAT,
    optimized_emissions_kg FLOAT,
    emission_reduction_percent FLOAT,
    recommended_mode STRING,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
```

## 🔍 Analytics Queries

### Monthly Emission Trends
```sql
SELECT 
    DATE_TRUNC('month', created_at) as month,
    SUM(co2_emissions_kg) as total_emissions,
    COUNT(*) as shipment_count,
    AVG(co2_emissions_kg) as avg_emissions
FROM shipments 
GROUP BY month 
ORDER BY month;
```

### Transport Mode Comparison
```sql
SELECT 
    transport_mode,
    SUM(co2_emissions_kg) as total_emissions,
    COUNT(*) as shipment_count,
    AVG(co2_emissions_kg) as avg_emissions_per_shipment
FROM shipments 
GROUP BY transport_mode 
ORDER BY total_emissions DESC;
```

## 🚀 Recommended Deployment

For your GreenPath platform, I recommend:

1. **Streamlit Cloud** for web app hosting (free, easy setup)
2. **Snowflake** for data warehouse (enterprise-grade analytics)
3. **GitHub** for version control and CI/CD

This combination provides:
- ✅ Free hosting for the web application
- ✅ Enterprise-grade data storage and analytics
- ✅ Scalable architecture
- ✅ Professional deployment pipeline

## 🔐 Security Best Practices

1. **Use environment variables** for all credentials
2. **Enable MFA** on Snowflake account
3. **Create dedicated service user** for application access
4. **Use least privilege** role assignments
5. **Enable network policies** if required

## 📈 Scaling Considerations

- **Warehouse Size**: Start with X-SMALL, scale as needed
- **Auto-suspend**: Set to 60 seconds to minimize costs
- **Data Retention**: Configure time travel as needed
- **Clustering**: Add clustering keys for large datasets

## 💰 Cost Optimization

- Use **auto-suspend** for warehouses
- Choose appropriate **warehouse sizes**
- Monitor **query performance**
- Use **result caching** where possible

---

**Author**: Sayed Mohd Zayeem Khateeb  
**Contact**: zayeem.s.khateeb@gmail.com
