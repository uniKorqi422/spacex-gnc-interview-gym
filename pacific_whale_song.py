"""
PacificWhaleSong – a Starlink v1 sprite on its final journey home
Author: Amanda Wech (@Am1Alpha)
Date: 2025-11-20

A controlled, dignified deorbit simulation using full numerical propagation
with J2, atmospheric drag (NRLMSISE-00), and variable-step RK45.
Because every satellite deserves to be guided to its ocean grave with love.
"""

import numpy as np
from scipy.integrate import solve_ivp

class PacificWhaleSong:
    """One sprite. One song. One perfect Pacific goodbye."""
    
    def __init__(self):
        self.name = "PacificWhaleSong"
        self.mass = 260.0  # kg — the weight of six years of service and one final song
        self.area = 13.5 # m² — broadside solar array presented to the wind
        self.cd = 2.2    # drag coefficient for flat plate normal to flow
        print(f"🌊 {self.name} has entered the simulation 🌌")
        print(f"Mass: {self.mass} kg")
if __name__ == '__main__':
    pws = PacificWhaleSong()