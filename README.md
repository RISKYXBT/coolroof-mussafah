# Cool Roof Priority Index — Mussafah, Abu Dhabi

**Arab Youth Space Hackathon 2026 · 813 Challenge**
**Theme:** Urban Expansion, Land Use Change & Heat Risk  ·  **Track:** Hyperspectral Data Track
**Team:** T0050 · United Arab Emirates

> Satellite screening that turns a city heat map into a ranked worklist of individual
> rooftops — with the cooling-per-retrofit **measured from Abu Dhabi's own data**, and
> the roof material identified from **NASA EMIT hyperspectral imagery over Mussafah
> itself**.

![Roof priority](results/05_roof_priority.png)

---

## 2 · The business use case

### 2.1 Who the user is, and the decision they make

The asset-management and urban-planning departments of a Gulf municipality — Abu Dhabi
City Municipality in our case. Each budget cycle they allocate a finite heat-mitigation
budget across thousands of candidate buildings. Cool-roof coating is among the cheapest
interventions available, but it has to be targeted: coating every roof in an industrial
district is not affordable, and coating the wrong ones wastes the budget.

**What they use today.** City-scale urban heat island maps from consultants or research
groups, plus manual site survey. Those maps show *where it is hot*. They do not say
*which roof to treat first*, *how much cooling the treatment buys*, or *whether that
roof can be coated at all*. The step from map to works programme is taken on judgement.

### 2.2 Why ownership makes this harder than it looks

Roof ownership in Mussafah is split three ways, and the municipality has a **different
lever for each**:

