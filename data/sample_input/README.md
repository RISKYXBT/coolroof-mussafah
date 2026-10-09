# Sample input

Populated when the notebooks run. Nothing here is committed except this file.

From `02_main_analysis.ipynb`:

- `albedo_focus.tif` — clipped broadband albedo raster over the focus area
- `provenance.json` — every scene ID, query window, cloud threshold and data
  licence used in the run that produced `results/`

From `04_emit_hyperspectral.ipynb`:

- `EMIT_L2A_RFL_001_20260520T110418_2614007_042.nc` — the EMIT granule, ~3.5 GB.
  Excluded by `.gitignore`. The notebook pins this granule ID and re-downloads
  it from the NASA LP DAAC, so the scene is reproducible without the file being
  in version control.

Full satellite scenes are not committed: they are hundreds of megabytes to
gigabytes and are openly retrievable with the exact parameters recorded in
`provenance.json` and in the notebooks' configuration cells.
