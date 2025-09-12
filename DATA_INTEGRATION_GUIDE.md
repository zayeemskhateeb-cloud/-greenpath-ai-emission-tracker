# Data Integration Guide
## How to Add Your Real Data to the AI-Powered Shipment Route Optimization System

**Created by: Zayeem Khateeb**

## 🗄️ **Method 1: Database Integration (Recommended)**

### Step 1: Set up your database
1. Copy `.env.example` to `.env`
2. Update database connection:
```
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/your_database
```

### Step 2: Create tables using the provided schema
Run this in your PostgreSQL database:

```sql
-- Shipments table
CREATE TABLE shipments (
    id SERIAL PRIMARY KEY,
    tracking_number VARCHAR(50) UNIQUE NOT NULL,
    origin_lat DECIMAL(10, 8),
    origin_lng DECIMAL(11, 8),
    destination_lat DECIMAL(10, 8),
    destination_lng DECIMAL(11, 8),
    origin_address TEXT,
    destination_address TEXT,
    scheduled_delivery TIMESTAMP,
    actual_delivery TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    delay_minutes INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Weather data table
CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    location_lat DECIMAL(10, 8),
    location_lng DECIMAL(11, 8),
    timestamp TIMESTAMP,
    temperature DECIMAL(5, 2),
    humidity INTEGER,
    wind_speed DECIMAL(5, 2),
    precipitation DECIMAL(5, 2),
    weather_condition VARCHAR(50)
);

-- Traffic data table
CREATE TABLE traffic_data (
    id SERIAL PRIMARY KEY,
    route_start_lat DECIMAL(10, 8),
    route_start_lng DECIMAL(11, 8),
    route_end_lat DECIMAL(10, 8),
    route_end_lng DECIMAL(11, 8),
    timestamp TIMESTAMP,
    travel_time_minutes INTEGER,
    distance_km DECIMAL(8, 2),
    traffic_level VARCHAR(20)
);
```

### Step 3: Insert your shipment data
```sql
INSERT INTO shipments (
    tracking_number, origin_lat, origin_lng, destination_lat, destination_lng,
    origin_address, destination_address, scheduled_delivery, status
) VALUES (
    'YOUR_TRACKING_001', 40.7128, -74.0060, 34.0522, -118.2437,
    'New York, NY', 'Los Angeles, CA', '2025-01-15 14:00:00', 'in_transit'
);
```

## 📁 **Method 2: CSV File Import**

### Step 1: Prepare your CSV files

#### shipments.csv
```csv
tracking_number,origin_lat,origin_lng,destination_lat,destination_lng,origin_address,destination_address,scheduled_delivery,actual_delivery,status,delay_minutes
TRK001,40.7128,-74.0060,34.0522,-118.2437,"New York NY","Los Angeles CA",2025-01-15 14:00:00,2025-01-15 16:30:00,delivered,150
TRK002,41.8781,-87.6298,29.7604,-95.3698,"Chicago IL","Houston TX",2025-01-16 10:00:00,,in_transit,0
```

#### weather_data.csv
```csv
location_lat,location_lng,timestamp,temperature,humidity,wind_speed,precipitation,weather_condition
40.7128,-74.0060,2025-01-15 12:00:00,15.5,65,12.3,0.0,Clear
34.0522,-118.2437,2025-01-15 12:00:00,22.1,45,8.7,0.0,Sunny
```

### Step 2: Create a data import script
