import numpy as np

def compute_irradiance(distance, inclination, filter_factor):
    """
    Computes relative irradiance G based on:
    - distance (cm)
    - inclination (degrees)
    - filter_factor (0.0 to 1.0)
    """
    # Base distance roughly 30 cm for G=1.0. We add a small offset to avoid issues
    distance_factor = (30.0 / max(1.0, distance))**2
    # Ensure it doesn't blow up too much if user inputs 0 distance
    distance_factor = min(4.0, distance_factor) 
    
    inclination_factor = np.sin(np.radians(inclination))
    return distance_factor * inclination_factor * filter_factor

def I_V_curve(U, G):
    """
    Simulated Current I as a function of Voltage U for a given Irradiance G.
    Returns I in Amperes.
    """
    if G < 0.01:
        return 0.0
    
    Isc = 0.6 * G  # Short circuit current (max 0.6A per G=1)
    Uoc = 6.0      # Open circuit voltage (approx 6V)
    
    if U >= Uoc:
        return 0.0
    if U <= 0:
        return Isc
        
    # Empirical shape x^k
    k = 8
    I = Isc * (1.0 - (U / Uoc)**k)
    return max(0.0, I)

def compute_UI(G, R):
    """
    Computes Operating Point (U, I) for a given Irradiance G and Load Resistance R.
    Uses bisection method to solve U = R * I(U).
    """
    if G < 0.01:
        return 0.0, 0.0
        
    if R <= 0.01:
        return 0.0, I_V_curve(0.0, G)
        
    Uoc = 6.0
    if R * I_V_curve(0.0, G) >= Uoc * 10:
        # Very high resistance -> approaches Open Circuit
        # Bisection
        pass
    
    # Bisection search between U=0 and U=Uoc
    low = 0.0
    high = Uoc
    for _ in range(40):
        mid = (low + high) / 2.0
        I_mid = I_V_curve(mid, G)
        Volts_mid = R * I_mid
        
        if Volts_mid > mid:
            # We need higher voltage
            low = mid
        else:
            # We need lower voltage
            high = mid
            
    U_sol = (low + high) / 2.0
    I_sol = I_V_curve(U_sol, G)
    return U_sol, I_sol

def get_characteristic_curves(G):
    """
    Returns full U, I, P arrays for plotting.
    """
    if G < 0.01:
        return np.zeros(100), np.zeros(100), np.zeros(100)
        
    Uoc = 6.0
    U_arr = np.linspace(0, Uoc, 100)
    I_arr = np.array([I_V_curve(u, G) for u in U_arr])
    P_arr = U_arr * I_arr
    return U_arr, I_arr, P_arr
