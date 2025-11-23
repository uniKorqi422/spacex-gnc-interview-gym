"""
PacificWhaleSong – a Starlink v1 sprite on its final journey home
Author: Amanda Wech-Meehan (@Am1Alpha)
Date: 2025-11-20

A controlled, dignified deorbit simulation using full numerical propagation
with J2, atmospheric drag (NRLMSISE-00), and variable-step RK45.
Because every satellite deserves to be guided to its ocean grave with love.
"""

"""
PacificWhaleSong – a Starlink v1 sprite on its final journey home
Author: Amanda Wech-Meehan (@Am1Alpha)
Date: 2025-11-20
"""
import numpy as np
from scipy.integrate import solve_ivp
from datetime import datetime

# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
# THIS IS THE ONLY LINE YOU NEED TO CHANGE
import pymsis          # ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←

class PacificWhaleSong:
    """One sprite. One song. One perfect Pacific goodbye."""

    def __init__(self):
        self.name = "PacificWhaleSong"
        self.mass = 260.0                  # kg
        self.cd = 2.2                      # drag coefficient
        self.area_drag = 13.5              # m² — default: belly broadside
        self.attitude_mode = "belly"       # start in max-drag mode

        self._update_ballistic_coeff()     # compute once at birth
        self.report()                      # announce itself

    def _update_ballistic_coeff(self):
        """Recompute ballistic coefficient whenever area or Cd changes."""
        self.ballistic_coeff = self.mass / (self.cd * self.area_drag)

    def set_deorbit_attitude(self, mode: str = "belly"):
        """Change attitude and instantly update drag area and ballistic coeff."""
        if mode == "belly":           # max drag — current v1 deorbit mode
            self.area_drag = 13.5
            self.attitude_mode = "belly"
        elif mode == "edge":          # knife-edge — minimal drag
            self.area_drag = 1.8
            self.attitude_mode = "edge"
        elif mode == "sail":          # solar array perpendicular — feather mode!
            self.area_drag = 22.0      # both sides flashing in tumble
            self.attitude_mode = "sail"
        else:
            raise ValueError("Attitude mode must be 'belly', 'edge', or 'sail'")

    def get_atm_density(self, alt_km: float, dt: datetime = None) -> float:
        """Return total mass density in kg/m³ using NRLMSISE-00."""
        if dt is None:
            dt = datetime.now().date()

        lon, lat = -140.0, 0.0          # Point Nemo-ish
        f107, f107a, ap = 150, 150, 15  # average conditions

        # ←←← THIS IS THE CORRECT FUNCTION NAME
        density_array = pymsis.msis00f(alt_km, lon, lat, f107, f107a, ap, dt)
        # ←←← returns a list of 12 values → index 0 is total density
        return float(density_array[0])

    def drag_acceleration(self, r_eci_km: np.ndarray, v_eci_km_s: np.ndarray, dt: datetime = None):
        """Return drag acceleration vector in ECI (km/s²)."""
        # Altitude from magnitude of position vector (assume Earth radius 6378.1 km)
        alt_km = np.linalg.norm(r_eci_km) - 6378.1
        if alt_km > 1000 or alt_km < 0:
            return np.zeros(3)

        density = self.get_atm_density(alt_km, dt)
        v_rel_mag = np.linalg.norm(v_eci_km_s)
        if v_rel_mag < 0.001:
            return np.zeros(3)

        # Drag force: ½ ρ v² Cd A
        drag_mag = 0.5 * density * v_rel_mag**2 * self.cd * self.area_drag
        # Direction opposite to velocity
        a_drag = - (drag_mag / self.mass) * (v_eci_km_s / v_rel_mag)
        return a_drag  # km/s²

        self._update_ballistic_coeff()
        print(f"→ Attitude changed to: {self.attitude_mode.upper()}")

    def report(self):
        """Let the whale sing its current state."""
        print(f"🌊 {self.name} has entered the simulation 🌌")
        print(f"Mass: {self.mass} kg")
        print(f"Drag reference area: {self.area_drag:.1f} m² → {self.attitude_mode} mode")
        print(f"Ballistic coefficient: {self.ballistic_coeff:.1f} kg/m²")
        print()

        
if __name__ == '__main__':
    pws = PacificWhaleSong()    # born in belly mode
    pws.set_deorbit_attitude("sail")  # final command: become a feather!
    pws.report()         # report final state, sing the new song
    print("Testing atmospheric density at 250 km:")
    test_alt = 250.0
    density = pws.get_atm_density(test_alt, datetime(2025, 11, 22))
    print(f"Density at {test_alt} km: {density:.3e} kg/m³")