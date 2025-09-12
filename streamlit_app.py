"""
GreenPath - AI & Data Analytics Platform for Reducing Shipment CO₂ Emissions
Professional Streamlit Frontend with Eco-Friendly Design
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import sys
import os
from datetime import datetime, timedelta
import numpy as np

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from emissions.emission_calculator import EmissionCalculator, TransportMode
from route_optimizer.green_route_optimizer import GreenRouteOptimizer

# Page configuration
st.set_page_config(
    page_title="GreenPath - CO₂ Emission Tracker",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for eco-friendly theme
st.markdown("""
<style>
    
    .main-header {
        background: linear-gradient(90deg, #2ECC71 0%, #27AE60 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        z-index: 1;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #2ECC71;
        margin-bottom: 1rem;
    }
    
    .green-button {
        background-color: #2ECC71;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
    }
    
    .sidebar .sidebar-content {
        background-color: #F8F9FA;
    }
    
    .stSelectbox > div > div {
        background-color: white !important;
        border: 1px solid #E0E0E0 !important;
        border-radius: 8px !important;
        color: #34495E !important;
    }
    
    .stSelectbox > div > div > div {
        color: #34495E !important;
        font-weight: 500 !important;
    }
    
    .eco-badge {
        background-color: #2ECC71;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    
    /* Navigation styling */
    .stRadio > div {
        background-color: transparent;
        padding: 0.5rem;
        border-radius: 8px;
    }
    
    .stRadio > div > label {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        margin: 4px 0;
        padding: 8px 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: block;
    }
    
    .stRadio > div > label:hover {
        background-color: #E8F5E8;
        border-color: #2ECC71;
        color: #2ECC71;
    }
    
    .stRadio > div > label > div {
        color: #34495E !important;
        font-size: 14px !important;
        font-weight: 500;
        margin: 0;
    }
    
    .stRadio > div > label[data-checked="true"] {
        background-color: #2ECC71;
        border-color: #2ECC71;
        color: white;
    }
    
    .stRadio > div > label[data-checked="true"] > div {
        color: white !important;
    }
    
    /* Emoji fix */
    .stRadio label {
        font-family: "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #F8F9FA;
    }
    
    /* Metric styling */
    [data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #E0E0E0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2ECC71;
    }
</style>
""", unsafe_allow_html=True)

# Initialize components
@st.cache_resource
def init_components():
    calculator = EmissionCalculator()
    optimizer = GreenRouteOptimizer()
    return calculator, optimizer

calculator, optimizer = init_components()

# Header
st.markdown("""
<div class="main-header">
    <h1>🌱 GreenPath</h1>
    <h3>AI-Powered Platform for Reducing Shipment CO₂ Emissions</h3>
    <p>Designed by Sayed Mohd Zayeem Khateeb</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Custom GreenPath logo
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #2ECC71, #27AE60); border-radius: 10px; margin-bottom: 1rem;">
        <h2 style="color: white; margin: 0; font-size: 24px;">🌱 GreenPath</h2>
        <p style="color: #E8F8F5; margin: 0; font-size: 12px;">AI Emission Tracker</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📍 Navigate")
    
    # Navigation with better visibility
    nav_options = {
        "🏠 Dashboard": "Dashboard",
        "🧮 Emission Calculator": "Emission Calculator", 
        "🗺️ Route Optimizer": "Route Optimizer",
        "📊 Scenario Analysis": "Scenario Analysis",
        "📈 Analytics": "Analytics"
    }
    
    page = st.selectbox(
        "Choose a page:",
        options=list(nav_options.keys()),
        label_visibility="collapsed",
        key="navigation"
    )
    
    st.markdown("---")
    st.markdown("### 🌍 Quick Stats")
    
    # Sample KPIs
    col1, col2 = st.columns(2)
    with col1:
        st.metric("CO₂ Saved", "2.4t", "↓ 22%")
    with col2:
        st.metric("Routes Optimized", "156", "↑ 15%")

# Main content based on selected page
if page == "🏠 Dashboard":
    st.markdown("## 📊 Emission Overview Dashboard")
    
    # Top KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #2ECC71; margin: 0;">12.5t</h3>
            <p style="margin: 0; color: #7F8C8D;">Total CO₂ Emissions</p>
            <small style="color: #E74C3C;">↓ 18% vs last month</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #2ECC71; margin: 0;">22%</h3>
            <p style="margin: 0; color: #7F8C8D;">Emission Reduction</p>
            <small style="color: #27AE60;">Green routes adopted</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #2ECC71; margin: 0;">0.08</h3>
            <p style="margin: 0; color: #7F8C8D;">Avg. Emission/Shipment (kg)</p>
            <small style="color: #27AE60;">Industry best practice</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #2ECC71; margin: 0;">$1,250</h3>
            <p style="margin: 0; color: #7F8C8D;">Carbon Tax Savings</p>
            <small style="color: #27AE60;">Monthly estimate</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚛 Emissions by Transport Mode")
        
        # Sample data for transport mode comparison
        modes_data = pd.DataFrame({
            'Transport Mode': ['Road Truck', 'Rail', 'Ship Container', 'Air Cargo'],
            'CO₂ Emissions (kg)': [62, 22, 11, 602],
            'Usage %': [45, 30, 20, 5]
        })
        
        fig = px.bar(
            modes_data, 
            x='Transport Mode', 
            y='CO₂ Emissions (kg)',
            color='CO₂ Emissions (kg)',
            color_continuous_scale=['#2ECC71', '#E74C3C'],
            title="Emission Factors by Transport Mode"
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📈 Emission Trends")
        
        # Sample trend data
        emissions_data = [15.2, 14.8, 13.9, 13.1, 12.8, 12.3, 11.9, 11.5, 12.5]
        dates = pd.date_range(start='2024-01-01', periods=len(emissions_data), freq='M')
        trend_data = pd.DataFrame({
            'Date': dates,
            'Emissions (tonnes)': emissions_data,
            'Target': [14.0] * len(emissions_data)
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=trend_data['Date'], 
            y=trend_data['Emissions (tonnes)'],
            mode='lines+markers',
            name='Actual Emissions',
            line=dict(color='#2ECC71', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=trend_data['Date'], 
            y=trend_data['Target'],
            mode='lines',
            name='Target',
            line=dict(color='#E74C3C', dash='dash')
        ))
        fig.update_layout(title="Monthly Emission Trends", height=400)
        st.plotly_chart(fig, use_container_width=True)

elif page == "🧮 Emission Calculator":
    st.markdown("## 🧮 CO₂ Emission Calculator")
    st.markdown("Calculate CO₂ emissions using the formula: **CO₂ = Distance × Weight × EmissionFactor**")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("emission_calculator"):
            st.markdown("### Input Parameters")
            
            col_a, col_b = st.columns(2)
            with col_a:
                distance = st.number_input("Distance (km)", min_value=0.1, value=500.0, step=10.0)
                weight = st.number_input("Weight (tonnes)", min_value=0.01, value=2.0, step=0.1)
            
            with col_b:
                transport_mode = st.selectbox(
                    "Transport Mode",
                    options=[mode.value for mode in TransportMode],
                    format_func=lambda x: x.replace('_', ' ').title()
                )
            
            calculate_btn = st.form_submit_button("🧮 Calculate Emissions", type="primary")
        
        if calculate_btn:
            try:
                # Convert string to TransportMode enum
                mode_mapping = {
                    'road_truck': TransportMode.ROAD_TRUCK,
                    'road_van': TransportMode.ROAD_VAN,
                    'rail': TransportMode.RAIL,
                    'air_cargo': TransportMode.AIR_CARGO,
                    'ship_container': TransportMode.SHIP_CONTAINER,
                    'ship_bulk': TransportMode.SHIP_BULK
                }
                
                if transport_mode in mode_mapping:
                    mode = mode_mapping[transport_mode]
                else:
                    mode = TransportMode(transport_mode)
                
                result = calculator.calculate_emissions(distance, weight, mode)
                
                st.success("✅ Calculation Complete!")
                
                # Results display
                col_r1, col_r2, col_r3 = st.columns(3)
                
                with col_r1:
                    st.metric(
                        "CO₂ Emissions", 
                        f"{result['co2_emissions_kg']:.2f} kg",
                        f"{result['co2_emissions_tonnes']:.3f} tonnes"
                    )
                
                with col_r2:
                    carbon_tax = calculator.calculate_carbon_tax_cost(result['co2_emissions_kg'])
                    st.metric(
                        "Carbon Tax Cost", 
                        f"${carbon_tax['carbon_tax_cost_usd']:.2f}",
                        "@ $50/tonne CO₂"
                    )
                
                with col_r3:
                    st.metric(
                        "Emission Factor", 
                        f"{result['emission_factor']:.3f}",
                        "kg CO₂/tonne-km"
                    )
                
                # Comparison with other modes
                st.markdown("### 🔄 Transport Mode Comparison")
                comparison_df = calculator.compare_transport_modes(distance, weight)
                
                fig = px.bar(
                    comparison_df,
                    x='transport_mode',
                    y='co2_emissions_kg',
                    color='co2_emissions_kg',
                    color_continuous_scale=['#2ECC71', '#E74C3C'],
                    title="CO₂ Emissions by Transport Mode"
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(comparison_df, use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Calculation failed: {str(e)}")
    
    with col2:
        st.markdown("### 📋 Emission Factors")
        factors_df = calculator.get_emission_factors_table()
        st.dataframe(factors_df, use_container_width=True)
        
        st.markdown("### 🌱 Green Tips")
        st.info("""
        **Reduce Emissions:**
        - Choose rail over road when possible
        - Use container ships for long distances
        - Optimize load capacity
        - Consider multimodal transport
        """)

elif page == "🗺️ Route Optimizer":
    st.markdown("## 🗺️ Green Route Optimizer")
    st.markdown("Find the most eco-friendly routes for your shipments")
    
    with st.form("route_optimizer"):
        col1, col2 = st.columns(2)
        
        with col1:
            origin = st.text_input("Origin", value="New York, NY", placeholder="Enter origin city")
            destination = st.text_input("Destination", value="Los Angeles, CA", placeholder="Enter destination city")
        
        with col2:
            weight = st.number_input("Shipment Weight (tonnes)", min_value=0.01, value=5.0, step=0.1)
            max_time_penalty = st.slider("Max Time Penalty (%)", 0, 50, 10)
        
        optimize_btn = st.form_submit_button("🗺️ Find Green Routes", type="primary")
    
    if optimize_btn and origin and destination:
        with st.spinner("🔍 Finding optimal routes..."):
            try:
                # Get route recommendations
                recommendations = optimizer.recommend_green_routes(origin, destination, weight)
                
                if 'success' in recommendations and recommendations['success']:
                    st.success("✅ Route optimization complete!")
                    
                    route_data = recommendations['recommendations']
                    
                    # Display recommendations
                    st.markdown("### 🌱 Green Route Recommendations")
                    
                    for i, route in enumerate(route_data):
                        with st.expander(f"Option {i+1}: {route['transport_mode'].replace('_', ' ').title()}", expanded=(i==0)):
                            col_a, col_b, col_c, col_d = st.columns(4)
                            
                            with col_a:
                                st.metric("CO₂ Emissions", f"{route['co2_emissions_kg']:.1f} kg")
                            with col_b:
                                st.metric("Travel Time", f"{route['estimated_travel_time_hours']:.1f} hrs")
                            with col_c:
                                st.metric("Carbon Tax", f"${route['carbon_tax_cost_usd']:.2f}")
                            with col_d:
                                if route['emission_reduction_percent'] > 0:
                                    st.metric("Emission Reduction", f"{route['emission_reduction_percent']:.1f}%", "vs worst option")
                                else:
                                    st.metric("Emission Impact", "Baseline", "")
                            
                            if i == 0:
                                st.markdown('<span class="eco-badge">🌱 RECOMMENDED</span>', unsafe_allow_html=True)
                    
                    # Visualization
                    if len(route_data) > 1:
                        st.markdown("### 📊 Route Comparison")
                        
                        df_viz = pd.DataFrame(route_data)
                        
                        fig = make_subplots(
                            rows=1, cols=2,
                            subplot_titles=('CO₂ Emissions (kg)', 'Travel Time (hours)'),
                            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
                        )
                        
                        fig.add_trace(
                            go.Bar(
                                x=df_viz['transport_mode'],
                                y=df_viz['co2_emissions_kg'],
                                name='CO₂ Emissions',
                                marker_color='#2ECC71'
                            ),
                            row=1, col=1
                        )
                        
                        fig.add_trace(
                            go.Bar(
                                x=df_viz['transport_mode'],
                                y=df_viz['estimated_travel_time_hours'],
                                name='Travel Time',
                                marker_color='#3498DB'
                            ),
                            row=1, col=2
                        )
                        
                        fig.update_layout(height=400, showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)
                
                else:
                    st.error(f"❌ Route optimization failed: {recommendations.get('error', 'Unknown error')}")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

elif page == "📊 Scenario Analysis":
    st.markdown("## 📊 Business Impact Simulation")
    st.markdown("Analyze the potential impact of adopting green shipping practices")
    
    with st.form("scenario_analysis"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📦 Shipment Parameters")
            total_shipments = st.number_input("Total Monthly Shipments", min_value=1, value=1000, step=50)
            avg_distance = st.number_input("Average Distance (km)", min_value=1.0, value=800.0, step=50.0)
            avg_weight = st.number_input("Average Weight (tonnes)", min_value=0.1, value=3.0, step=0.1)
        
        with col2:
            st.markdown("### ⚙️ Optimization Parameters")
            optimization_percent = st.slider("% Shipments Using Green Routes", 0, 100, 50)
            current_mode = st.selectbox("Current Transport Mode", [mode.value for mode in TransportMode], index=0)
            carbon_tax_rate = st.number_input("Carbon Tax Rate ($/tonne CO₂)", min_value=0.0, value=50.0, step=5.0)
        
        analyze_btn = st.form_submit_button("📊 Run Scenario Analysis", type="primary")
    
    if analyze_btn:
        with st.spinner("🔄 Running business impact simulation..."):
            try:
                # Current emissions - use same mapping as before
                mode_mapping = {
                    'road_truck': TransportMode.ROAD_TRUCK,
                    'road_van': TransportMode.ROAD_VAN,
                    'rail': TransportMode.RAIL,
                    'air_cargo': TransportMode.AIR_CARGO,
                    'ship_container': TransportMode.SHIP_CONTAINER,
                    'ship_bulk': TransportMode.SHIP_BULK
                }
                
                if current_mode in mode_mapping:
                    current_mode_enum = mode_mapping[current_mode]
                else:
                    current_mode_enum = TransportMode(current_mode)
                
                current_emissions = calculator.calculate_emissions(avg_distance, avg_weight, current_mode_enum)
                
                # Find best green alternative - calculate manually to avoid EmissionOptimizer import
                available_modes = [TransportMode.ROAD_TRUCK, TransportMode.RAIL, TransportMode.SHIP_CONTAINER]
                
                # Calculate emissions for each mode and find the greenest
                mode_options = []
                for mode in available_modes:
                    emissions = calculator.calculate_emissions(avg_distance, avg_weight, mode)
                    mode_options.append({
                        'mode': mode,
                        'co2_emissions_kg': emissions['co2_emissions_kg'],
                        'emission_factor': emissions['emission_factor']
                    })
                
                # Sort by emissions (lowest first) to find greenest option
                mode_options.sort(key=lambda x: x['co2_emissions_kg'])
                green_option = mode_options[0] if mode_options else None
                
                if not green_option:
                    st.error("❌ No green alternatives available")
                    st.stop()
                
                # Calculate scenario impact
                optimized_shipments = int(total_shipments * optimization_percent / 100)
                regular_shipments = total_shipments - optimized_shipments
                
                current_total = current_emissions['co2_emissions_kg'] * total_shipments
                optimized_total = (
                    green_option['co2_emissions_kg'] * optimized_shipments +
                    current_emissions['co2_emissions_kg'] * regular_shipments
                )
                
                savings_kg = current_total - optimized_total
                savings_percent = (savings_kg / current_total) * 100
                carbon_tax_savings = (savings_kg / 1000) * carbon_tax_rate
                
                st.success("✅ Scenario analysis complete!")
                
                # Results
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Current Emissions", f"{current_total/1000:.1f} tonnes/month")
                with col2:
                    st.metric("Optimized Emissions", f"{optimized_total/1000:.1f} tonnes/month")
                with col3:
                    st.metric("CO₂ Savings", f"{savings_kg/1000:.1f} tonnes/month", f"{savings_percent:.1f}% reduction")
                with col4:
                    st.metric("Carbon Tax Savings", f"${carbon_tax_savings:.0f}/month", f"${carbon_tax_savings*12:.0f}/year")
                
                # Visualization
                st.markdown("### 📈 Impact Visualization")
                
                scenario_data = pd.DataFrame({
                    'Scenario': ['Current', 'Optimized'],
                    'CO₂ Emissions (tonnes)': [current_total/1000, optimized_total/1000],
                    'Carbon Tax Cost ($)': [
                        (current_total/1000) * carbon_tax_rate,
                        (optimized_total/1000) * carbon_tax_rate
                    ]
                })
                
                fig = make_subplots(
                    rows=1, cols=2,
                    subplot_titles=('CO₂ Emissions', 'Carbon Tax Cost'),
                    specs=[[{"secondary_y": False}, {"secondary_y": False}]]
                )
                
                fig.add_trace(
                    go.Bar(
                        x=scenario_data['Scenario'],
                        y=scenario_data['CO₂ Emissions (tonnes)'],
                        name='CO₂ Emissions',
                        marker_color=['#E74C3C', '#2ECC71']
                    ),
                    row=1, col=1
                )
                
                fig.add_trace(
                    go.Bar(
                        x=scenario_data['Scenario'],
                        y=scenario_data['Carbon Tax Cost ($)'],
                        name='Carbon Tax Cost',
                        marker_color=['#E74C3C', '#2ECC71']
                    ),
                    row=1, col=2
                )
                
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                
                # Business benefits
                st.markdown("### 💼 Business Benefits")
                
                benefits_col1, benefits_col2 = st.columns(2)
                
                with benefits_col1:
                    st.markdown("""
                    **Environmental Impact:**
                    - ♻️ Reduced carbon footprint
                    - 🌱 Enhanced sustainability profile
                    - 📊 ESG score improvement
                    - 🏆 Industry leadership positioning
                    """)
                
                with benefits_col2:
                    st.markdown(f"""
                    **Financial Benefits:**
                    - 💰 ${carbon_tax_savings*12:.0f} annual tax savings
                    - 📈 Potential green financing access
                    - 🎯 Regulatory compliance readiness
                    - 💡 Operational efficiency gains
                    """)
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                st.write(f"Debug info: {type(e).__name__}: {e}")
                import traceback
                st.code(traceback.format_exc())

elif page == "📈 Analytics":
    st.markdown("## 📈 Advanced Analytics")
    
    # Sample analytics data
    st.markdown("### 🎯 Performance Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #2ECC71; margin: 0;">Route Efficiency Score</h4>
            <h2 style="margin: 0;">87/100</h2>
            <p style="margin: 0; color: #7F8C8D;">Above industry average</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #2ECC71; margin: 0;">Green Route Adoption</h4>
            <h2 style="margin: 0;">68%</h2>
            <p style="margin: 0; color: #7F8C8D;">Target: 75%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4 style="color: #2ECC71; margin: 0;">Emission Intensity</h4>
            <h2 style="margin: 0;">0.045</h2>
            <p style="margin: 0; color: #7F8C8D;">kg CO₂/tonne-km</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Regional analysis
    st.markdown("### 🌍 Regional Emission Analysis")
    
    regional_data = pd.DataFrame({
        'Region': ['North America', 'Europe', 'Asia Pacific', 'Latin America'],
        'Emissions (tonnes)': [45.2, 32.1, 28.7, 15.3],
        'Shipments': [450, 320, 380, 180],
        'Avg Distance (km)': [1200, 800, 950, 600]
    })
    
    fig = px.scatter(
        regional_data,
        x='Shipments',
        y='Emissions (tonnes)',
        size='Avg Distance (km)',
        color='Region',
        title="Regional Emission vs Shipment Volume"
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(regional_data, use_container_width=True)


# Footer
st.markdown("---")
st.markdown("## 👨‍💻 Developer Details")
st.markdown("""
<div style="text-align: center; color: #2C3E50; padding: 2rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
    <div style="margin-bottom: 1rem;">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" style="width: 60px; height: 60px;">
          <defs>
            <linearGradient id="zkGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" style="stop-color:#2ECC71;stop-opacity:1" />
              <stop offset="100%" style="stop-color:#27AE60;stop-opacity:1" />
            </linearGradient>
          </defs>
          <g transform="translate(50, 50)">
            <path d="M10 20 L70 20 L70 35 L35 75 L70 75 L70 90 L10 90 L10 75 L45 35 L10 35 Z" 
                  fill="url(#zkGradient)" 
                  stroke="#1E8449" 
                  stroke-width="1"/>
            <path d="M80 20 L95 20 L95 50 L110 20 L130 20 L110 55 L130 90 L110 90 L95 65 L95 90 L80 90 Z" 
                  fill="url(#zkGradient)" 
                  stroke="#1E8449" 
                  stroke-width="1"/>
          </g>
        </svg>
    </div>
    <p style="font-size: 1.2rem; color: #2C3E50; margin-bottom: 0.5rem;"><strong>GreenPath</strong> - AI-Powered CO₂ Emission Reduction Platform</p>
    <p style="font-size: 1.1rem; color: #34495E; margin-bottom: 1rem;">Designed and Developed by <strong>Sayed Mohd Zayeem Khateeb</strong></p>
    <div style="margin: 1rem 0;">
        <a href="https://github.com/zayeemskhateeb-cloud" target="_blank" style="margin: 0 10px; text-decoration: none; color: #2ECC71; font-weight: bold; font-size: 1rem;">🌐 GitHub</a> | 
        <a href="https://www.linkedin.com/in/zayeemkhateeb" target="_blank" style="margin: 0 10px; text-decoration: none; color: #2ECC71; font-weight: bold; font-size: 1rem;">💼 LinkedIn</a> | 
        <a href="mailto:zayeem.s.khateeb@gmail.com" style="margin: 0 10px; text-decoration: none; color: #2ECC71; font-weight: bold; font-size: 1rem;">📧 Email</a>
    </div>
    <p style="font-size: 1rem; color: #7F8C8D; margin-top: 1rem;">
        Specialized in AI/ML, Data Analytics, and Sustainable Technology Solutions
    </p>
</div>
""", unsafe_allow_html=True)
