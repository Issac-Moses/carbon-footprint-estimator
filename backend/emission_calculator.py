"""
Emission factors source for Indian averages (approximate values used for the project):
- Petrol: 2.31 kg CO2 per litre
- Diesel: 2.68 kg CO2 per litre
- LPG/Gas: 2.98 kg CO2 per kg
- Electricity: 0.82 kg CO2 per kWh
- Oil: 2.52 kg CO2 per litre
"""

def calculate_emission(petrol, diesel, gas, electricity, oil):
    """
    Calculates the total CO2 emission based on consumption of various resources.
    
    Args:
        petrol (float): Petrol consumed in litres.
        diesel (float): Diesel consumed in litres.
        gas (float): Gas (LPG) consumed in kg.
        electricity (float): Electricity consumed in kWh.
        oil (float): Oil consumed in litres.
        
    Returns:
        float: Total CO2 emission in kg.
    """
    # Define emission factors
    factors = {
        'petrol': 2.31,
        'diesel': 2.68,
        'gas': 2.98,
        'electricity': 0.82,
        'oil': 2.52
    }
    
    # Calculate total emission
    total_emission = (
        petrol * factors['petrol'] +
        diesel * factors['diesel'] +
        gas * factors['gas'] +
        electricity * factors['electricity'] +
        oil * factors['oil']
    )
    
    return total_emission
