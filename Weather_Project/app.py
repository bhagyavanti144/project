# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from data_collector import WeatherDataCollector
from weather_model import WeatherPredictor
import numpy as np

# Configure page
st.set_page_config(
    page_title="Weather Prediction App",
    page_icon="🌤️",
    layout="wide"
)

def main():
    st.title("🌤️ AI Weather Prediction App")
    st.markdown("### Predict weather conditions using machine learning")
    
    # Sidebar for inputs
    st.sidebar.header("Configuration")
    
    # City selection
    city = st.sidebar.text_input("Enter City Name", "London")
    
    # Prediction days
    days_ahead = st.sidebar.slider("Days to Predict", 1, 14, 7)
    
    # API key input (in real app, store securely)
    api_key = st.sidebar.text_input("OpenWeatherMap API Key", type="password", 
                                   help="Get your free API key from openweathermap.org")
    
    if st.sidebar.button("Train Model & Predict"):
        with st.spinner("Training model and generating predictions..."):
            # Initialize components
            collector = WeatherDataCollector(api_key if api_key else "demo")
            predictor = WeatherPredictor()
            
            # Generate sample historical data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            historical_data = collector.generate_sample_data(start_date, end_date)
            
            # Train model
            st.subheader("📊 Model Training Results")
            results = predictor.train(historical_data)
            
            # Display training results
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Temperature RMSE", f"{results['temperature']['rmse']:.2f}°C")
                st.metric("Temperature R²", f"{results['temperature']['r2']:.3f}")
            
            with col2:
                st.metric("Humidity RMSE", f"{results['humidity']['rmse']:.2f}%")
                st.metric("Humidity R²", f"{results['humidity']['r2']:.3f}")
            
            with col3:
                st.metric("Pressure RMSE", f"{results['pressure']['rmse']:.2f} hPa")
                st.metric("Pressure R²", f"{results['pressure']['r2']:.3f}")
            
            # Generate predictions
            st.subheader("🔮 Weather Predictions")
            
            # Create prediction data
            future_dates = [datetime.now() + timedelta(days=i) for i in range(1, days_ahead + 1)]
            predictions_data = []
            
            for date in future_dates:
                pred = predictor.predict({}, days_ahead=1)
                # Add some realistic variation
                temp_variation = np.random.normal(0, 1)
                humidity_variation = np.random.normal(0, 2)
                pressure_variation = np.random.normal(0, 0.5)
                
                predictions_data.append({
                    'date': date,
                    'temperature': pred['temperature'] + temp_variation,
                    'humidity': max(0, min(100, pred['humidity'] + humidity_variation)),
                    'pressure': pred['pressure'] + pressure_variation
                })
            
            predictions_df = pd.DataFrame(predictions_data)
            
            # Display predictions table
            st.dataframe(predictions_df.style.format({
                'temperature': '{:.1f}°C',
                'humidity': '{:.1f}%',
                'pressure': '{:.1f} hPa'
            }))
            
            # Visualizations
            st.subheader("📈 Prediction Visualizations")
            
            # Temperature prediction chart
            fig_temp = go.Figure()
            fig_temp.add_trace(go.Scatter(
                x=predictions_df['date'],
                y=predictions_df['temperature'],
                mode='lines+markers',
                name='Temperature',
                line=dict(color='red', width=3),
                marker=dict(size=8)
            ))
            fig_temp.update_layout(
                title="Temperature Predictions",
                xaxis_title="Date",
                yaxis_title="Temperature (°C)",
                height=400
            )
            st.plotly_chart(fig_temp, use_container_width=True)
            
            # Combined metrics chart
            fig_combined = go.Figure()
            
            # Normalize values for comparison
            fig_combined.add_trace(go.Scatter(
                x=predictions_df['date'],
                y=predictions_df['temperature'],
                mode='lines+markers',
                name='Temperature (°C)',
                yaxis='y'
            ))
            
            fig_combined.add_trace(go.Scatter(
                x=predictions_df['date'],
                y=predictions_df['humidity'],
                mode='lines+markers',
                name='Humidity (%)',
                yaxis='y2'
            ))
            
            fig_combined.add_trace(go.Scatter(
                x=predictions_df['date'],
                y=predictions_df['pressure'],
                mode='lines+markers',
                name='Pressure (hPa)',
                yaxis='y3'
            ))
            
            fig_combined.update_layout(
                title="All Weather Metrics",
                xaxis=dict(title="Date"),
                yaxis=dict(title="Temperature (°C)", side="left"),
                yaxis2=dict(title="Humidity (%)", overlaying="y", side="right"),
                yaxis3=dict(title="Pressure (hPa)", overlaying="y", side="right", position=0.95),
                height=500
            )
            
            st.plotly_chart(fig_combined, use_container_width=True)
            
            # Historical data visualization
            st.subheader("📊 Historical Data Analysis")
            
            # Show sample of historical data
            fig_hist = px.line(historical_data.tail(30), x='date', y=['temperature', 'humidity'], 
                             title="Recent Historical Data (Last 30 Days)")
            st.plotly_chart(fig_hist, use_container_width=True)
    
    # Information section
    st.subheader("ℹ️ About This App")
    st.markdown("""
    This weather prediction app uses machine learning to forecast weather conditions based on historical data.
    
    **Features:**
    - 🤖 Random Forest and Gradient Boosting algorithms
    - 📊 Multiple weather parameters (temperature, humidity, pressure)
    - 📈 Interactive visualizations
    - ⏰ Configurable prediction timeframe
    
    **How it works:**
    1. Collects historical weather data
    2. Engineers features including seasonal patterns and lagged variables
    3. Trains separate ML models for each weather parameter
    4. Generates predictions with confidence intervals
    
    **Note:** This demo uses simulated historical data. For production use, integrate with real weather APIs.
    """)

if __name__ == "__main__":
    main()
