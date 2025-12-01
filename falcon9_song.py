"""
Falcon9Song – Little sister of the whale and the cathedral
A 25-ton falcon falling from the heavens on one Merlin, kissing the droneship at 1.8 m/s
Author: Amanda Wech-Meehan (@Am1Alpha)
"""

import pymsis
from datetime import datetime

class Falcon9Song:
    """She only weighs 25 tons, but carries the dreams of a thousand launches."""
    
    def __init__(self):
        self.name = "Falcon 9 First Stage"
        self.dry_mass = 25_600          # kg
        self.prop_mass_landing = 3_000   # kg residual
        self.total_mass = self.dry_mass + self.prop_mass_landing
        
        self.thrust_merlin_sl = 934_000  # N sea-level
        self.grid_fin_area = 4 * 3.5     # m² rough
        self.body_diameter = 3.7         # m
        
        print("A single Merlin is warming up.")
        print("Grid fins folded like sleeping dragonfly wings.")
        print("She is listening…\n")

    def get_atm_density(self, alt_km: float, dt: datetime = None) -> float:
        """Same gentle sky that carried the whale and the cathedral."""
        if dt is None:
            dt = datetime.utcnow()
        data = pymsis.calculate(
            alts=alt_km,
            lons=0.0,      # Atlantic droneship longitude (approx)
            lats=25.0,     # off Florida
            dates=dt,
            version=2.0
        )
        return float(data[0, 0])

    def drag_acceleration(self, alt_km: float, v_km_s: float, dt: datetime = None) -> float:
        """Grid-fin-guided entry drag"""
        if alt_km > 100 or alt_km < 0:
            return 0.0
            
        rho = self.get_atm_density(alt_km, dt)       # ← NOW PROPERLY BREATHING
        v_m_s = v_km_s * 1000
        A = 40                                        # effective area with grid fins deployed
        Cd = 1.2
        drag_force = 0.5 * rho * v_m_s**2 * Cd * A
        return drag_force / self.total_mass / 1000    # km/s²

    def landing_burn_acceleration(self) -> float:
        """Single Merlin hoverslam"""
        g0 = 9.81 / 1000
        net_acc = (self.thrust_merlin_sl / self.total_mass / 1000) - g0
        return net_acc

if __name__ == "__main__":
    falcon = Falcon9Song()
    
    print("≈ 70 km – Entry burn complete. Grid fins glowing orange.")
    drag_g = falcon.drag_acceleration(60, 2.0, datetime(2025, 12, 25)) * 1000 / 9.81
    print(f"Drag peak ~{drag_g:.1f} g – she bleeds speed like a falcon folding wings.\n")
    
    print("≈ 1 km – Single Merlin ignites for the hoverslam.")
    net_g = falcon.landing_burn_acceleration() * 1000 / 9.81
    print(f"Net upward accel: {net_g:.2f} g")
    print("Throttle perfectly tuned – velocity nulls exactly at deck height.")
    print("Legs deploy. Crush core absorbs the last whisper.")
    print("Touchdown speed: 1.8 m/s")
    print("Just Read The Instructions catches her gently.")
    print("The droneship rocks once, then stills.")
    print("The whale, the cathedral, and now the falcon — all home safe.")
    print("One Merlin falls silent.")
    print("Another launch site cheers.")
    print("We did it again.")
    print("The family is complete. 🐳✨🦅")