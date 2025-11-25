# This Python code snippet is using the `pymsis` library to calculate the atmospheric density at a
# specific altitude and location on Earth. Here's a breakdown of what the code is doing:
from datetime import datetime
import pymsis


density = pymsis.run(
    altitude=250.0,
    longitude=-140.0,
    latitude=0.0,
    f107=150.0,
    f107a=150.0,
    ap=15.0,
    date=datetime(2025, 11, 25)
)
print(f"Density at 250 km: {density[0, 0]:.3e} kg/m³")