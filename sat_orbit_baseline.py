"""Initial Satellite Orbit Baseline Configuration, always works."""
import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
from poliastro.bodies import Earth, Sun
from poliastro.twobody import Orbit
from poliastro.plotting import OrbitPlotter3D
from poliastro.core.perturbations import (
    J2_perturbation,
    atmospheric_drag_exponential,
    radiation_pressure,
)
from poliastro.twobody.propagation import CowellPropagator

# —— Build elliptical 550 km orbit properly ——
circular = Orbit.circular(Earth, alt=550 * u.km)
a = circular.a
initial = Orbit.from_classical(
    Earth, a, 0.1*u.one, 0*u.deg, 0*u.deg, 0*u.deg, 0*u.deg
)
tof = 24 * u.hour

# Two-body baseline
baseline = initial.propagate(tof)
print(f"Baseline semi-major axis after 24 h: {baseline.a:.2f}")
