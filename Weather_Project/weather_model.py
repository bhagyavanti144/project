# weather_model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import joblib

class WeatherPredictor:
    def __init__(self):
        self.models = {
            'temperature': RandomForestRegressor(n_estimators=100, random_state=42),
            'humidity': RandomForestRegressor(n_estimators=100, random_state=42),
            'pressure': GradientBoostingRegressor(n_estimators=100, random_state=42)
        }
        self.scalers = {}
        self.feature_columns = []
        
    def prepare_features(self, df):
        """Create features from historical weather data"""
        df = df.copy()
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Time-based features
        df['day_of_year'] = df['date'].dt.dayofyear
        df['month'] = df['date'].dt.month
        df['day_of_week'] = df['date'].dt.dayofweek
        
        # Lagged features (previous days' values)
        for lag in [1, 2, 3, 7]:
            df[f'temp_lag_{lag}'] = df['temperature'].shift(lag)
            df[f'humidity_lag_{lag}'] = df['humidity'].shift(lag)
            df[f'pressure_lag_{lag}'] = df['pressure'].shift(lag)
        
        # Rolling averages
        for window in [3, 7, 14]:
            df[f'temp_rolling_{window}'] = df['temperature'].rolling(window).mean()
            df[f'humidity_rolling_{window}'] = df['humidity'].rolling(window).mean()
            df[f'pressure_rolling_{window}'] = df['pressure'].rolling(window).mean()
        
        # Seasonal features
        df['temp_seasonal'] = np.sin(2 * np.pi * df['day_of_year'] / 365)
        df['temp_seasonal_cos'] = np.cos(2 * np.pi * df['day_of_year'] / 365)
        
        return df.dropna()
    
    def train(self, df):
        """Train the weather prediction models"""
        # Prepare features
        df_processed = self.prepare_features(df)
        
        # Define feature columns
        self.feature_columns = [col for col in df_processed.columns 
                               if col not in ['date', 'temperature', 'humidity', 'pressure', 'wind_speed', 'precipitation']]
        
        X = df_processed[self.feature_columns]
        
        # Train models for each target variable
        results = {}
        for target in ['temperature', 'humidity', 'pressure']:
            y = df_processed[target]
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, shuffle=False
            )
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            self.scalers[target] = scaler
            
            # Train model
            self.models[target].fit(X_train_scaled, y_train)
            
            # Evaluate
            y_pred = self.models[target].predict(X_test_scaled)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            results[target] = {
                'mse': mse,
                'rmse': np.sqrt(mse),
                'r2': r2
            }
            
            print(f"{target.capitalize()} Model Performance:")
            print(f"  RMSE: {results[target]['rmse']:.2f}")
            print(f"  R²: {results[target]['r2']:.3f}")
            print()
        
        return results
    
    def predict(self, current_data, days_ahead=7):
        """Predict weather for the next few days"""
        predictions = {}
        
        for target in ['temperature', 'humidity', 'pressure']:
            # Prepare features (this would need current weather context)
            # For simplicity, we'll use the most recent data patterns
            features = np.array([[15.5, 6, 1, 20.0, 18.5, 17.2, 19.1, 65, 68, 70, 62, 
                                1015.2, 1014.8, 1013.5, 1016.1, 18.7, 19.2, 19.5, 
                                66.2, 67.1, 65.8, 1014.8, 1015.1, 1014.9, 0.5, 0.8]])
            
            if len(features[0]) != len(self.feature_columns):
                # Pad or truncate to match expected features
                expected_len = len(self.feature_columns)
                if len(features[0]) < expected_len:
                    features = np.pad(features, ((0, 0), (0, expected_len - len(features[0]))), mode='constant')
                else:
                    features = features[:, :expected_len]
            
            # Scale features
            features_scaled = self.scalers[target].transform(features)
            
            # Predict
            pred = self.models[target].predict(features_scaled)[0]
            predictions[target] = round(pred, 1)
        
        return predictions
    
    def save_models(self, filepath):
        """Save trained models"""
        model_data = {
            'models': self.models,
            'scalers': self.scalers,
            'feature_columns': self.feature_columns
        }
        joblib.dump(model_data, filepath)
    
    def load_models(self, filepath):
        """Load trained models"""
        model_data = joblib.load(filepath)
        self.models = model_data['models']
        self.scalers = model_data['scalers']
        self.feature_columns = model_data['feature_columns']
