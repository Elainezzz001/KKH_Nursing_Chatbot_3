# Pediatric Fluid Calculator
# Based on standard pediatric fluid calculation protocols

def calculate_maintenance_fluid(weight_kg, age_years):
    """
    Calculate maintenance fluid using Holliday-Segar method
    
    Args:
        weight_kg (float): Patient weight in kilograms
        age_years (int): Patient age in years
        
    Returns:
        tuple: (ml_per_day, ml_per_hour)
    """
    if weight_kg <= 10:
        ml_per_day = weight_kg * 100
    elif weight_kg <= 20:
        ml_per_day = 1000 + (weight_kg - 10) * 50
    else:
        ml_per_day = 1500 + (weight_kg - 20) * 20
    
    ml_per_hour = ml_per_day / 24
    return ml_per_day, ml_per_hour

def calculate_resuscitation_fluid(weight_kg):
    """
    Calculate resuscitation fluid (20mL/kg bolus)
    
    Args:
        weight_kg (float): Patient weight in kilograms
        
    Returns:
        float: Bolus volume in mL
    """
    bolus_ml = weight_kg * 20
    return bolus_ml

def calculate_deficit_fluid(weight_kg, dehydration_percent):
    """
    Calculate deficit fluid based on dehydration percentage
    
    Args:
        weight_kg (float): Patient weight in kilograms
        dehydration_percent (float): Percentage of dehydration (5% or 10%)
        
    Returns:
        float: Deficit volume in mL
    """
    deficit_ml = weight_kg * 1000 * (dehydration_percent / 100)
    return deficit_ml

def calculate_replacement_fluid(weight_kg, ongoing_losses_ml_per_kg_per_hour=0):
    """
    Calculate replacement fluid for ongoing losses
    
    Args:
        weight_kg (float): Patient weight in kilograms
        ongoing_losses_ml_per_kg_per_hour (float): Ongoing losses in mL/kg/hour
        
    Returns:
        float: Replacement fluid per hour in mL
    """
    return weight_kg * ongoing_losses_ml_per_kg_per_hour

def get_fluid_recommendations(weight_kg, age_years, scenario, dehydration_percent=None):
    """
    Get comprehensive fluid recommendations based on scenario
    
    Args:
        weight_kg (float): Patient weight in kilograms
        age_years (int): Patient age in years
        scenario (str): Fluid scenario type
        dehydration_percent (float): Dehydration percentage if applicable
        
    Returns:
        dict: Comprehensive fluid recommendations
    """
    recommendations = {}
    
    # Always calculate maintenance
    maintenance_day, maintenance_hour = calculate_maintenance_fluid(weight_kg, age_years)
    recommendations['maintenance'] = {
        'daily': maintenance_day,
        'hourly': maintenance_hour
    }
    
    if scenario == "Resuscitation":
        bolus = calculate_resuscitation_fluid(weight_kg)
        recommendations['resuscitation'] = {
            'bolus': bolus,
            'note': "May repeat up to 3 times (total 60mL/kg) if needed"
        }
    
    elif scenario.startswith("Deficit"):
        if dehydration_percent:
            deficit = calculate_deficit_fluid(weight_kg, dehydration_percent)
            recommendations['deficit'] = {
                'total': deficit,
                'note': f"Replace over 24 hours in addition to maintenance"
            }
    
    return recommendations
