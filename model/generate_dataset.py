import pandas as pd
import numpy as np
import os

np.random.seed(42)

FACTORS = {
    'petrol': 2.31,
    'diesel': 2.68,
    'gas': 2.98,
    'electricity': 0.82,
    'oil': 2.52
}

def generate_data(num_samples=1000):
    data = []
    for _ in range(num_samples):
        is_industry = np.random.choice([True, False])
        
        if is_industry:
            type_str = 'industry'
            petrol = np.random.uniform(100, 2000)
            diesel = np.random.uniform(500, 5000)
            gas = np.random.uniform(50, 1000)
            electricity = np.random.uniform(1000, 20000)
            oil = np.random.uniform(100, 3000)
        else:
            type_str = 'household'
            petrol = np.random.uniform(10, 200)
            diesel = np.random.uniform(0, 100)
            gas = np.random.uniform(10, 50)
            electricity = np.random.uniform(100, 1000)
            oil = np.random.uniform(0, 50)
            
        # Base calculation
        total_emission = (
            petrol * FACTORS['petrol'] +
            diesel * FACTORS['diesel'] +
            gas * FACTORS['gas'] +
            electricity * FACTORS['electricity'] +
            oil * FACTORS['oil']
        )
        
        # STRONG NON-LINEARITY to break linear models
        if is_industry:
            if diesel > 3000:
                total_emission += 20000  # heavy step function
            elif diesel > 1000:
                total_emission += 5000
                
            if electricity > 10000 and gas > 500:
                total_emission *= 2.0  # interaction term
        else:
            if petrol > 100 and electricity > 500:
                total_emission += 2000
                
        noise_factor = np.random.uniform(0.95, 1.05)
        total_emission *= noise_factor
        
        data.append([
            type_str, round(petrol, 2), round(diesel, 2), round(gas, 2), 
            round(electricity, 2), round(oil, 2), round(total_emission, 2)
        ])
        
    df = pd.DataFrame(data, columns=[
        'type', 'petrol_litres', 'diesel_litres', 'gas_kg', 
        'electricity_kwh', 'oil_litres', 'total_emission_kg_co2'
    ])
    return df

if __name__ == '__main__':
    os.makedirs('../dataset', exist_ok=True)
    df = generate_data(1000)
    save_path = '../dataset/consumption_data.csv'
    df.to_csv(save_path, index=False)
    print(f"Dataset generated successfully at {save_path} with {len(df)} rows.")
