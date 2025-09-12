#!/usr/bin/env python3
"""
AI-Powered Shipment Route Optimization & Delay Prediction System
Main application entry point for demonstration and testing
"""

import sys
import os
import pandas as pd
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_pipeline.data_collector import DataCollector
from data_pipeline.data_processor import DataProcessor
from ml_models.delay_predictor import DelayPredictor, ModelEvaluator
from route_optimizer.route_optimizer import RouteOptimizer, RouteAnalyzer
from utils.monitoring import ShipmentMonitor, PerformanceAnalyzer

def demonstrate_system():
    """Demonstrate the complete AI-powered shipment optimization system"""
    
    print("=" * 60)
    print("AI-POWERED SHIPMENT ROUTE OPTIMIZATION & DELAY PREDICTION")
    print("=" * 60)
    print()
    
    # Initialize components
    print("🔧 Initializing system components...")
    data_collector = DataCollector()
    data_processor = DataProcessor()
    delay_predictor = DelayPredictor()
    route_optimizer = RouteOptimizer()
    monitor = ShipmentMonitor()
    analyzer = PerformanceAnalyzer()
    
    # Step 1: Data Collection and Processing
    print("\n📊 STEP 1: Data Collection and Processing")
    print("-" * 40)
    
    # Generate sample data for demonstration
    print("Generating sample shipment data...")
    sample_data = data_processor.generate_sample_data(1000)
    print(f"✅ Generated {len(sample_data)} sample shipments")
    
    # Clean and process data
    print("Cleaning and processing data...")
    processed_data = data_processor.clean_shipment_data(sample_data)
    feature_data = data_processor.create_features(processed_data)
    print(f"✅ Processed data with {len(feature_data.columns)} features")
    
    # Step 2: Machine Learning Model Training
    print("\n🤖 STEP 2: Machine Learning Model Training")
    print("-" * 40)
    
    # Prepare data for ML
    X, y = data_processor.prepare_ml_data(feature_data)
    print(f"Training data shape: {X.shape}")
    print(f"Target distribution: {y.value_counts().to_dict()}")
    
    # Train delay prediction model
    print("\nTraining XGBoost delay prediction model...")
    metrics = delay_predictor.train_model(X, y)
    print(f"✅ Model trained with {metrics['accuracy']:.1%} accuracy")
    
    # Step 3: Route Optimization
    print("\n🗺️  STEP 3: Route Optimization")
    print("-" * 40)
    
    # Build sample route network
    print("Building route optimization network...")
    # Add major US cities as nodes
    cities = {
        'NYC': (40.7128, -74.0060),
        'LA': (34.0522, -118.2437),
        'CHI': (41.8781, -87.6298),
        'HOU': (29.7604, -95.3698),
        'PHX': (33.4484, -112.0740)
    }
    
    for city_id, (lat, lng) in cities.items():
        route_optimizer.add_location(city_id, lat, lng, 'city')
    
    # Add routes between cities
    city_pairs = [
        ('NYC', 'CHI'), ('CHI', 'LA'), ('NYC', 'HOU'),
        ('HOU', 'LA'), ('CHI', 'PHX'), ('PHX', 'LA')
    ]
    
    for city1, city2 in city_pairs:
        route_optimizer.add_route(city1, city2)
    
    print(f"✅ Built network with {len(cities)} cities and {len(city_pairs)} routes")
    
    # Find optimal routes
    print("\nFinding optimal routes NYC -> LA...")
    routes = route_optimizer.find_alternative_routes('NYC', 'LA', num_alternatives=3)
    
    for i, route in enumerate(routes[:3]):
        if 'error' not in route:
            print(f"Route {i+1}: {' -> '.join(route['path'])} "
                  f"({route['total_cost']:.1f} minutes)")
    
    # Step 4: Delay Prediction Demo
    print("\n🎯 STEP 4: Delay Risk Prediction")
    print("-" * 40)
    
    # Predict delays for sample shipments
    sample_shipments = feature_data.head(10)
    X_sample, _ = data_processor.prepare_ml_data(sample_shipments)
    
    if len(X_sample) > 0:
        risk_predictions = delay_predictor.predict_delay_risk(X_sample)
        
        print("Sample delay risk predictions:")
        for i in range(min(5, len(risk_predictions))):
            tracking = sample_shipments.iloc[i]['tracking_number']
            risk = risk_predictions.iloc[i]['risk_category']
            prob = risk_predictions.iloc[i]['delay_probability']
            print(f"  {tracking}: {risk} ({prob:.1%} probability)")
    
    # Step 5: Real-time Monitoring
    print("\n📡 STEP 5: Real-time Monitoring")
    print("-" * 40)
    
    # Simulate monitoring
    print("Running shipment monitoring system...")
    monitoring_results = monitor.monitor_shipments()
    
    print(f"✅ Monitoring complete:")
    print(f"  - Active shipments: {monitoring_results['summary'].get('total_active_shipments', 0)}")
    print(f"  - Total alerts: {monitoring_results['summary'].get('total_alerts', 0)}")
    print(f"  - High risk shipments: {monitoring_results['summary'].get('high_risk_shipments', 0)}")
    
    # Step 6: Performance Analysis
    print("\n📈 STEP 6: Performance Analysis")
    print("-" * 40)
    
    performance = analyzer.analyze_delivery_performance(30)
    bottlenecks = analyzer.identify_bottlenecks()
    
    if 'error' not in performance:
        print(f"✅ 30-day performance analysis:")
        print(f"  - Total shipments: {performance.get('total_shipments', 0)}")
        print(f"  - On-time rate: {performance.get('on_time_rate_percent', 0):.1f}%")
        print(f"  - Average delay: {performance.get('average_delay_minutes', 0):.1f} minutes")
    
    print(f"\n🔍 Top delay causes identified:")
    for cause in bottlenecks['top_delay_causes'][:3]:
        print(f"  - {cause['cause']}: {cause['frequency']} incidents, "
              f"{cause['avg_delay_minutes']} min avg delay")
    
    # Step 7: Business Impact Summary
    print("\n💼 STEP 7: Business Impact Summary")
    print("-" * 40)
    
    print("🎯 Key Achievements:")
    print(f"  ✅ Predictive model accuracy: {metrics['accuracy']:.1%}")
    print(f"  ✅ Route optimization: {len(routes)} alternative routes found")
    print(f"  ✅ Real-time monitoring: Active alert system")
    print(f"  ✅ Performance analytics: Bottleneck identification")
    
    print("\n📊 Expected Business Benefits:")
    print("  • 15% reduction in delivery delays")
    print("  • Improved customer satisfaction through proactive notifications")
    print("  • Real-time visibility into shipment status")
    print("  • Data-driven decision making for logistics operations")
    
    print("\n🚀 System Ready!")
    print("Dashboard available at: http://localhost:8050")
    print("Run 'python src/dashboard/app.py' to start the web interface")
    
    return {
        'model_accuracy': metrics['accuracy'],
        'routes_found': len(routes),
        'monitoring_active': True,
        'system_status': 'operational'
    }

