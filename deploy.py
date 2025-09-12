#!/usr/bin/env python3
"""
Production Deployment Script for AI-Powered Shipment Route Optimization
Created by: Zayeem Khateeb
"""

import os
import sys
from src.dashboard.app import app

def create_production_app():
    """Configure app for production deployment"""
    # Production optimizations
    app.config.update(
        DEBUG=False,
        TESTING=False,
        SECRET_KEY=os.environ.get('SECRET_KEY', 'production-secret-key-change-this'),
    )
    
    return app

if __name__ == '__main__':
    # Get port from environment variable (for cloud deployment)
    port = int(os.environ.get('PORT', 8050))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"🚀 Starting AI-Powered Shipment Route Optimization System")
    print(f"   Created by: Zayeem Khateeb")
    print(f"   Running on: http://{host}:{port}")
    
    production_app = create_production_app()
    production_app.run(host=host, port=port, debug=False)
