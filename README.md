# CTP_data — LES results for a planar jet with co-flow

This repository contains results from Large Eddy Simulation (LES) runs of a
planar jet issuing between two co-flows in a rectangular channel, computed on a
supercomputer. Profiles are taken across the channel (position 0–15 m) at four
downstream stations: y = 5, 10, 15 and 20 m.

## Files

| File | Quantity | Units |
| --- | --- | --- |
| `LES_mean_velocity_contour.txt` | Time-averaged (mean) velocity magnitude | m/s |
| `LES_RMSE_velocity_plot.txt` | RMS velocity fluctuation magnitude | m/s |
| `LES_mean_mass_fraction_O2_plot.txt` | Time-averaged O2 mass fraction | – |
| `LES_RMSE_mass_fraction_O2_plot.txt` | RMS O2 mass-fraction fluctuation | – |
| `postprocess_LES_mean_velocity.py` | Example script: load, analyse and plot a data file | |

## File naming convention

```
LES_<statistic>_<quantity>_<descriptor>.txt
```

- `LES` — results come from the Large Eddy Simulation runs.
- `<statistic>` — `mean` for the time-averaged field, `RMSE` for the RMS of the
  fluctuations about that mean.
- `<quantity>` — `velocity` (velocity magnitude) or `mass_fraction_O2`
  (mass fraction of molecular oxygen).
- `<descriptor>` — `contour` / `plot`, the label the dataset was originally
  exported under. Every file holds line profiles in the same format,
  whichever descriptor it has.

## File format

Plain text, whitespace separated, one header line:

```
position[m] y=05 y=10 y=15 y=20
0.000000e+00 5.409836e-03 4.057377e-03 3.065574e-03 3.065574e-03
...
```

- Column 1: cross-stream position in metres, 0 to 15 m in 0.1 m steps (151 rows).
- Columns 2–5: the quantity at downstream stations y = 5, 10, 15 and 20 m.

## Quick start

```bash
pip install numpy matplotlib
python postprocess_LES_mean_velocity.py                       # default file
python postprocess_LES_mean_velocity.py LES_RMSE_velocity_plot.txt
```

The script prints the peak value, peak location, co-flow level and jet
half-width at each station, then saves `LES_mean_velocity_profiles.png`.
