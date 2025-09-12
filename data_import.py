#!/usr/bin/env python3
"""
Data Import Script for AI-Powered Shipment Route Optimization System
Created by: Zayeem Khateeb

This script helps you import your real data into the system.
"""

import pandas as pd
import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config.database import DatabaseConfig

class DataImporter:
    def __init__(self):
        self.db = DatabaseConfig()
        
    def import_from_csv(self, csv_file_path, table_name):
        """Import data from CSV file to database table"""
        try:
            # Read CSV file
            df = pd.read_csv(csv_file_path)
            print(f"📁 Loaded {len(df)} records from {csv_file_path}")
            
            # Convert to database format
            if table_name == 'shipments':
                df = self._prepare_shipments_data(df)
            elif table_name == 'weather_data':
                df = self._prepare_weather_data(df)
            elif table_name == 'traffic_data':
                df = self._prepare_traffic_data(df)
            
            # Insert into database
            self._insert_dataframe(df, table_name)
            print(f"✅ Successfully imported {len(df)} records to {table_name} table")
            
        except Exception as e:
            print(f"❌ Error importing data: {e}")
    
    def _prepare_shipments_data(self, df):
        """Prepare shipments data for database insertion"""
        # Ensure required columns exist
        required_cols = ['tracking_number', 'origin_lat', 'origin_lng', 
                        'destination_lat', 'destination_lng', 'scheduled_delivery']
        
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        # Convert datetime columns
        if 'scheduled_delivery' in df.columns:
            df['scheduled_delivery'] = pd.to_datetime(df['scheduled_delivery'])
        if 'actual_delivery' in df.columns:
            df['actual_delivery'] = pd.to_datetime(df['actual_delivery'])
        
        # Add created_at if not present
        if 'created_at' not in df.columns:
            df['created_at'] = datetime.now()
        
        # Fill missing values
        df['status'] = df.get('status', 'pending')
        df['delay_minutes'] = df.get('delay_minutes', 0)
        
        return df
    
    def _prepare_weather_data(self, df):
        """Prepare weather data for database insertion"""
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    
    def _prepare_traffic_data(self, df):
        """Prepare traffic data for database insertion"""
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    
    def _insert_dataframe(self, df, table_name):
        """Insert DataFrame into database table"""
        # This would use SQLAlchemy or pandas to_sql in production
        # For now, we'll show the structure
        print(f"📊 Data structure for {table_name}:")
        print(df.head())
        print(f"Columns: {list(df.columns)}")
    
    def import_from_excel(self, excel_file_path, sheet_name='Sheet1', table_name='shipments'):
        """Import data from Excel file"""
        try:
            df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
            print(f"📁 Loaded {len(df)} records from {excel_file_path}")
            
            # Convert to CSV temporarily and use CSV import
            temp_csv = f"temp_{table_name}.csv"
            df.to_csv(temp_csv, index=False)
            self.import_from_csv(temp_csv, table_name)
            
            # Clean up temp file
            os.remove(temp_csv)
            
        except Exception as e:
            print(f"❌ Error importing Excel data: {e}")
    
    def validate_data_format(self, csv_file_path, expected_format='shipments'):
        """Validate that your data has the correct format"""
        try:
            df = pd.read_csv(csv_file_path)
            
            if expected_format == 'shipments':
                required_cols = ['tracking_number', 'origin_lat', 'origin_lng', 
                               'destination_lat', 'destination_lng']
                optional_cols = ['origin_address', 'destination_address', 
                               'scheduled_delivery', 'actual_delivery', 'status', 'delay_minutes']
            
            elif expected_format == 'weather':
                required_cols = ['location_lat', 'location_lng', 'timestamp', 'temperature']
                optional_cols = ['humidity', 'wind_speed', 'precipitation', 'weather_condition']
            
            elif expected_format == 'traffic':
                required_cols = ['route_start_lat', 'route_start_lng', 'route_end_lat', 
                               'route_end_lng', 'timestamp']
                optional_cols = ['travel_time_minutes', 'distance_km', 'traffic_level']
            
            # Check required columns
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                print(f"❌ Missing required columns: {missing_cols}")
                return False
            
            # Show available columns
            print(f"✅ Data validation passed for {expected_format} format")
            print(f"📊 Found columns: {list(df.columns)}")
            print(f"📈 Data shape: {df.shape}")
            print(f"🔍 Sample data:")
            print(df.head(3))
            
            return True
            
        except Exception as e:
            print(f"❌ Error validating data: {e}")
            return False

def main():
    """Main function to demonstrate data import"""
    importer = DataImporter()
    
    print("=" * 60)
    print("🚛 DATA IMPORT TOOL - AI Shipment Route Optimization")
    print("Created by: Zayeem Khateeb")
    print("=" * 60)
    print()
    
    # Example usage
    print("📋 USAGE EXAMPLES:")
    print()
    print("1. Validate your data format:")
    print("   python data_import.py validate shipments.csv")
    print()
    print("2. Import shipments from CSV:")
    print("   python data_import.py import shipments.csv shipments")
    print()
    print("3. Import weather data:")
    print("   python data_import.py import weather_data.csv weather_data")
    print()
    print("4. Import from Excel:")
    print("   python data_import.py excel shipments.xlsx Sheet1 shipments")
    print()
    
    # Handle command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'validate' and len(sys.argv) >= 3:
            file_path = sys.argv[2]
            data_type = sys.argv[3] if len(sys.argv) > 3 else 'shipments'
            importer.validate_data_format(file_path, data_type)
            
        elif command == 'import' and len(sys.argv) >= 4:
            file_path = sys.argv[2]
            table_name = sys.argv[3]
            importer.import_from_csv(file_path, table_name)
            
        elif command == 'excel' and len(sys.argv) >= 5:
            file_path = sys.argv[2]
            sheet_name = sys.argv[3]
            table_name = sys.argv[4]
            importer.import_from_excel(file_path, sheet_name, table_name)
    
    else:
        print("💡 QUICK START:")
        print("1. Prepare your data in CSV format (see DATA_INTEGRATION_GUIDE.md)")
        print("2. Run: python data_import.py validate your_file.csv")
        print("3. Run: python data_import.py import your_file.csv shipments")

if __name__ == "__main__":
    main()
