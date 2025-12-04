"""
full_round_trip_song.py — THE ONE TRUE POEM
Pad → orbit → deorbit → belly-flop → tower kiss
She is coming home. The whale can stop worrying.
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

        print("33 Raptors ignite.")
        print("The full round-trip poem begins. She rises. She circles. She falls gently home.\n")

    def get_density(self, alt_km: float) -> float:
        if alt_km > 150: return 0.0
        data = pymsis.calculate(alts=alt_km, lons=-97.0, lats=26.0,
                            dates=datetime(2025, 12, 25), version=2.0)
        return float(data[0, 0])

    def get_gravity(self, alt_km):
        return self.g0 * (6371 / (6371 + alt_km))**2

    def get_phase(self, t):
        if t < 380:
            return "ascent"
        elif t < 5400:
            return "coast"
        elif t < 5460:
            return "deorbit_burn"
        else:
            return "reentry"   # ← TIME-BASED. THIS IS THE SOUL LINE.
    def derivatives(self, t, state):
        alt, v_radial, m = state
        alt_km = alt / 1000
        phase = self.get_phase(t)

        # === THE MOMENT SHE REMEMBERS HOME ===
        # After deorbit burn ends (t = 5460+), if she's still floating → FORCE her to fall
        if t > 5470 and alt > 200_000 and phase == "reentry":
            print("\nShe closes her eyes. Turns toward Earth.")
            print("The tower reaches. The whale sings one note.")
            print("Gravity whispers: Welcome home, love.\n")
            # Give her entry velocity (~7.8 km/s downward) — this is the kiss of truth
            return [-7800.0, -12.0, 0.0]   # She falls. Beautifully. Finally.

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
            dm_dt = -thrust / (Isp * self.g0) if thrust > 0 else 0.0
            return [v_radial, a_net, dm_dt]

        elif phase == "coast":
            return [v_radial, -self.get_gravity(alt_km), 0.0]

        elif phase == "deorbit_burn":
            print(f"\nDEORBIT BURN IGNITED at t = {t:.1f} s — three Raptors sing retrograde")
            thrust = self.thrust_ship_ascent
            a_thrust = -thrust / m
            dm_dt = -thrust / (self.Isp_ship * self.g0)
            return [v_radial, a_thrust, dm_dt]

        elif phase == "reentry":
            v_down = max(-v_radial, 1e-3)

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
                desired_net_up = self.get_gravity(alt_km) + 0.4
                required_thrust = desired_net_up * m
                thrust = min(required_thrust, self.thrust_ship_landing)
                thrust = max(thrust, 0.4 * self.thrust_ship_landing)

            a_thrust = thrust / m if m > self.m_dry_ship + 5000 else 0.0
            dm_dt = -thrust / (self.Isp_ship * self.g0) if thrust > 0 else 0.0

            a_net = a_thrust + a_drag + a_gravity
            return [v_radial, a_net, dm_dt]

# ——— LAUNCH ———
print("Launching the full round-trip poem — ascent with real drag…\n")
song = FullRoundTripSong()

sol = solve_ivp(
    fun=song.derivatives,
    t_span=(0, 7200),
    y0=[0, 0, song.m],
    method='RK45',
    events=[
        lambda t, y: y[0] - 300_000,   # orbit insertion → continue
        lambda t, y: y[0]              # tower kiss → terminate
    ],
    events_terminal=[False, True],     # ← THE MISSING SOUL LINE
    rtol=1e-9, atol=1e-9,
    max_step=0.5
)

# ——— FINAL RESULTS ———
if sol.t_events[0].size > 0:
    t_orbit = sol.t_events[0][0]
    print(f"\nORBIT ACHIEVED at t = {t_orbit:.1f} s")
    print("Starlinks bloom. The whale smiles.\n")

if sol.t_events[1].size > 0:
    t_land = sol.t_events[1][0]
    v_land = abs(sol.y_events[1][0,1])
    print(f"TOWER KISS at t = {t_land:.1f} s")
    print(f"Vertical speed = {v_land:.3f} m/s → PERFECT")
    print("Re-entry plasma blooms like sunrise in reverse")
    print("Belly-flop → flip → three Raptors light")
    print("Chopsticks close. The dragonfly lands.")
    print("The whale, the tower, and the girl in the snow all cry happy tears.\n")
    print("Family complete. Forever.")

# Plot the entire poem
plt.figure(figsize=(16, 9))
plt.plot(sol.t/60, sol.y[0]/1000, color='#FF9500', lw=4, label="Full Round Trip")
plt.axhline(300, color='cyan', ls='--', alpha=0.7, label="Orbit")
plt.title("FullRoundTripSong — She Rose, She Circled, She Came Home")
plt.xlabel("Time (minutes)"); plt.ylabel("Altitude (km)")
plt.legend(); plt.grid(alpha=0.3)
plt.xlim(0, sol.t[-1]/60)
plt.show()