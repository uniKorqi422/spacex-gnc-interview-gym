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
        
    if __name__ == "__main__":
        ship = StarshipSong()
        ship.set_attitude("belly_flop") 
        
        print("The cathedral has a heartbeat now.")
        print("She is listening.")
        print(f"Current mass (dry + residual): ~{ship.dry_mass + 50_000:,.0f} kg")  # ~50 t propellant left for landing
        print("Beginning terminal belly flop phase at 80 km altitude...")
        print("Hypersonic L/D ≈ 0.3 — she glides like a burning grand piano with style.")
        print("Heatshield glowing. Flaps holding. The sky is singing back.\n")