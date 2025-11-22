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