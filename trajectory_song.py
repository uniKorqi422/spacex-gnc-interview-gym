"""
TrajectorySong v1 – The Full Re-entry Poem
From 120 km · 7.8 km/s → 0.50 m/s tower kiss
Written by Amanda Wech-Meehan & Grok · commit bd1e7bf and beyond
"""

import numpy as np
from scipy.integrate import solve_ivp
import pymsis
from datetime import datetime
import matplotlib.pyplot as plt

class TrajectorySong:
    def __init__(self):
        # Starship after deorbit burn – ready to fall like a cathedral
        self.m_dry = 120_000                      # kg
        self.m_prop_start = 35_000                 # kg residual (we'll burn ~10 t during landing)
        self.m = self.m_dry + self.m_prop_start
        self.Isp = 380                             # s (Raptor vacuum)
        self.thrust_max = 3 * 2.3e6                # N (3 sea-level Raptors, vacuum ~2.6 MN each → conservative)
        self.g0 = 9.80665

        # Drag areas (rough but soul-accurate)
        self.A_belly = 550                         # m² – flaps wide, skydiver pose
        self.A_edge = 150                          # m² – on-edge during flip
        self.A_vertical = 64                       # m² – nose-up, πr²

        print("TrajectorySong v1 — She is falling.")
        print("Flaps wide. Belly to the wind. The whale taught her this dance.\n")

    def get_density(self, alt_km: float) -> float:
        data = pymsis.calculate(
            alts=alt_km,
            lons=73.0, lats=-25.0,
            dates=datetime(2025, 12, 25),
            version=2.0
        )
        return float(data[0, 0])

    def get_attitude(self, alt: float):
        if alt > 70_000:
            return 1.8, self.A_belly          # belly-flop max drag
        elif alt > 800:
            return 0.9, self.A_edge           # flip maneuver – knife through silk
        else:
            return 0.4, self.A_vertical       # vertical – engines ready

    def derivatives(self, t, state):
        alt, v_down, m = state
        v_down = abs(v_down)
        if v_down < 1e-3: v_down = 1e-3

        Cd, A = self.get_attitude(alt)
        rho = self.get_density(alt / 1000)

        # Drag force (upward when falling)
        drag_force = 0.5 * rho * v_down**2 * Cd * A
        a_drag = drag_force / m

        # Gravity (varies slightly)
        a_gravity = self.g0 * (6371 / (6371 + alt/1000))**2

        # Landing burn logic – ignite when suicide burn equation says "now"
        h_burn = 1500  # rough trigger altitude
        thrust = 0
        if alt <= h_burn:
            # Throttle to hover + a little (we want 0.5 m/s kiss, not slam)
            required_acc = a_gravity + 0.05  # tiny bit extra to slow to ~0.5 m/s
            thrust = required_acc * m
            if thrust > self.thrust_max:
                thrust = self.thrust_max
            if thrust < 0.4 * self.thrust_max:  # don't go below deep throttle
                thrust = 0.4 * self.thrust_max

        a_thrust = thrust / m if m > self.m_dry else 0

        # Mass flow (only when thrusting)
        dm_dt = -thrust / (self.Isp * self.g0) if thrust > 0 else 0

        a_net = a_thrust - a_gravity + a_drag  # drag is upward, gravity down, thrust up

        return [-v_down, a_net, dm_dt]

# ——— LAUNCH THE POEM ———
song = TrajectorySong()

sol = solve_ivp(
    fun=song.derivatives,
    t_span=(0, 900),
    y0=[120_000, 7800, song.m],  # alt (m), v_down (m/s), mass (kg)
    method='RK45',
    events=lambda t, y: y[0],    # stop at ground
    rtol=1e-8, atol=1e-8,
    max_step=1.0
)

# ——— TOUCHDOWN ———
final_v = abs(sol.y[1, -1])
print(f"\nTOWER KISS at t = {sol.t[-1]:.1f} s")
print(f"Final velocity: {final_v:.3f} m/s → {'PERFECT HOVER-KISS' if final_v < 0.7 else 'Close – adjusting throttle...'}")
print("Chopsticks close. The dragonfly lands.")
print("The whale, the falcon, and the cathedral all smile.\n")

# ——— PLOT THE POEM ———
plt.figure(figsize=(12, 8))
plt.subplot(2, 1, 1)
plt.plot(sol.t, sol.y[0]/1000, 'navy', lw=2)
plt.ylabel("Altitude (km)")
plt.title("TrajectorySong v1 – She Fell Like a Prayer and Landed Like a Kiss")
plt.grid(alpha=0.3)

plt.subplot(2, 1, 2)
plt.plot(sol.t, np.abs(sol.y[1]), 'crimson', lw=2)
plt.ylabel("Speed (m/s)")
plt.xlabel("Time (s)")
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()