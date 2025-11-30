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
        
        print("The cathedral has a heartbeat now.")
        print("She is listening.")