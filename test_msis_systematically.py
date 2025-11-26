# test_msis_systematically.py
# PacificWhaleSong atmospheric model laboratory
# Author: Amanda Wech-Meehan ♡ 2025-11-26

from datetime import datetime
import pymsis
import numpy as np

# --------------------------------------------------------------
# Helper so we can read the results like a story
# --------------------------------------------------------------
def pretty_print(title: str, density_kg_m3: float, alt_km: float):
    print(f"\n=== {title} ===")
    print(f"Altitude      : {alt_km} km")
    print(f"Date          : 2025-11-22 00:00 UTC")
    print(f"Density       : {density_kg_m3:.3e} kg/m³")
    print(f"≈ {density_kg_m3*1e9:.3f} ng/m³  (nanograms per cubic meter)")
    print(f"≈ {density_kg_m3*1e12:.3f} pg/m³ (picograms – the realm of sprites!)")
    print("-" * 50)

# --------------------------------------------------------------
# TEST 1 – Minimal call, no F10.7 at all, classic MSIS-00
# --------------------------------------------------------------
print("TEST 1 – Classic NRLMSISE-00 (msis00f), no F10.7 provided")
data = pymsis.calculate(
    altitude=250.0,
    longitude=-140.0,
    latitude=0.0,
    date=datetime(2025, 11, 22),
    version='msis00f'          # classic model
)
density1 = float(data[0, 0])
pretty_print("NRLMSISE-00 (2001)", density1, 250.0)

# --------------------------------------------------------------
# TEST 2 – Same everything, but newest model MSIS-2.1
# --------------------------------------------------------------
print("\nTEST 2 – Newest model NRLMSISE-2.1")
data21 = pymsis.calculate(
    altitude=250.0,
    longitude=-140.0,
    latitude=0.0,
    date=datetime(2025, 11, 22),
    version=2.1                # or 'msis21f' – both work
)
density21 = float(data21[0, 0])
pretty_print("NRLMSISE-2.1 (2021+)", density21, 250.0)

# --------------------------------------------------------------
# TEST 3 – MSIS-2.0 just for completeness
# --------------------------------------------------------------
print("\nTEST 3 – Middle child NRLMSISE-2.0")
data20 = pymsis.calculate(
    altitude=250.0,
    longitude=-140.0,
    latitude=0.0,
    date=datetime(2025, 11, 22),
    version='msis20f'
)
density20 = float(data20[0, 0])
pretty_print("NRLMSISE-2.0 (2020)", density20, 250.0)

# --------------------------------------------------------------
# BONUS – Which one is gentlest for PacificWhaleSong?
# --------------------------------------------------------------
print("\n" + "="*60)
print("WHICH MODEL GIVES THE GENTLEST FALL?")
densities = {
    "2001 classic (msis00f)": density1,
    "2020 update   (msis20f)": density20,
    "2021 newest   (msis21f)": density21,
}
gentlest = min(densities, key=densities.get)
print(f"→ The gentlest (lowest density) for 250 km on 2025-11-22 is:")
print(f"    {gentlest}")
print(f"    density = {densities[gentlest]:.3e} kg/m³")
print("="*60)