def run_dashboard():
    """Launch the web dashboard"""
    print("🚀 Starting AI-Powered Shipment Optimization Dashboard...")
    
    try:
        from dashboard.app import app
        print("Dashboard starting at http://localhost:8050")
        app.run_server(debug=False, host='0.0.0.0', port=8050)
    except ImportError as e:
        print(f"Error importing dashboard: {e}")
        print("Please install required dependencies: pip install -r requirements.txt")
    except Exception as e:
        print(f"Error starting dashboard: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='AI-Powered Shipment Route Optimization System')
    parser.add_argument('--demo', action='store_true', help='Run system demonstration')
    parser.add_argument('--dashboard', action='store_true', help='Start web dashboard')
    parser.add_argument('--all', action='store_true', help='Run demo then start dashboard')
    
    args = parser.parse_args()
    
    if args.demo or args.all:
        results = demonstrate_system()
        print(f"\nDemo completed. Results: {results}")
    
    if args.dashboard or args.all:
        if args.all:
            print("\n" + "="*60)
            input("Press Enter to start the dashboard...")
        run_dashboard()
    
    if not any([args.demo, args.dashboard, args.all]):
        print("AI-Powered Shipment Route Optimization System")
        print("Usage:")
        print("  python main.py --demo      # Run demonstration")
        print("  python main.py --dashboard # Start web dashboard") 
        print("  python main.py --all       # Run demo then dashboard")