| Who owns the roof | Municipality's lever | What the ranking is used for |
|---|---|---|
| **ADM-owned municipal buildings** | Direct capital works | Sequencing its own retrofit programme against budget |
| **Other government entities** | Inter-entity coordination; each holds its own capex | Showing an entity its own stock, ranked, with the evidence |
| **Private industrial landlords** (most of Mussafah's roof area) | Regulation, permit conditions, incentive schemes — **not** direct spending | Targeting where a code change or incentive buys the most cooling per unit of regulatory effort |

This is the reason a ranked list has value even where the municipality is not paying.
For privately owned stock the output is not a works order, it is **an evidence base for
where to apply a rule**. A blanket requirement across an industrial district is
politically expensive; a requirement aimed at the 2.8% of roofs carrying 21% of the
available cooling is defensible.

### 2.3 Commercial model

Procurement reality in Abu Dhabi favours a **periodic study, not a software
subscription**. Municipal departments buy consultancy studies on a multi-year cycle far
more readily than they take on recurring software. The natural cadence is **once every
three to four years**, which also matches how fast the building stock and its surfaces
actually change.

So the product is a **repeat screening study**:

- **Deliverable:** ranked roof inventory (CSV + GIS layer), heat and material maps, and
  a prioritisation report, scoped to a district or to a single entity's portfolio
- **Cadence:** every 3–4 years, with the previous run as the baseline, so the second
  study also measures what the first one achieved
- **Cost base:** the input data is free and open (Landsat, Sentinel-2, EMIT,
  OpenStreetMap). Essentially all cost is analyst time, which is why this is viable at
  district scale where a field survey of 3,603 roofs never would be.
- **Buyers:** ADM for its own stock; other government entities for theirs; large
  industrial landlords and free-zone operators for their portfolios.

**On unit rates — deliberately left open.** The pipeline outputs cooling per square
metre and avoided solar absorption in kilowatts. It does **not** embed a coating price.
ADM already maintains its own schedule of rates, and so does every contractor who would
bid the works. The ranking becomes a cost-effectiveness ranking the moment the client's
own rate card is applied to the `area_m2` column — one multiplication. Publishing an
invented AED/m² figure would add nothing and would be the first number a procurement
reviewer challenged. **[TEAM: if a verified Abu Dhabi rate is available before
submission, add it here as a worked example and cite the source.]**

---

## 3 · The problem

Gulf cities are among the fastest-warming urban environments on Earth, and the warming
is not only climatic — it is constructed. When bare desert is replaced by asphalt,
concrete and dark roofing, surface albedo falls, shortwave absorption rises,
evapotranspirative cooling disappears, and stored heat is re-radiated through the night.

In Mussafah, Abu Dhabi's principal industrial district, a decade of Landsat observation
shows:

- **30.4 km² (3,045 hectares) of bare desert converted to built-up land** between
  2014–2016 and 2024–2026
- built-up surfaces today run **+1.33 °C hotter** than surrounding bare desert
  (t = 78.6, p < 10⁻³⁰⁰)
- **the existing built fabric is warming 0.34 °C per decade faster than the desert
  around it** (t = 62.7, p < 10⁻³⁰⁰, Cohen's d = 0.32)

The third point is what makes retrofit, rather than new-build regulation, the right
lever: **the heat problem is intensifying inside the city that already exists**, not at
the expansion frontier (see §9.3).

**Why satellite data is the right instrument.** Rooftop albedo, surface temperature and
material cannot be inventoried at city scale by any ground method at acceptable cost —
tens of thousands of roofs, most behind private fences. Earth observation measures all
three for every roof simultaneously, repeatedly, without site access.

---

## 4 · Data used

| Product | Provider | Level | Dates | Scenes | Resolution | Licence |
|---|---|---|---|---|---|---|
| Landsat 8/9 Collection 2 Level-2 | USGS / NASA | L2SP | 2014-05-18 → 2015-11-04 | 40, cloud < 15% (88% May–Sept) | 30 m | Public domain |
| Landsat 8/9 Collection 2 Level-2 | USGS / NASA | L2SP | 2024-10-03 → 2026-09-24 | 40, cloud < 15% (72% May–Sept) | 30 m | Public domain |
| Sentinel-2 L2A | ESA Copernicus | L2A | 2025-09-24 → 2026-09-27 | 20, cloud < 15% (**20% May–Sept** — see §9.7) | 10–20 m | Free and open |
| **NASA EMIT L2A surface reflectance** | **NASA JPL / LP DAAC** | **L2A** | **2026-05-20, 15:03 local** | **1 granule** | **60 m, 285 bands** | **Open** |
| ESA WorldCover v200 | ESA | — | 2021 | tile N24E054 | 10 m | CC BY 4.0 |
| OpenStreetMap buildings | OSM contributors | — | 2026-10-07 | 8,503 raw | vector | ODbL |

Scene IDs, query windows and cloud thresholds are written to
`data/sample_input/provenance.json` on each run. Access is via the **Microsoft
Planetary Computer STAC API**, **NASA Earthdata (CMR + LP DAAC)** for EMIT, and the
**Overpass API** for OpenStreetMap.

### 4.1 How we arrived at EMIT, and what we checked first

Satellite 813 data is not available to participants during the PoC phase. We therefore
searched for open hyperspectral coverage of the AOI, and record the search because the
negative results are part of the evidence:

- **Planet Tanager** — we walked the open STAC catalogue. **No `urban` scene intersects
  the UAE in the open archive.** Tanager-1 has daily revisit, so the satellite has
  certainly imaged Abu Dhabi; the *open archive* is a curated public sample and that is
  what we searched. We briefly prepared a declared Riyadh analogue (24.58 °N, the same
  latitude and climate) and then discarded it once real coverage was found.
- **NASA EMIT** — **47 L2A granules intersect Mussafah.** EMIT is an imaging
  spectrometer on the ISS whose mission is arid-region surface mineralogy, which is why
  the Arabian Peninsula is well covered. We selected on summer timing, sun angle, AOI
  overlap and recency.

We report this because "no hyperspectral coverage exists" would have been wrong, and
checking only the first archive we were handed would have produced that wrong answer.

---

## 5 · Technical approach

**1 — Surface temperature.** Landsat Collection 2 **Level-2**, which ships a
USGS-produced atmospherically corrected Surface Temperature band (band 10, ASTER GED
emissivity). We deliberately do not derive LST from top-of-atmosphere radiance: Level-2
removes a class of hand-made assumptions and gives a citable processing chain. Scaling
`K = DN × 0.00341802 + 149.0`; per-pixel cloud, cirrus, shadow and dilated-cloud masking
from `qa_pixel` before compositing; per-pixel median over each epoch window.

**2 — One sensor for both epochs.** Both the thermal and the optical layers of the
change analysis come from Landsat. Mixing Landsat 2014 with Sentinel-2 2025 would fold a
cross-sensor calibration difference into what we report as real-world change. Sentinel-2
is used only for present-day albedo, where no cross-epoch comparison is made.

**3 — Built-up classification: a documented escalation.** We began with the standard
index threshold (`NDBI > 0`) as the simple explainable baseline. **It failed**, and we
established that rigorously: calibrating the threshold to maximise F1 on a spatially
held-out half left precision pinned at **0.40 at every threshold tested**, with 92% of
the AOI labelled built-up against a 41% reference. The reason is physical —
NDBI = (SWIR − NIR)/(SWIR + NIR), and **bare sabkha is SWIR-bright exactly like
concrete**. With that failure documented we escalated to a **random forest on 14
features including multi-scale texture** (local standard deviation at ~150 m and ~270 m):
industrial fabric is spatially rough at 30 m, sabkha is smooth. The same model is
applied to both epochs.

**4 — Broadband albedo.** Sentinel-2 narrow bands via published narrow-to-broadband
coefficients:

```
α = 0.2266·B2 + 0.1236·B3 + 0.1573·B4 + 0.3417·B8 + 0.1170·B11 + 0.0338·B12
```

(weights sum to 1.0). **Source:** Bonafoni & Sekertekin, *Albedo Retrieval From
Sentinel-2 by New Narrow-to-Broadband Conversion Coefficients*, IEEE GRSL, 2020.

**5 — Calibrating the intervention (the analytical core).** Over pixels that *both* our
classifier and ESA WorldCover independently call built-up, with water and vegetation
excluded, we regress epoch-B LST on albedo controlling for NDVI. The slope is the
**locally measured marginal effect of albedo on surface temperature**. Uncertainty comes
from a **300-sample spatial block bootstrap** — resampling whole 1 km blocks, not
pixels, because pixel resampling ignores spatial autocorrelation and understates the
interval.

**6 — Hyperspectral material identification (EMIT).** EMIT ships in sensor geometry
with a geometric lookup table; we orthorectify only the AOI window. Atmospheric water
bands (1340–1480, 1790–1980 nm) and the detector edges are removed — EMIT's own
`good_wavelengths` flag retains them and reflectance there is noise — leaving **230
bands, 425–2455 nm**.

Clustering the raw spectra does not work, and we report why: the six classes came back
with near-identical shapes differing only in brightness, because **in a dust-blown arid
city sand, concrete and dusty roofs share a carbonate/silicate spectral shape**. We
therefore measure **band depth against a local two-point continuum** (Clark & Roush,
1984) at four diagnostic features, then cluster on the standardised depths:

| Centre | Feature | Diagnostic of |
|---|---|---|
| 900 nm | Fe-oxide | rust, red tile, ferruginous sand |
| **1730 nm** | **C–H stretch** | **bitumen / asphalt — invisible to Sentinel-2** |
| 2200 nm | Al–OH | clay, cement, concrete |
| 2340 nm | carbonate | limestone aggregate, sabkha sand |

Classes are interpreted by **deviation from the scene mean**, not absolute depth,
because carbonate absorption dominates everywhere in a carbonate-sabkha setting.

**7 — Roof-level ranking.** OSM footprints; zonal mean albedo and LST per roof;

```
ΔT      = |sensitivity| × max(0, 0.60 − current_albedo)      with CI bounds
benefit = ΔT × roof_area_m²                                   [°C·m²]
ΔQ      = (0.60 − current_albedo) × S × area                  [W avoided]
```

Area enters deliberately: one large warehouse roof is far cheaper to treat per square
metre than fifty small ones. Three ranking modes are produced (§9.5).

**Validation is spatial throughout, never random pixel splits** — neighbouring pixels
are near-duplicates and a random split leaks them across the train/test boundary.

---

## 6 · Installation

Requires **Python 3.11**.

```bash
git clone https://github.com/RISKYXBT/coolroof-mussafah.git
cd coolroof-mussafah
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

The main analysis needs no credentials. The EMIT notebook requires a **free NASA
Earthdata account** (https://urs.earthdata.nasa.gov/users/new) — registration is instant
and the data is open.

---

## 7 · How to run

```bash
jupyter lab notebooks/02_main_analysis.ipynb     # ~30-40 min, no GPU
jupyter lab notebooks/04_emit_hyperspectral.ipynb # ~15 min, needs Earthdata login
```

Run all cells top to bottom. Nothing needs editing to reproduce our result. To run a
different city, change only `AOI_BBOX`, `FOCUS_BBOX` and the epoch windows in the
configuration cell.

Optional: `notebooks/00_recon.ipynb` is a 10-minute data-availability check that
downloads no imagery. `notebooks/03_hyperspectral.ipynb` documents the Tanager
catalogue search described in §4.1.

---

## 8 · Example input and output

**Input** — `data/sample_input/albedo_focus.tif` (clipped albedo raster) and
`provenance.json` (every scene ID and parameter used). Full scenes are not committed;
they are openly retrievable with the recorded parameters.

**Output** — `results/`:

| File | Contents |
|---|---|
| `roof_priority_ranked.csv` | all 3,603 roofs: albedo, LST, area, ΔT with bounds, avoided kW, three ranking modes |
| `top500_roofs.geojson` | top 500 roofs as GIS-ready polygons |
| `emit_material_classes.csv/.tif` | EMIT material classes and their composition fingerprints |
| `emit_depth_bitumen_1730.tif` | the C–H band-depth map |
| `transition_summary.csv` | LST change by land-use transition |
| `significance_tests.csv` | Welch tests and effect sizes for every claim |
| `summary.json`, `emit_final_summary.json` | all headline figures and validation statistics |
| `01`–`10_*.png` | figures |

![LST change](results/01_lst_change.png)
![EMIT materials](results/10_emit_final.png)

---

## 9 · Results and limitations

### 9.1 Headline results

| Quantity | Value |
|---|---|
| Mean composite LST, 2014–2016 → 2024–2026 | 49.62 °C → 50.56 °C |
| Desert converted to built-up | **30.4 km² (3,045 ha)** |
| Static surface UHI (built-up vs desert, today) | **+1.33 °C** (t = 78.6, p < 10⁻³⁰⁰) |
| Existing built fabric warming vs desert | **+0.34 °C/decade** (t = 62.7, d = 0.32) |
| **Measured albedo sensitivity** | **−4.56 °C per unit albedo**, 95% CI **[−6.05, −2.94]** |
| → cooling per +0.10 albedo | **0.46 °C** [0.29, 0.61] |
| Roofs ranked | 3,603 (4.82 km² of roof) |
| Top 100 roofs | 20.8% of total benefit — **7.5× concentration** |
| Avoided solar absorption, top 100 | **64.8 MW** summer-mean, 205 MW at noon peak |

### 9.2 Validation

**Built-up classification** — 2 km spatial blocks, 60/40 split, metrics on held-out
blocks only (n = 95,346 test pixels):

| Metric | NDBI > 0 baseline | Random forest |
|---|---|---|
| accuracy | 0.465 | **0.770** |
| precision | 0.426 | **0.675** |
| recall | 0.856 | 0.856 |
| F1 | 0.569 | **0.754** |
| IoU | 0.398 | **0.606** |
| false positives | 45,337 | **16,262** |
| predicted built-up share | 82.9% | 52.4% *(reference 41.3%)* |

Top features: `swir` 0.132, `mndwi` 0.116, **`tex_bright_5` 0.108**, `brightness` 0.079,
**`tex_swir_5` 0.074**, `nir` 0.072, **`tex_swir_9` 0.067**. The three texture features
account for roughly a quarter of the model's decision weight — direct evidence for why
the spectral index alone failed.

**Albedo → LST model** — 5-fold spatial block CV, 1 km blocks:

| | |
|---|---|
| slope | −4.56 °C per unit albedo |
| 95% CI (300 block bootstrap resamples) | **[−6.05, −2.94]** |
| spatial-CV R² | 0.057 |
| spatial-CV RMSE | 1.47 °C |
| n | 152,487 px in 159 blocks |

**On the low R².** The model explains 5% of the variance in absolute LST, and we report
that plainly. It does not undermine the result, because **we estimate a marginal effect,
not a prediction**. Absolute surface temperature over built land is driven mostly by
factors we do not model — thermal mass, moisture, building use, HVAC exhaust. The
coefficient on albedo is nonetheless tightly constrained: its entire 95% interval lies
below zero and it is stable across independent spatial folds.

**Robustness across methods.** The sensitivity was estimated three times under three
different built-up classifications:

| Classification | Slope |
|---|---|
| WorldCover mask + water/vegetation exclusion | −4.07 |
| Calibrated NDBI threshold + WorldCover | −4.55 |
| Random forest + WorldCover | **−4.56** |

The first two were development runs under alternative masks. The committed notebook
reproduces the adopted model (−4.56) and the rejected baseline (+11.55); `summary.json`
records both.

**A sign error we caught and fixed.** Our first mask (`NDBI > 0` alone) gave a slope of
**+11.55** — brighter surfaces appearing hotter, inverting the physics. The cause was
contamination: channel water (dark *and* cold) anchoring the low-albedo end, bright
sabkha (bright *and* very hot) anchoring the high end. Requiring agreement with an
independent land-cover product recovered the expected negative slope. `summary.json`
retains both values, because the audit trail is part of the evidence.

### 9.3 A null result, reported as such

**Land converted from desert to built-up did *not* warm more than desert left untouched**
(−0.01 °C, t = −1.3, p = 0.21, d = −0.008).

The diagnostic explains why. In 2014–2016, *before any construction*, land that would
later be built on was already **1.44 °C hotter** than desert that stayed desert
(53.00 °C vs 51.55 °C) while being spectrally almost indistinguishable from it (NDBI
0.055 vs 0.058). Its slightly lower brightness accounts, using our own measured
sensitivity, for only ≈0.11 °C of that gap.

Two explanations fit and **we cannot separate them**:

1. **Siting.** Development occurs adjacent to existing urban fabric, so the land was
   already inside the city's thermal footprint. A spatial confound.
2. **Site preparation.** Clearing and compaction remove the salt crust and shallow
   moisture of natural sabkha, raising surface temperature before any structure exists.

Distinguishing them needs construction-timing records or a matched-control design
pairing converted parcels with equidistant unconverted ones. Out of scope here, and the
natural next step.

### 9.4 The roof cross-section does not confirm the per-roof predictions

We ranked the roofs, then tested the ranking against itself. Across the 3,603 buildings,
**a brighter roof is not a cooler roof**: the cross-sectional association is
**+8.11 °C per unit albedo** (p ≈ 10⁻⁹⁰, r² = 0.107), and it survives controlling for
roof size (+6.20). That is the opposite sign to the −4.56 the product is built on, and it
is visible in panel 3 of `results/05_roof_priority.png` — a file we ship. Reporting it is
not optional.

**Part of it is the thermal pixel.** Landsat thermal is 30 m, so one pixel is 900 m². The
median roof in the ranking is 796 m² — under one pixel — and its "roof temperature" is
therefore largely its surroundings. Splitting by roof size:

| Roof size | median area | ≈ Landsat px | slope | p |
|---|---|---|---|---|
| Q1 | 438 m² | 0.5 | **+9.69** | 10⁻²⁷ |
| Q2 | 573 m² | 0.6 | +5.62 | 10⁻¹⁰ |
| Q3 | 796 m² | 0.9 | +1.59 | 0.035 |
| Q4 | 1,185 m² | 1.3 | +4.17 | 10⁻⁶ |
| Q5 | 2,399 m² | 2.7 | +5.05 | 10⁻⁶ |
| ≥ 5,000 m² (n = 93) | — | ~5.5 | +3.45 | **0.24, not significant** |

The association is strongest where the pixel is dirtiest and is not significant for the
93 roofs that span a clean pixel — but it does not flip negative, so mixing is not the
whole story.

**The rest is a between-building confound.** Brighter-roofed buildings in Mussafah are
systematically different buildings: larger, newer, set in wider paved yards, with
different roof thermal mass and internal heat loads. None of those are in our data, and
none of them are removed by comparing across buildings.

**Why this does not refute −4.56.** The two numbers answer different questions. The
pixel-level model asks *does a brighter surface run cooler, holding location and
vegetation roughly fixed* — a within-block marginal effect, and the answer is yes. The
roof cross-section asks *are buildings that happen to have brighter roofs cooler
buildings* — a between-unit comparison, and the answer is no. The second is a fact about
which buildings in Mussafah have bright roofs; it is not a statement about radiative
physics, and it is exactly the kind of comparison the spatial-block design was chosen to
avoid.

**What it costs us, stated plainly.** The per-roof `delta_T_est_c` column is a screening
estimate carried down from a pixel-level marginal effect. **It is not validated at
individual-roof scale, and our own data does not confirm it.** Settling it requires a
before/after measurement on coated roofs, or a matched-pair design holding building type,
size and surroundings fixed. That is step 1 of the proposed next phase, and until it is
done the ΔT column should be read as a prioritisation score, not as a predicted
temperature drop for a named building.

---

### 9.5 Three ranking modes — a policy choice, not a technical one

| Mode | Top-100 area | Mean albedo | Mean LST | Avoided absorption |
|---|---|---|---|---|
| Total benefit (area × cooling) | 106.6 ha | 0.387 | 54.5 °C | 64.8 MW |
| Hottest roofs first | 47.7 ha | 0.404 | 56.5 °C | 26.9 MW |
| Biggest per-roof ΔT | 5.0 ha | 0.220 | 51.7 °C | 5.7 MW |

Only **27 of 100 roofs** appear on both the "total benefit" and "hottest" lists. The
choice of objective genuinely changes which buildings get treated, so it belongs to the
municipality. All three ship in the CSV.

### 9.6 What hyperspectral adds, and what it does not

EMIT granule `EMIT_L2A_RFL_001_20260520T110418_2614007_042`, 2026-05-20 at 15:03 local
— **three hours later in the day than Landsat's ~10:30 overpass**, so it samples closer
to peak surface temperature. 12,738 clean spectra, 230 bands.

**Two classes carry real compositional signal** (σ from scene mean):

| Class | Share | Albedo | Fe | **Bitumen** | **Al–OH** | Carbonate | Reading |
|---|---|---|---|---|---|---|---|
| **2** | 13.9% | 0.270 (sd **0.082**) | +0.5 | **+1.2** | **+1.4** | −0.7 | bituminous + cement-bearing built surface |
| **0** | 18.9% | 0.324 | +0.3 | −0.5 | +0.5 | **+1.3** | carbonate — bare sabkha sand |
| 3 | 12.5% | 0.250 | **−1.9** | +0.2 | −0.9 | +0.1 | iron-depleted; possibly shadowed |
| 1 | 24.7% | 0.271 | 0.0 | +0.4 | −0.6 | 0.0 | spectrally average |
| 4 | 30.1% | 0.284 | +0.4 | −0.7 | −0.1 | −0.6 | spectrally average |

**Adjusted Rand Index against clustering on albedo alone: 0.092.** The composition
grouping is almost independent of brightness — the absorption features are separating
surfaces that broadband albedo cannot.

**The claim, stated precisely.** Class 2 is not the darkest class (class 3 is, at
0.250), but it is the one enriched in both the 1730 nm C–H bitumen feature and the
2200 nm Al–OH cement feature while being depleted in the carbonate background, and it
has the widest albedo spread of any class (0.082 against ~0.03), consistent with mixed
built materials rather than uniform sand. Broadband albedo identifies these surfaces as
dark; the narrow bands identify them as bituminous and cement-bearing — which is what
determines whether a roof can be coated or has to be replaced.

A visual check: the darkest patch in the albedo map (α ≈ 0.13) coincides with the
strongest 1730 nm response in the scene, consistent with a large asphalt or bitumen
surface. Mussafah contains asphalt plants.

**What hyperspectral does not do here.** Three of five classes — **67% of the imaged
area** — are spectrally average, with no feature more than 0.7σ from the scene mean.
Aeolian dust deposition homogenises surface spectra in an arid industrial zone, so
hyperspectral meaningfully differentiates roughly **one third** of the scene, not all of
it. We consider this worth reporting for its own sake: any operational hyperspectral
urban product over Gulf cities, including Satellite 813, will face the same constraint.

### 9.7 Limitations

- **The composites are warm-season-weighted, not summer-only.** The epoch windows are
  continuous date ranges and scenes are selected by lowest cloud, not by month, so the
  Landsat composites are **88% May–Sept for 2014–2016 and 72% for 2024–2026** (the rest
  April, October, November). The seasonal mix therefore differs between epochs, and the
  later epoch carries more cool-season imagery — which biases the epoch-to-epoch warming
  figure (+0.94 °C) **downward**, so that number is conservative rather than inflated.
  The static UHI and the per-decade trend compare land classes *within* a composite, so
  the seasonal mix affects both classes alike and largely cancels. Every scene ID is in
  `data/sample_input/provenance.json`; the month breakdown above is recomputed from it.
- **Albedo and temperature are measured in different seasons.** Only **4 of the 20
  Sentinel-2 scenes fall in May–Sept**; the albedo composite is dominated by
  October–February imagery, because the Gulf's summer dust and haze are flagged by the
  cloud mask and the lowest-cloud scenes are therefore cool-season. Surface albedo of
  built materials is fairly stable through the year, but solar zenith angle at 24°N
  differs sharply between December and June and dust deposition is seasonal, so the
  albedo values carry an unquantified offset from their summer values. The −4.56
  sensitivity regresses a warm-season LST composite on a cool-season albedo composite.
  Restricting both to May–Sept, over a wider multi-year window so enough clean summer
  scenes are available, is the first thing we would change.
- **The per-roof ΔT is not validated at roof scale.** See §9.4 — the roof cross-section
  shows the opposite sign, for reasons we can partly but not fully attribute to mixed
  thermal pixels. Treat the ΔT column as a prioritisation score.
- **Land surface temperature is not air temperature.** Satellites measure the radiating
  skin of the surface. Human thermal comfort depends on air temperature, humidity and
  radiant load. This tool ranks *surfaces*; it does not predict heat-stroke risk.
- **The sensitivity is correlational, not causal.** §5 step 5 measures covariance across
  space. It is not a controlled experiment, and confounders — roof thermal mass,
  building use, HVAC exhaust, roof age — are not separated. The ΔT figures are screening
  estimates with stated bounds, not engineering predictions.
- **Validation is against a model, not ground truth.** ESA WorldCover is itself a
  classification product. No field survey or in-situ logging was performed.
- **The classifier still over-predicts built-up** (52.4% vs 41.3% reference). Precision
  0.675 means roughly a third of pixels we call built-up are not; the land-cover areas in
  §9.1 carry that bias.
- **The 2021-trained classifier is applied to 2014–2016 imagery**, assuming spectral
  stationarity for the same sensor. Reasonable, unverified.
- **EMIT spatial resolution.** 60 m, one pixel 3,600 m². Material classes are reliable
  only for roofs spanning a clean pixel; the top-100 roofs average 1.07 ha (~3 pixels),
  smaller roofs in the ranking are spectrally mixed.
- **EMIT coverage is partial.** The granule's southern edge falls at 24.353 °N against an
  AOI south edge of 24.29 °N, with 43.5% geometric-lookup fill — roughly **46 km² of the
  195 km² AOI**, the northern strip. The material results describe that strip.
- **Detector striping.** Both the 2200 nm and the 1730 nm band-depth maps show diagonal
  striping, so part of those signals is instrumental rather than surface. The coherent
  patches in the 1730 nm map are not stripe-aligned and we read those as real, but the
  per-pixel depths should not be over-interpreted.
- **Spectral inference only.** Classes are "consistent with" a material, never confirmed
  as one. No field verification was carried out.
- **Mixed thermal pixels.** Landsat thermal is 30 m; roofs below ~900 m² carry signal
  from surroundings. Roofs under 400 m² are excluded.
- **OSM completeness varies.** Missing footprints are missing from the ranking. A
  deployed version would use municipal cadastral data.
- **Overpass time.** Landsat crosses at ~10:30 local; peak surface temperature is later,
  so absolute values understate the daily maximum. Relative ranking is unaffected.
- **Avoided absorption is not avoided energy.** The megawatt figures are reduced
  shortwave absorption at an assumed S = 300 W/m² summer daytime mean. They are **not**
  an air-conditioning saving. **[TEAM: verify and cite the irradiance figure.]**

---

## 10 · Team, licence and attribution

| Member | Role |
|---|---|
| Meera Almansoori | Team lead · surface energy balance physics, methodology, validation design |
| Ghazi Hafedh | Data pipeline, modelling, software, repository |
| Ahmed Abu Farha | Municipal building-control domain input, end-user requirements |

**Code licence:** MIT (see `LICENSE`).

**Data attribution.**
Landsat Collection 2 Level-2 courtesy of the U.S. Geological Survey.
Contains modified Copernicus Sentinel-2 data (2025–2026).
EMIT data courtesy of NASA JPL, distributed by the LP DAAC.
© ESA WorldCover project 2021, CC BY 4.0.
Map data © OpenStreetMap contributors, Open Database Licence.

**Methods cited.**
Bonafoni, S. & Sekertekin, A. (2020). *Albedo Retrieval From Sentinel-2 by New
Narrow-to-Broadband Conversion Coefficients.* IEEE GRSL.
Clark, R. N. & Roush, T. L. (1984). *Reflectance spectroscopy: quantitative analysis
techniques for remote sensing applications.* JGR Solid Earth.
USGS (2024). *Landsat Collection 2 Level-2 Science Product Guide.*

**Built on.** Starter notebooks and data-access patterns from the official
[813 Challenge repository](https://github.com/Tnecniv-Teikram/813-hyperspectral-hackathon)
by Dr. Vincent Markiet, Space42.

No credentials, API keys or restricted imagery are committed to this repository.
