# orbit_tug_perigee_kick.py — Perigee Raise Visualization (Dec 2025)
# 15 m/s tangential kick + 3D plot to watch the dance!

import numpy as np
from astropy import units as u
from astropy.time import Time
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from poliastro.twobody.propagation import CowellPropagator
from poliastro.maneuver import Maneuver
from poliastro.plotting import OrbitPlotter3D  # For immersive 3D visualization
from poliastro.core.propagation import func_twobody
from numba import njit

# Constants
R_EARTH_KM = Earth.R.to_value(u.km)
J2_VAL = Earth.J2.value
MU = Earth.k.to_value(u.km**3 / u.s**2)

# Epoch
epoch = Time("2025-12-13 00:00:00", scale="utc")

# Initial orbit (starting at perigee)
circ = Orbit.circular(Earth, alt=550 * u.km, epoch=epoch)
initial = Orbit.from_classical(
    Earth,
    a=circ.a,
    ecc=0.1 * u.one,
    inc=51.6 * u.deg,
    raan=0 * u.deg,
    argp=0 * u.deg,
    nu=0 * u.deg,  # Perigee — ideal for kick
    epoch=epoch
)

print("Initial orbit (at perigee):")
print(initial)
print(f"Periapsis altitude: {(initial.r_p - Earth.R).to(u.km):.1f} km")
print(f"Apoapsis altitude: {(initial.r_a - Earth.R).to(u.km):.1f} km\n")

# Optional vector state (for deeper Cowell insight — comment if not needed)
# r0 = initial.r.to_value(u.km)
# v0 = initial.v.to_value(u.km / u.s)
# state0 = np.hstack((r0, v0))

# 15 m/s tangential Δv
v_vec = initial.v.to_value(u.km / u.s)
delta_v_vec = 0.015 * (v_vec / np.linalg.norm(v_vec))  # Posigrade

maneuver = Maneuver.impulse(delta_v_vec * u.km / u.s)
post_kick = initial.apply_maneuver(maneuver)

print("Immediate post-15 m/s kick:")
print(post_kick)
print(f"Periapsis altitude: {(post_kick.r_p - Earth.R).to(u.km):.1f} km")
print(f"Apoapsis altitude: {(post_kick.r_a - Earth.R).to(u.km):.1f} km\n")

# Perturbations (J2 + drag)
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
    acc = func_twobody(t0, u, k)[3:]
    acc += j2_accel(r, k)
    h = np.linalg.norm(r) - R_EARTH_KM
    if 0 < h < 1000:
        rho = 2.5e-12 * np.exp(-h / 60)
        acc += -1e-6 * rho * np.linalg.norm(v) * v
    return np.hstack((v, acc))

# Propagate post-kick
final = post_kick.propagate(24 * u.h, method=CowellPropagator(f=full_accel))

print("After 24 hours (post-kick + perturbations):")
print(final)
print(f"Periapsis altitude: {(final.r_p - Earth.R).to(u.km):.1f} km")
print(f"Apoapsis altitude: {(final.r_a - Earth.R).to(u.km):.1f} km")
print(f"Net perigee change vs original: {(final.r_p - initial.r_p).to(u.km):+.1f} km")
print(f"Net apoapsis change vs original: {(final.r_a - initial.r_a).to(u.km):+.1f} km\n")

# 3D Plot to visualize the dance
plotter = OrbitPlotter3D()
plotter.set_attractor(Earth)
plotter.plot(initial, label="Initial (decaying)", color="#1f77b4")
plotter.plot(post_kick, label="Post-kick (stretched)", color="#ff7f0e")
plotter.plot(final, label="After 24h", color="#2ca02c")
plotter.show()