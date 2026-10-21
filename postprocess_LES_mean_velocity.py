"""Example: load and post-process LES_mean_velocity_contour.txt.

Each data file has a one-line header followed by whitespace-separated columns:
    position[m]  y=05  y=10  y=15  y=20
where y=XX is the downstream station (m) at which the profile was sampled.

Usage:
    python postprocess_LES_mean_velocity.py [path/to/file.txt]
"""
import sys

import numpy as np
import matplotlib.pyplot as plt

fname = sys.argv[1] if len(sys.argv) > 1 else "LES_mean_velocity_contour.txt"

# --- Load -------------------------------------------------------------------
with open(fname) as f:
    header = f.readline().split()
data = np.loadtxt(fname, skiprows=1)

x = data[:, 0]                 # cross-stream position [m]
stations = header[1:]          # ['y=05', 'y=10', 'y=15', 'y=20']
profiles = data[:, 1:]         # mean velocity magnitude [m/s], one column per station

# --- Post-process -----------------------------------------------------------
# Co-flow velocity: median of the outer region, away from the jet and walls
outer = ((x > 1.0) & (x < 4.0)) | ((x > 11.0) & (x < 14.0))

print(f"{'station':>8} {'U_max [m/s]':>12} {'x_peak [m]':>11} "
      f"{'U_coflow':>10} {'half-width [m]':>15}")
for name, u in zip(stations, profiles.T):
    i_max = np.argmax(u)
    u_max, x_peak = u[i_max], x[i_max]
    u_co = np.median(u[outer])

    # Jet half-width: distance between the points where the excess velocity
    # (u - u_co) falls to half of its peak value
    u_half = u_co + 0.5 * (u_max - u_co)
    above = np.where(u >= u_half)[0]
    half_width = 0.5 * (x[above[-1]] - x[above[0]])

    print(f"{name:>8} {u_max:12.4e} {x_peak:11.2f} {u_co:10.4e} {half_width:15.3f}")

# --- Plot -------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.5))
for name, u in zip(stations, profiles.T):
    ax.plot(x, u, marker="o", ms=2.5, lw=1.2, label=name)
ax.set_xlabel("Position (m)")
ax.set_ylabel("Mean velocity magnitude (m/s)")
ax.set_xlim(x.min(), x.max())
ax.set_ylim(bottom=0)
ax.legend(title="Station")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("LES_mean_velocity_profiles.png", dpi=150)
plt.show()
