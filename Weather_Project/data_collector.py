# data_collector.py
import requests
import pandas as pd
from datetime import datetime, timedelta
import json

class WeatherDataCollector:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
    
    def get_current_weather(self, city):
        """Fetch current weather data"""
        url = f"{self.base_url}/weather"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
    
    def get_historical_data(self, lat, lon, start_date, end_date):
        """Fetch historical weather data"""
        # Note: This requires a paid API plan for historical data
        # For demo purposes, we'll generate sample data
        return self.generate_sample_data(start_date, end_date)
    
    def generate_sample_data(self, start_date, end_date):
        """Generate sample historical weather data for demonstration"""
        import numpy as np
        
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        np.random.seed(42)
        
        data = []
        for date in date_range:
            # Generate realistic weather patterns
            base_temp = 20 + 10 * np.sin(2 * np.pi * date.dayofyear / 365)
            temp = base_temp + np.random.normal(0, 5)
            
            data.append({
                'date': date,
                'temperature': round(temp, 1),
                'humidity': np.random.randint(30, 90),
                'pressure': round(np.random.normal(1013, 10), 1),
                'wind_speed': round(np.random.exponential(3), 1),
                'precipitation': max(0, np.random.normal(2, 3))
            })
        
        return pd.DataFrame(data)                                                                                                    