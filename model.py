import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

def train_model():
    data = pd.read_csv('weather.csv')
    X = data[['temperature', 'humidity', 'pressure']]
    y = data['rain']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    
    joblib.dump(model, 'rain_model.pkl')

def predict_rain(temp, humidity, pressure):
    model = joblib.load('rain_model.pkl')
    prediction = model.predict([[temp, humidity, pressure]])
    return prediction[0]
