# Carbon Footprint Estimator for Industry and Household

This is a 3rd-year engineering mini project that estimates carbon emissions (CO2) for both industries and households based on their monthly consumption of various energy sources. The system uses a Decision Tree Regression model (proposed system) and compares it against Sparse Regression (existing system) to prove improved accuracy.

## Tech Stack
- **Backend:** Python + Flask
- **ML/Data:** scikit-learn, pandas, numpy, matplotlib, seaborn
- **Database:** SQLite
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Model storage:** joblib/pickle (.pkl file)

## Folder Structure
```
carbon-footprint-estimator/
├── dataset/
│   └── consumption_data.csv
├── model/
│   ├── train_model.py
│   ├── sparse_regression.py
│   └── carbon_model.pkl
├── backend/
│   ├── app.py
│   ├── emission_calculator.py
│   └── threshold_checker.py
├── frontend/
│   ├── templates/
│   │   ├── index.html
│   │   ├── industry_form.html
│   │   ├── household_form.html
│   │   └── result.html
│   └── static/
│       ├── css/style.css
│       └── js/script.js
├── requirements.txt
└── README.md
```

## How to Install
1. Ensure Python 3.8+ is installed.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run
1. Generate the dataset and train the model first:
   ```bash
   cd model
   python generate_dataset.py
   python train_model.py
   ```
2. Start the Flask application:
   ```bash
   cd ../backend
   python app.py
   ```
3. Open a browser and navigate to `http://127.0.0.1:5000/`

## Comparison: Existing vs Proposed System
- **Existing System (Sparse Regression / Lasso):** A linear model with L1 regularization. It may underperform if the underlying data has non-linear noise or complex interactions, leading to higher RMSE and MAE.
- **Proposed System (Decision Tree Regression):** A non-linear tree-based approach. It handles non-linear relationships and captures synthetic variances better, offering a lower error rate (RMSE) and higher R² score compared to the existing system. You can verify this by running `python model/sparse_regression.py`.
