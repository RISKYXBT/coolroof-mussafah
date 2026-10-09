# Sample input

Committed: the worked example the submission guide asks for, from the same run
that produced `results/`.

From `02_main_analysis.ipynb`:

- `albedo_focus.tif` — clipped broadband albedo raster over the focus area
  (54.48–54.55 E, 24.33–24.38 N), EPSG:32640, 20 m
- `provenance.json` — every scene ID, query window, cloud threshold and data
  licence used in that run: 40 + 40 Landsat scene IDs, 20 Sentinel-2 scene IDs,
  the WorldCover tile, and the Overpass bbox

`provenance.json` is the file to check our claims against. The season breakdown
quoted in the root README §9.7 is recomputed from the scene IDs in it — the
windows are continuous date ranges with scenes chosen by lowest cloud, not a
May–Sept filter, which is why the composites are warm-season-weighted rather
than summer-only.

From `04_emit_hyperspectral.ipynb`:

- `EMIT_L2A_RFL_001_20260520T110418_2614007_042.nc` — the EMIT granule, ~3.5 GB.
  Excluded by `.gitignore`. The notebook pins this granule ID and re-downloads
  it from the NASA LP DAAC, so the scene is reproducible without the file being
  in version control.

Full satellite scenes are not committed: they are hundreds of megabytes to
gigabytes and are openly retrievable with the exact parameters recorded in
`provenance.json` and in the notebooks' configuration cells.
