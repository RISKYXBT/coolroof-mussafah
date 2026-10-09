# results/

Every file here is produced by a notebook in `../notebooks/`. Nothing is
hand-edited. The provenance of each is below.

## From `04_emit_hyperspectral.ipynb` — committed

| File | What it is |
|---|---|
| `10_emit_final.png` | the hyperspectral figure: albedo, 1730 nm C–H band depth, material classes, class spectra, composition fingerprint |
| `emit_material_classes.csv` | the five classes with pixel share, mean albedo, albedo spread, per-feature z-scores and interpretation |
| `emit_material_classes.tif` | class map, EPSG:4326, 60 m |
| `emit_albedo.tif` | broadband albedo synthesised from EMIT over Sentinel-2 passbands |
| `emit_depth_bitumen_1730.tif` | the 1730 nm C–H band-depth map — the measurement no multispectral sensor can make |
| `emit_class_spectra.npz` | mean reflectance spectrum per class, with the wavelength vector |
| `emit_final_summary.json` | every headline figure, the full method description, and the limitations |

Source granule `EMIT_L2A_RFL_001_20260520T110418_2614007_042`, acquired
2026-05-20 11:04 UTC (15:04 local). It is pinned by ID in the notebook, so a
reviewer analyses the same scene. The 3.5 GB `.nc` is not committed — see
`.gitignore`.

Two prose corrections were applied to `emit_final_summary.json` after the first
run and are recorded in its `corrections_applied` field. The notebook now
computes both claims from the data rather than asserting them, so they cannot
drift again.

## From `02_main_analysis.ipynb` — committed

| File | What it is |
|---|---|
| `01_lst_change.png` | summer surface temperature, both epochs, and the change |
| `02_albedo.png` | Sentinel-2 broadband albedo over the focus area |
| `03_expansion_heat.png` | land-cover transitions and their thermal signature |
| `04_albedo_model.png` | the albedo→temperature model and its spatial-block residuals |
| `05_roof_priority.png` | every roof by temperature, the top 100, and the roof scatter |
| `roof_priority_ranked.csv` | all 3,603 roofs: albedo, LST, area, ΔT with bounds, avoided kW, three ranking modes |
| `top500_roofs.geojson` | the top 500 as GIS-ready polygons |
| `transition_summary.csv` | LST change by land-use transition |
| `significance_tests.csv` | Welch tests and effect sizes for every claim |
| `summary.json` | every headline figure and validation statistic |

Every number quoted in the root `README.md` §9 comes from `summary.json`, except
the roof cross-section in §9.4, which is computed from `roof_priority_ranked.csv`
(the script is `../docs/make_figs.py`, function `f7_roof_confound`).

Note panel 3 of `05_roof_priority.png`: across buildings the albedo–temperature
relationship is **positive**, the opposite sign to the pixel-level effect the
product uses. That is deliberate and is addressed in README §9.4 rather than
cropped out.
