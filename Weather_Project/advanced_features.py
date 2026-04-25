# advanced_features.py
import numpy as np
from sklearn.ensemble import VotingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR

class AdvancedWeatherPredictor(WeatherPredictor):
    def __init__(self):
        super().__init__()
        # Ensemble models for better predictions
        self.ensemble_models = {}
    
    def create_ensemble_model(self, target):
        """Create ensemble model combining multiple algorithms"""
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        gb = GradientBoostingRegressor(n_estimators=100, random_state=42)
        lr = LinearRegression()
        
        ensemble = VotingRegressor([
            ('rf', rf),
            ('gb', gb),
            ('lr', lr)
        ])
        
        return ensemble
    
    def add_weather_features(self, df):
        """Add advanced meteorological features"""
        df = df.copy()
        
        # Heat index calculation
        df['heat_index'] = self.calculate_heat_index(df['temperature'], df['humidity'])
        
        # Pressure tendency (rate of change)
        df['pressure_tendency'] = df['pressure'].diff()
        
        # Temperature range
        df['temp_range'] = df['temperature'].rolling(7).max() - df['temperature'].rolling(7).min()
        
        return df
    
    def calculate_heat_index(self, temp, humidity):
        """Calculate heat index from temperature and humidity"""
        # Simplified heat index formula
        hi = -42.379 + 2.04901523*temp + 10.14333127*humidity
        hi = hi - 0.22475541*temp*humidity - 6.83783e-3*temp**2
        hi = hi - 5.481717e-2*humidity**2 + 1.22874e-3*temp**2*humidity
        hi = hi + 8.5282e-4*temp*humidity**2 - 1.99e-6*temp**2*humidity**2
        return hi

# Additional utility functions
def create_weather_alerts(predictions):
    """Generate weather alerts based on predictions"""
    alerts = []
    
    for _, row in predictions.iterrows():
        if row['temperature'] > 35:
            alerts.append(f"⚠️ Heat Warning: {row['temperature']:.1f}°C on {row['date'].strftime('%Y-%m-%d')}")
        elif row['temperature'] < -10:
            alerts.append(f"🥶 Cold Warning: {row['temperature']:.1f}°C on {row['date'].strftime('%Y-%m-%d')}")
        
        if row['humidity'] > 90:
            alerts.append(f"💧 High Humidity: {row['humidity']:.1f}% on {row['date'].strftime('%Y-%m-%d')}")
    
    return alerts
