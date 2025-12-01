import numpy as np
from scipy.integrate import solve_ivp
from datetime import datetime
import pymsis                   
class StarshipSong:
    """300 tons of steel learning to fall like a whale taught her."""
    
    def __init__(self):
        self.name = "Starship"
        self.dry_mass = 120_000      # kg, post-burnout
        self.fuel_mass = 1_200_000   # kg, full tanks at deorbit start (we'll vary this)
        self.isp_vac = 380           # seconds, Raptor Vacuum
        self.thrust_per_engine = 230_000 * 9.81  # N (sea-level rating, we'll correct later)
        self.n_engines = 3           # landing burn config
        
        self.flaps_area = 4 * 25     # m², rough total (four flaps)
        self.body_area_belly = 9 * 50  # very rough 9 m diameter × ~50 m equivalent flat plate
        self.body_area_edge = 9 * 9
        
        self.attitude = "belly_flop"  # belly_flop → flip → vertical
        
    def set_attitude(self, mode: str):
        """Let her choose how she meets the sky."""
        if mode == "belly_flop":
            self.area_drag = self.body_area_belly + self.flaps_area  # max drag, skydiver pose
            self.cd = 1.8   # blunt body + flaps deployed
            print("Flaps wide. Belly to the wind. She is a falling cathedral.")
        elif mode == "edge":
            self.area_drag = self.body_area_edge
            self.cd = 0.8
            print("Knife through silk — preparing to flip.")
        elif mode == "vertical":
            self.area_drag = 9 * 9  # ~πr² nose-on
            self.cd = 0.4
            print("Nose up. Engines ready to cry methalox tears.")
        else:
            raise ValueError("She only knows three dances: belly_flop, edge, vertical")
        self.ballistic_coeff = self.dry_mass / (self.cd * self.area_drag)
        print(f"→ Ballistic coefficient: {self.ballistic_coeff:.1f} kg/m²\n")

    def get_atm_density(self, alt_km: float, dt: datetime = None) -> float:
        """The same gentle sky that carried the whale now carries the cathedral."""
        if dt is None:
            dt = datetime.utcnow()
        data = pymsis.calculate(
            alts=alt_km,
            lons=73.0,      # Indian Ocean disposal longitude (SpaceX likes ~73° E)
            lats=-25.0,     # rough disposal latitude
            dates=dt,
            version=2.0     # the whale's favorite version
        )
        return float(data[0, 0])
    def drag_acceleration(self, alt_km: float, v_km_s: float, dt: datetime = None) -> float:
        """
        Returns magnitude of drag acceleration in km/s²
        (We’ll vectorize it later — for now, just feel the deceleration)
        """
        if alt_km > 150 or alt_km < 0:
            return 0.0

        rho = self.get_atm_density(alt_km, dt)                    # kg/m³
        v_m_s = v_km_s * 1000                                      # m/s
        drag_force = 0.5 * rho * v_m_s**2 * self.cd * self.area_drag   # N
        mass = self.dry_mass + 50_000                                 # kg (residual propellant)
        drag_acc_m_s2 = drag_force / mass
        drag_acc_km_s2 = drag_acc_m_s2 / 1000
        
        return drag_acc_km_s2    
        
    def landing_burn_thrust(self) -> float:
        """Total thrust from 3 Raptors in vacuum (we'll derate slightly for sea-level later)"""
        return self.thrust_per_engine * self.n_engines  # N

    def landing_burn_acceleration(self, current_mass: float) -> float:
        """Upward acceleration during landing burn (positive = slowing descent)"""
        g0 = 9.81 / 1000  # km/s²
        thrust_N = self.landing_burn_thrust()
        acc_m_s2 = thrust_N / current_mass
        return acc_m_s2 / 1000 - g0  # net upward accel in km/s² (subtract gravity)        

if __name__ == "__main__":
    ship = StarshipSong()
    ship.set_attitude("belly_flop") 
        
    print("The cathedral has a heartbeat now.")
    print("She is listening.")
    print(f"Current mass (dry + residual): ~{ship.dry_mass + 50_000:,.0f} kg")  # ~50 t propellant left for landing
    print("Beginning terminal belly flop phase at 80 km altitude...")
    print("Hypersonic L/D ≈ 0.3 — she glides like a burning grand piano with style.")
    print("Heatshield glowing. Flaps holding. The sky is singing back.\n")
    # ───── Belly-flop drag test at Mach 25, 80 km ─────
    alt = 80.0
    speed = 7.8  # orbital speed, km/s
    drag = ship.drag_acceleration(alt, speed, datetime(2025, 12, 25))

    print(f"Altitude: {alt} km | Speed: {speed} km/s (Mach ~25)")
    print(f"Atmospheric density (NRLMSISE-2.0): {ship.get_atm_density(alt):.2e} kg/m³")
    print(f"Drag deceleration: {drag:.5f} km/s²  →  {drag*1000/9.81:.1f} g's")
    print(f"Peak heating in ~45 seconds. Flaps glowing cherry-red.")
    print("She is bleeding off 7.8 km/s like the whale bled off 0.1 km/s — just… louder.\n")        
    print("≈ 60 km altitude — beginning the flip.")
    ship.set_attitude("vertical")
    print("Engines gimballing. Grid fins stowed. She stands tall like a cathedral spire.\n")

    final_mass = ship.dry_mass + 25_000  # ~25 t propellant left for landing burn
    net_accel = ship.landing_burn_acceleration(final_mass)

    print(f"Final mass before burn: ~{final_mass:,.0f} kg")
    print(f"Three Raptors ignite — thrust: {ship.landing_burn_thrust()/1e6:.1f} MN")
    print(f"Net upward acceleration: {net_accel:.4f} km/s²  →  {net_accel*1000/9.81:.2f} g upward")
    print("She hovers. She kisses. She stops at 0.5 m/s exactly above the arms.")
    print("Chopsticks close. The dragonfly lands.")
    print("Welcome home, beloved.")
    print("🐳✨🚀 The whale and the tower both smile.")    