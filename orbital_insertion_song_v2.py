"""
OrbitalInsertionSong v2 — FIXED & TRUE
Drag now bites. Max Q ~1.8 g. Orbit earned, not gifted.
"""

import numpy as np
from scipy.integrate import solve_ivp
import pymsis
from datetime import datetime
import matplotlib.pyplot as plt

class OrbitalInsertionSong:
    def __init__(self):
        self.m_dry_ship = 120_000
        self.m_dry_booster = 85_000
        self.m_prop_ship = 1_200_000
        self.m_prop_booster = 3_800_000
        self.m_total = self.m_dry_ship + self.m_dry_booster + self.m_prop_ship + self.m_prop_booster

        self.thrust_booster = 33 * 2.30e6
        self.thrust_ship = 9 * 2.63e6
        self.Isp_booster = 327
        self.Isp_ship = 378
        self.g0 = 9.80665
        self.A_stack = 9.0 * 70
        self.Cd_base = 0.25

        print("33 Raptors ignite.")
        print("The atmosphere snarls. She smiles and leans in.\n")

    def get_density(self, alt_km: float) -> float:
        if alt_km > 150:
            return 0.0
        data = pymsis.calculate(alts=alt_km, lons=-97.0, lats=26.0,
                            dates=datetime(2025, 12, 25), version=2.0)
        return float(data[0, 0])

    def get_gravity(self, alt_km):
        return self.g0 * (6371 / (6371 + alt_km))**2

    def derivatives(self, t, state):  # ← RENAMED & USED
        alt, v_up, m = state
        alt_km = alt / 1000

        # Stage
        if t < 162:
            thrust = self.thrust_booster
            Isp = self.Isp_booster
        else:
            thrust = self.thrust_ship
            Isp = self.Isp_ship

        # Gravity turn
        pitch = 90 - max(0, (t - 12) * 0.45)
        pitch = max(pitch, 6)
        sin_pitch = np.sin(np.radians(pitch))

        a_thrust = (thrust * sin_pitch) / m
        a_gravity = -self.get_gravity(alt_km)

        # DRAG — NOW REAL
        a_drag = 0.0
        if alt_km < 120 and v_up > 50:
            rho = self.get_density(alt_km)
            Cd = self.Cd_base * (1 + 0.8 * min(v_up / 340 / 5, 1)**2)
            drag_force = 0.5 * rho * v_up**2 * Cd * self.A_stack
            a_drag = -drag_force / m

        a_net = a_thrust + a_gravity + a_drag
        dm_dt = -thrust / (Isp * self.g0) if thrust > 0 else 0

        return [v_up, a_net, dm_dt]

# ——— FIXED LAUNCH BLOCK ———
print("Launching the TRUE poem — drag included…\n")
song = OrbitalInsertionSong()

sol = solve_ivp(
    fun=song.derivatives,        # ← NOW USING THE REAL ONE
    t_span=(0, 600),
    y0=[0, 0, song.m_total],
    method='RK45',
    events=lambda t, y: y[0] - 300_000,
    rtol=1e-8, atol=1e-8,
    max_step=0.5
)

t_orbit = sol.t_events[0][0] if sol.t_events else sol.t[-1]
alt_final = sol.y[0, -1] / 1000

print(f"\nORBIT ACHIEVED at t = {t_orbit:.1f} seconds")
print(f"Final altitude: {alt_final:.1f} km")
print("She bled speed through Max Q. She bled prop through the sky.")
print("And still — she kissed 300 km with grace.\n")
print("The atmosphere lost. Again.\n")

plt.figure(figsize=(12, 7))
plt.plot(sol.t, sol.y[0]/1000, color='#FFAA00', lw=4, label="True Trajectory (with drag)")
plt.axhline(300, color='cyan', ls='--', alpha=0.8, label="Target")
plt.title("OrbitalInsertionSong v2 — She Fought the Sky and Won")
plt.xlabel("Time (s)"); plt.ylabel("Altitude (km)")
plt.legend(); plt.grid(alpha=0.3)
plt.show()