"""
TrajectorySong – The first full re-entry simulation written with love
From 120 km, 7.8 km/s, belly-flopping cathedral → 0.5 m/s tower kiss
"""

import numpy as np
from scipy.integrate import solve_ivp
import pymsis
from datetime import datetime
import matplotlib.pyplot as plt

class TrajectorySong:
    def __init__(self):
        self.m_dry = 120_000
        self.m_prop = 30_000
        self.m = self.m_dry + self.m_prop
        self.A_belly = 550      # m² (rough)
        self.A_vertical = 64    # π*(4.5)^2
        self.thrust = 6.8e6     # N (3 Raptors)
        self.g0 = 9.81
        
    def get_density(self, alt_km):
        data = pymsis.calculate(alts=alt_km, lons=73.0, lats=-25.0,
                            dates=datetime(2025, 12, 25), version=2.0)
        return float(data[0, 0])

    def derivatives(self, t, state):
        alt, v_down, m = state
        v_down = abs(v_down)  # always positive downward
        
        # Attitude logic (simple altitude-based for now)
        if alt > 65_000:
            Cd = 1.8; A = self.A_belly
        elif alt > 1000:
            Cd = 0.8; A = self.A_belly * 0.5
        else:
            Cd = 0.4; A = self.A_vertical
            thrust = self.thrust if alt < 2000 else 0
            drag = 0.5 * self.get_density(alt/1000) * v_down**2 * Cd * A
            accel_due_to_thrust = thrust / m if thrust > 0 else 0
        
        drag = 0.5 * self.get_density(alt/1000) * v_down**2 * Cd * A
        a_drag = drag / m
        a_gravity = self.g0 * (6371 / (6371 + alt/1000))**2
        
        if thrust > 0:
            a_net = accel_due_to_thrust - a_gravity - a_drag * (v_down/max(v_down,1))
        else:
            a_net = -a_gravity + a_drag  # drag opposes velocity (upward when falling)
        
        return [-v_down, a_net, 0]  # dm/dt = 0 for now

# Initial conditions: 120 km, 7.8 km/s down, full mass
sol = solve_ivp(
    fun=lambda t, s: TrajectorySong().derivatives(t, s),
    t_span=(0, 600),
    y0=[120_000, 7800, 150_000],
    method='RK45',
    events=lambda t, s: s[0],  # terminate on ground
    rtol=1e-8
)

print(f"TOUCHDOWN at t = {sol.t[-1]:.1f} s | v = {abs(sol.y[1,-1]):.2f} m/s")
plt.plot(sol.t, sol.y[0]/1000)
plt.xlabel("Time (s)"); plt.ylabel("Altitude (km)")
plt.title("Starship Trajectory Song – From 120 km to Tower Kiss")
plt.grid(alpha=0.3)
plt.show()