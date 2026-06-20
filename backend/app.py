import os
import sys
import sqlite3
import joblib
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from threshold_checker import check_threshold

TEMPLATE_DIR = os.path.join(BASE_DIR, '..', 'frontend', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, '..', 'frontend', 'static')

app = Flask(__name__, 
            template_folder=TEMPLATE_DIR,
            static_folder=STATIC_DIR)

DB_NAME = os.path.join(BASE_DIR, 'emissions.db')
MODEL_PATH = os.path.join(BASE_DIR, '..', 'model', 'carbon_model.pkl')

# Load the trained model
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Warning: Model not found at {MODEL_PATH}. Make sure to run train_model.py first.")
    model = None

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_type TEXT,
            petrol REAL,
            diesel REAL,
            gas REAL,
            electricity REAL,
            oil REAL,
            predicted_emission REAL,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize Database
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/industry', methods=['GET', 'POST'])
def industry():
    if request.method == 'POST':
        return process_submission(request, 'industry')
    return render_template('industry_form.html')

@app.route('/household', methods=['GET', 'POST'])
def household():
    if request.method == 'POST':
        return process_submission(request, 'household')
    return render_template('household_form.html')

def process_submission(req, user_type):
    if not model:
        return "Model is not trained yet! Please run train_model.py.", 500
        
    try:
        petrol = float(req.form.get('petrol', 0))
        diesel = float(req.form.get('diesel', 0))
        gas = float(req.form.get('gas', 0))
        electricity = float(req.form.get('electricity', 0))
        oil = float(req.form.get('oil', 0))
    except ValueError:
        return "Invalid input. Please enter numeric values.", 400

    # Create input DataFrame for prediction
    input_data = pd.DataFrame([[petrol, diesel, gas, electricity, oil]], 
                              columns=['petrol_litres', 'diesel_litres', 'gas_kg', 'electricity_kwh', 'oil_litres'])
    
    # Predict using the Decision Tree model
    predicted_emission = model.predict(input_data)[0]
    
    # Check threshold and get suggestion
    status, suggestion = check_threshold(predicted_emission, user_type)
    
    # Save to database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO submissions 
        (user_type, petrol, diesel, gas, electricity, oil, predicted_emission, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_type, petrol, diesel, gas, electricity, oil, predicted_emission, status))
    conn.commit()
    conn.close()
    
    return render_template('result.html', 
                           user_type=user_type,
                           emission=round(predicted_emission, 2),
                           status=status,
                           suggestion=suggestion)

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM submissions", conn)
    conn.close()
    
    if df.empty:
        return render_template('dashboard.html', chart_url=None, message="No data available yet.")
        
    # Generate chart
    plt.figure(figsize=(10, 6))
    
    # Plot emissions over time for industry vs household
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        industry_df = df[df['user_type'] == 'industry']
        household_df = df[df['user_type'] == 'household']
        
        plt.plot(industry_df['timestamp'], industry_df['predicted_emission'], marker='o', label='Industry', color='orange')
        plt.plot(household_df['timestamp'], household_df['predicted_emission'], marker='s', label='Household', color='green')
        
        plt.xlabel('Timestamp')
        plt.ylabel('Predicted Emission (kg CO2)')
        plt.title('Carbon Emissions Over Time')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        plt.tight_layout()

    # Save to a bytes object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    
    chart_url = base64.b64encode(img.getvalue()).decode('utf8')
    
    return render_template('dashboard.html', chart_url=chart_url, message=None)

if __name__ == '__main__':
    app.run(debug=True)
