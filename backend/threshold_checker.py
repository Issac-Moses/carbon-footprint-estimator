def check_threshold(emission_value, user_type):
    """
    Checks if the emission exceeds the allowed threshold for the given user type
    and returns a status and a suggestion.
    
    Args:
        emission_value (float): The calculated or predicted emission in kg CO2.
        user_type (str): 'industry' or 'household'.
        
    Returns:
        tuple: (status, suggestion)
               status is 'Safe' or 'Exceeded'
               suggestion is a human-readable string.
    """
    if user_type == 'household':
        threshold = 500
        if emission_value <= threshold:
            return "Safe", "Great job keeping your carbon footprint low! Continue using energy-efficient appliances."
        else:
            return "Exceeded", "Your household emission is high. Consider renewable energy sources, reducing AC usage, and minimizing personal vehicle usage."
            
    elif user_type == 'industry':
        threshold = 5000
        if emission_value <= threshold:
            return "Safe", "Your industrial emission is within safe limits. Keep optimizing your energy and fuel consumption."
        else:
            return "Exceeded", "Industrial emission limit exceeded! Reduce diesel usage by switching to electric alternatives, and consider energy audits and renewable energy adoption."
            
    else:
        return "Unknown", "No specific suggestions available."
