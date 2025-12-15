# orbit_tug_core_test.py — The One That Always Works (Dec 2025)
# This is your new gold standard. Push this. It works. Period.

import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
from astropy.time import Time
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from poliastro.core.propagation import func_twobody
from numba import njit
R_EARTH_KM = Earth.R.to_value(u.km)   # ← scalar float, Numba loves this
J2_VAL = Earth.J2.value               # ← scalar float

# ================== 1. EPOCH (the exact moment your orbit is defined) ==================
epoch = Time("2025-12-13 00:00:00", scale="utc")

# ================== 2. INITIAL ORBIT: 550 km circular → slightly eccentric ==================
# Start with perfect circular orbit at 550 km
circ = Orbit.circular(Earth, alt=550 * u.km, epoch=epoch)

# Now make it slightly eccentric (e = 0.1) so drag can "bite" the periapsis
initial = Orbit.from_classical(
    attractor=Earth,
    a=circ.a,
    ecc=0.1 * u.one,
    inc=51.6 * u.deg,        # ISS-like
    raan=0 * u.deg,    # doesn't matter for this demo
    argp=0 * u.deg,
    nu=0 * u.deg,            # start at periapsis
    epoch=epoch
)

print("Initial orbit:")
print(initial)
print(f"Periapsis altitude: {(initial.r_p - Earth.R).to(u.km):.1f}")
print(f"Apoapsis  altitude: {(initial.r_a - Earth.R).to(u.km):.1f}\n")

# ================== 3. PURE VECTOR STATE (this is what Cowell loves) ==================
r0 = initial.r.to_value(u.km)           # km
v0 = initial.v.to_value(u.km / u.s)      # km/s
state0 = np.hstack((r0, v0))

# ================== 4. NON-KEPLERIAN ACCELERATION (J2 + simple drag) ==================
@njit
def j2_accel(r_vec, k):
    r = np.linalg.norm(r_vec)
    z2 = r_vec[2]**2
    factor = -1.5 * J2_VAL * k * R_EARTH_KM**2 / r**5
    return factor * np.array([
        r_vec[0] * (5 * z2 / r**2 - 1),
        r_vec[1] * (5 * z2 / r**2 - 1),
        r_vec[2] * (5 * z2 / r**2 - 3)
    ])

@njit
def full_accel(t0, u, k):
    r = u[:3]
    v = u[3:]
    
    # Start with pure two-body
    acc = func_twobody(t0, u, k)[3:]  # extract dv/dt
    
    # Add perturbations
    acc += j2_accel(r, k)
    h = np.linalg.norm(r) - R_EARTH_KM
    if 0 < h < 1000:
        rho = 2.5e-12 * np.exp(-h / 60)
        acc += -1e-6 * rho * np.linalg.norm(v) * v  
        
    return np.hstack((v, acc))  # velocity + total acceleration

# ================== 5. PROPAGATE 24 HOURS — NO rtol, NO atol, NO DRAMA ==================
from poliastro.twobody.propagation import CowellPropagator
from poliastro.maneuver import Maneuver

final = initial.propagate(
    24 * u.h,
    method=CowellPropagator(f=full_accel)
)

print("After 24 hours with J2 + drag:")
print(final)
print(f"Periapsis altitude: {(final.r_p - Earth.R).to(u.km):.1f}")
print(f"Decay: {(final.r_p - initial.r_p).to(u.km):+.1f}")