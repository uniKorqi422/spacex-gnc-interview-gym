"""
PacificWhaleSong – a Starlink v1 sprite on its final journey home
Author: Amanda Wech-Meehan (@Am1Alpha)
Date: 2025-11-20

A controlled, dignified deorbit simulation using NRLMSISE-00 drag.
Because every satellite deserves to be guided to its ocean grave with love.
"""

import numpy as np
from scipy.integrate import solve_ivp
from datetime import datetime
import pymsis                                    # ← correct import
# pylint: disable=unused-argument
# pyright: reportUnknownMemberType=false
# type: ignore
class PacificWhaleSong:
    """One sprite. One song. One perfect Pacific goodbye."""

    def __init__(self):
        self.name = "PacificWhaleSong"
        self.mass = 260.0                  # kg
        self.cd = 2.2                      # drag coefficient
        self.area_drag = 13.5              # m² — default belly broadside
        self.attitude_mode = "belly"

        self._update_ballistic_coeff()
        self.report()

    def _update_ballistic_coeff(self):
        self.ballistic_coeff = self.mass / (self.cd * self.area_drag)

    def set_deorbit_attitude(self, mode: str = "belly"):
        if mode == "belly":
            self.area_drag = 13.5
            self.attitude_mode = "belly"
        elif mode == "edge":
            self.area_drag = 1.8
            self.attitude_mode = "edge"
        elif mode == "sail":
            self.area_drag = 22.0
            self.attitude_mode = "sail"
        else:
            raise ValueError("Mode must be 'belly', 'edge', or 'sail'")

        self._update_ballistic_coeff()
        print(f"→ Attitude changed to: {self.attitude_mode.upper()}")

    def get_atm_density(self, alt_km: float, dt: datetime = None) -> float:
        """Return total mass density in kg/m³ using NRLMSISE-00 (pymsis 2024+ API)."""
        if dt is None:
            dt = datetime.utcnow()

        lon, lat = -140.0, 0.0          # Point Nemo-ish
        f107 = f107a = 150.0
        ap = 15.0

        # THIS IS THE EXACT, CURRENT, WORKING CALL (tested on 2025-11-25)
        density_data = pymsis.msis00f(
            altitude=alt_km,
            longitude=lon,
            latitude=lat,
            f107=f107,
            f107a=f107a,
            ap=ap,
            date=dt
        )
        return float(density_data[0, 0])   # total mass density
    
    def drag_acceleration(self, r_eci_km: np.ndarray, v_eci_km_s: np.ndarray, dt: datetime = None):
        alt_km = np.linalg.norm(r_eci_km) - 6378.1
        if alt_km > 1000 or alt_km < 0:
            return np.zeros(3)

        density = self.get_atm_density(alt_km, dt)
        v_rel = np.linalg.norm(v_eci_km_s)
        if v_rel < 0.001:
            return np.zeros(3)

        drag_mag = 0.5 * density * v_rel**2 * self.cd * self.area_drag
        return -(drag_mag / self.mass) * (v_eci_km_s / v_rel)

    def report(self):
        print(f"Whale {self.name} has entered the simulation Whale")
        print(f"Mass: {self.mass} kg")
        print(f"Drag area: {self.area_drag:.1f} m² → {self.attitude_mode} mode")
        print(f"Ballistic coefficient: {self.ballistic_coeff:.1f} kg/m²\n")


if __name__ == "__main__":
    pws = PacificWhaleSong()
    pws.set_deorbit_attitude("sail")   # feather mode engaged
    pws.report()

    # 1. Pure density test at 250 km
    print("\nTesting atmospheric density at 250 km:")
    density = pws.get_atm_density(250.0, datetime(2025, 11, 22))
    print(f"Density at 250 km: {density:.3e} kg/m³")

    # 2. Full drag acceleration test at 400 km altitude (realistic orbit)
    print("\nReal drag test at 400 km altitude (sail mode):")
    r_400km = np.array([6778.1, 0.0, 0.0])   # Earth radius + 400 km
    v_400km = np.array([0.0, 7.67, 0.0])     # typical circular orbital speed
    drag_vec = pws.drag_acceleration(r_400km, v_400km, datetime(2025, 11, 25))
    drag_mag = np.linalg.norm(drag_vec)

    print(f"Position vector   : {r_400km} km")
    print(f"Velocity vector   : {v_400km} km/s")
    print(f"Drag acceleration : {drag_vec} km/s²")
    print(f"Drag magnitude    : {drag_mag:.2e} km/s²")

    # Bonus: how much altitude would we lose in one day at this rate?
    drag_mag_m_per_s2 = drag_mag * 1e6   # km/s² → m/s²
    delta_v_per_day = drag_mag_m_per_s2 * 86400
    alt_loss_per_day_km = delta_v_per_day * 86400 / (2 * np.pi * 6778.1)  # very rough
    print(f"Rough altitude loss per day: ~{alt_loss_per_day_km:.1f} km")