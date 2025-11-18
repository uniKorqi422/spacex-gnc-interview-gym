import numpy as np
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from poliastro.twobody.propagation import propagate
from astropy import units as u

# Primary Starlink at 550 km, simple circular orbit
a = Earth.R + 550 * u.km
from astropy.time import Time   # <-- add this import at top

epoch = Time.now()   # or Time("2025-11-17T12:00:00")

# Fixed lines
primary = Orbit.circular(Earth, alt=550 * u.km, epoch=epoch)
debris  = Orbit.circular(Earth, alt=560 * u.km, epoch=epoch)

print("Primary altitude:", (primary.a - Earth.R).to(u.km))
print("Debris altitude:", (debris.a - Earth.R).to(u.km))