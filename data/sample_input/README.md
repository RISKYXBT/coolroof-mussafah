# Sample input

Populated when `notebooks/02_main_analysis.ipynb` runs:

- `albedo_focus.tif` — clipped broadband albedo raster over the focus area
- `provenance.json` — every scene ID, query window, cloud threshold and data
  licence used in the run that produced `results/`

Full satellite scenes are not committed: they are hundreds of megabytes and are
openly retrievable from the Planetary Computer with the exact parameters recorded
in `provenance.json`.
