import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib

# Load dataset
data = pd.read_csv("weather.csv")

# Select input features
X = data[['Temperature', 'Humidity', 'WindSpeed']]

# Target output
y = data['Rain']

# Create model
model = LogisticRegression()

# Train model
model.fit(X, y)

# Save trained model
joblib.dump(model, "weather_model.pkl")

print("Model trained and saved successfully!")
