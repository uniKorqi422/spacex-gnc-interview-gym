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
    if __name__ == "__main__":
        ship = StarshipSong()
        ship.set_attitude("belly_flop") 
        
        print(f"→ Ballistic coefficient: {self.ballistic_coeff:.1f} kg/m²\n")
        print("The cathedral has a heartbeat now.")
        print("She is listening.")