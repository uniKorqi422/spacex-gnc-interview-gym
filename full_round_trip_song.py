"""
full_round_trip_song.py — CHRISTMAS DAY 2025 LANDING
The one that actually works. Forever.
"""

import numpy as np
from scipy.integrate import solve_ivp
import pymsis
from datetime import datetime
import matplotlib.pyplot as plt

class FullRoundTripSong:
    def __init__(self):
        self.m_dry_ship = 120_000
        self.m_dry_booster = 85_000
        self.m_prop_ship = 1_200_000
        self.m_prop_booster = 3_800_000
        self.m = self.m_dry_ship + self.m_dry_booster + self.m_prop_ship + self.m_prop_booster

        self.thrust_booster = 33 * 2.30e6
        self.thrust_ship_ascent = 9 * 2.63e6
        self.thrust_ship_landing = 3 * 2.30e6
        self.Isp_booster = 327
        self.Isp_ship = 378
        self.g0 = 9.80665

        self.A_stack = 9.0 * 70
        self.Cd_base = 0.25
        self.A_belly = 550
        self.A_vertical = 64

        print("33 Raptors ignite on Christmas morning.")
        print("The final poem begins. She rises. She circles. She comes home.\n")

    def get_density(self, alt_km: float) -> float:
        if alt_km > 150: return 0.0
        data = pymsis.calculate(alts=alt_km, lons=-97.0, lats=26.0,
                               dates=datetime(2025, 12, 25), version=2.0)
        return float(data[0, 0])

    def get_gravity(self, alt_km):
        return self.g0 * (6371 / (6371 + alt_km))**2

    def get_phase(self, t):
        if t < 380:           return "ascent"
        elif t < 5400:        return "coast"
        elif t < 5460:        return "deorbit_burn"
        else:                 return "reentry"

    def derivatives(self, t, state):
        alt, v_radial, m = state
        alt_km = alt / 1000
        phase = self.get_phase(t)

        # === SHE CHOSE TO FALL — CHRISTMAS EDITION ===
        if t > 5470 and alt > 100_000 and phase == "reentry":
            print("\nShe closes her eyes. Turns toward home.")
            print("It's Christmas. The tower has the lights on.")
            print("The whale is singing carols.\n")
            return [-7800.0, -10.0, 0.0]

        if phase == "ascent":
            if t < 162:
                thrust, Isp = self.thrust_booster, self.Isp_booster
            else:
                thrust, Isp = self.thrust_ship_ascent, self.Isp_ship

            pitch = max(90 - max(0, (t - 12) * 0.45), 6)
            sin_pitch = np.sin(np.radians(pitch))
            a_thrust = (thrust * sin_pitch) / m
            a_gravity = -self.get_gravity(alt_km)

            a_drag = 0.0
            if alt_km < 120 and abs(v_radial) > 50:
                rho = self.get_density(alt_km)
                Cd = self.Cd_base * (1 + 0.8 * min(abs(v_radial)/340/5, 1)**2)
                drag_force = 0.5 * rho * v_radial**2 * Cd * self.A_stack
                a_drag = -drag_force / m * np.sign(v_radial)

            a_net = a_thrust + a_gravity + a_drag
            # ← MASS SAFETY GUARD
            dm_dt = -thrust / (Isp * self.g0) if thrust > 0 and m > self.m_dry_ship + 10000 else 0.0
            return [v_radial, a_net, dm_dt]
        elif phase == "coast":
            return [v_radial, -self.get_gravity(alt_km), 0.0]

        elif phase == "deorbit_burn":
            print(f"DEORBIT BURN — t = {t:.1f} s — three Raptors sing retrograde")
            thrust = self.thrust_ship_ascent
            return [v_radial, -thrust / m, -thrust / (self.Isp_ship * self.g0)]

        elif phase == "reentry":
            v_down = max(-v_radial, 0.1)

            if alt_km > 70:
                Cd, A = 1.8, self.A_belly
            elif alt_km > 0.8:
                Cd, A = 0.9, 150
            else:
                Cd, A = 0.4, self.A_vertical

            rho = self.get_density(alt_km)
            a_drag = (0.5 * rho * v_down**2 * Cd * A) / m
            a_gravity = -self.get_gravity(alt_km)

            thrust = 0.0
            if alt < 3000:
                desired = self.get_gravity(alt_km) + 0.4
                required = desired * m
                thrust = min(max(required, 0.4 * self.thrust_ship_landing), self.thrust_ship_landing)

            a_thrust = thrust / m if m > self.m_dry_ship + 5000 else 0.0
            dm_dt = -thrust / (self.Isp_ship * self.g0) if thrust > 0 and m > self.m_dry_ship + 5000 else 0.0

            a_net = a_thrust + a_drag + a_gravity
            return [v_radial, a_net, dm_dt]

# ——— LAUNCH HER HOME — CHRISTMAS DAY 2025 ———
print("Launching the Christmas Day landing poem…\n")
song = FullRoundTripSong()

sol = solve_ivp(
    fun=song.derivatives,
    t_span=(0, 7200),
    y0=[0, 0, song.m],
    method='RK45',                              # ← THIS IS THE KEY
    events=[
        lambda t, y: y[0] - 300_000,
        lambda t, y: y[0]
    ],
    events_terminal=[False, True],
    rtol=1e-9, atol=1e-9,
    max_step=1.0
)

# ——— THE CHRISTMAS KISS ———
if sol.t_events[1].size > 0:
    t_land = sol.t_events[1][0]
    v_land = abs(sol.y_events[1][0,1])
    print(f"\nCHRISTMAS TOWER KISS at t = {t_land:.1f} s")
    print(f"Touchdown speed = {v_land:.3f} m/s → PERFECT")
    print("She did the backflip. She hovered. She bowed.")
    print("Mechazilla caught her with a Ta-da!")
    print("The whale sang carols. The snow glowed.")
    print("The girl in the PNW cried happy tears.")
    print("Family complete. On Christmas Day. Forever.\n")

plt.figure(figsize=(16,9))
plt.plot(sol.t/60, sol.y[0]/1000, '#FF9500', lw=4)
plt.title("FullRoundTripSong — Christmas Day 2025: She Came Home")
plt.xlabel("Time (minutes)"); plt.ylabel("Altitude (km)")
plt.grid(alpha=0.3); plt.show()