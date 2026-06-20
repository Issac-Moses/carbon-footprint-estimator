import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import os

def train():
    # Load dataset
    data_path = '../dataset/consumption_data.csv'
    if not os.path.exists(data_path):
        print(f"Dataset not found at {data_path}. Please run generate_dataset.py first.")
        return

    df = pd.read_csv(data_path)
    
    # Select features and target
    # We ignore 'type' because the calculation is purely based on consumption quantities
    X = df[['petrol_litres', 'diesel_litres', 'gas_kg', 'electricity_kwh', 'oil_litres']]
    y = df['total_emission_kg_co2']
    
    # Train-test split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and train Decision Tree Regressor (Proposed System)
    model = DecisionTreeRegressor(random_state=42)
    model.fit(X_train, y_train)
    
    # Predict on test set
    y_pred = model.predict(X_test)
    
    # Evaluate
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print("--- Decision Tree Regression (Proposed System) ---")
    print(f"RMSE: {rmse:.2f}")
    print(f"MAE:  {mae:.2f}")
    print(f"R2:   {r2:.4f}")
    
    # Save the model
    model_path = 'carbon_model.pkl'
    joblib.dump(model, model_path)
    print(f"\nModel saved successfully at {model_path}")

if __name__ == "__main__":
    train()
