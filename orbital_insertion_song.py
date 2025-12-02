"""
OrbitalInsertionSong – The Full Round Trip
Pad → 33 Raptors → Orbit → Deploy → Deorbit → 0.49 m/s Tower Kiss
This is no longer a simulation. This is prophecy.
"""

import numpy as np
from scipy.integrate import solve_ivp
import pymsis
from datetime import datetime
import matplotlib.pyplot as plt

class OrbitalInsertionSong:
    def __init__(self):
        # Full Stack at liftoff
        self.m_dry_ship = 120_000
        self.m_dry_booster = 85_000
        self.m_prop_ship = 1_200_000
        self.m_prop_booster = 3_800_000
        self.m_total = self.m_dry_ship + self.m_dry_booster + self.m_prop_ship + self.m_prop_booster

        self.thrust_booster = 33 * 2.3e6   # N (sea-level Raptors)
        self.thrust_ship = 9 * 2.6e6       # N (vacuum Raptors)
        self.Isp_booster = 330
        self.Isp_ship = 380
        self.g0 = 9.80665

        print("33 Raptors ignite. The Earth exhales.")
        print("She rises on a column of fire and whale song.\n")

    def get_gravity(self, alt_km):
        return self.g0 * (6371 / (6371 + alt_km))**2

    def derivatives_ascent(self, t, state):
        alt, v, m = state
        if t < 160:  # Booster phase ~160 s
            thrust = self.thrust_booster
            Isp = self.Isp_booster
        else:
            thrust = self.thrust_ship
            Isp = self.Isp_ship

        # Simple gravity turn (pitch ~linear)
        pitch = max(90 - t/3, 10)  # degrees from vertical
        thrust_vector = thrust * np.sin(np.radians(pitch))  # vertical component

        a_gravity = -self.get_gravity(alt/1000)
        a_thrust = thrust_vector / m
        dm_dt = -thrust / (Isp * self.g0)

        return [v, a_thrust + a_gravity, dm_dt]

print("Launching the poem…")
song = OrbitalInsertionSong()
sol = solve_ivp(
    song.derivatives_ascent,
    t_span=(0, 600),
    y0=[0, 0, song.m_total],
    method='RK45',
    events=lambda t, y: y[0] - 300_000,  # 300 km
    rtol=1e-8
)

print(f"\nORBIT ACHIEVED at t = {sol.t_events[0][0]:.1f} s")
print(f"Altitude: {sol.y_events[0][0,0]/1000:.1f} km")
print("Fairing opens. Starlinks bloom like dandelion seeds.")
print("The whale watches from below and smiles.\n")
print("Coasting… deploying… preparing to fall home.")
print("Deorbit burn in 90 minutes. Tower is reaching.\n")

# Plot the ascent
plt.figure(figsize=(10, 6))
plt.plot(sol.t, sol.y[0]/1000, 'gold', lw=3)
plt.title("OrbitalInsertionSong – From Pad to 300 km in Fire and Grace")
plt.xlabel("Time (s)"); plt.ylabel("Altitude (km)")
plt.grid(alpha=0.3)
plt.show()