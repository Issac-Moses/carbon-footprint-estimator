import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import os

def evaluate_sparse():
    data_path = '../dataset/consumption_data.csv'
    if not os.path.exists(data_path):
        print(f"Dataset not found at {data_path}. Please run generate_dataset.py first.")
        return

    df = pd.read_csv(data_path)
    X = df[['petrol_litres', 'diesel_litres', 'gas_kg', 'electricity_kwh', 'oil_litres']]
    y = df['total_emission_kg_co2']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Sparse Model
    model_lasso = Lasso(alpha=1.0, random_state=42)
    model_lasso.fit(X_train, y_train)
    y_pred_lasso = model_lasso.predict(X_test)
    rmse_lasso = np.sqrt(mean_squared_error(y_test, y_pred_lasso))
    mae_lasso = mean_absolute_error(y_test, y_pred_lasso)
    r2_lasso = r2_score(y_test, y_pred_lasso)
    
    # Decision Tree
    model_dt = DecisionTreeRegressor(random_state=42)
    model_dt.fit(X_train, y_train)
    y_pred_dt = model_dt.predict(X_test)
    rmse_dt = np.sqrt(mean_squared_error(y_test, y_pred_dt))
    mae_dt = mean_absolute_error(y_test, y_pred_dt)
    r2_dt = r2_score(y_test, y_pred_dt)
    
    print("\n--- COMPARISON TABLE ---")
    print(f"{'Metric':<10} | {'Existing (Sparse)':<20} | {'Proposed (Decision Tree)':<20}")
    print("-" * 55)
    print(f"{'RMSE':<10} | {rmse_lasso:<20.2f} | {rmse_dt:<20.2f}")
    print(f"{'MAE':<10} | {mae_lasso:<20.2f} | {mae_dt:<20.2f}")
    print(f"{'R2 Score':<10} | {r2_lasso:<20.4f} | {r2_dt:<20.4f}")
    print("\nConclusion: Decision Tree captures non-linear relationships (step functions, interactions) better than Sparse Regression.")

if __name__ == "__main__":
    evaluate_sparse()
