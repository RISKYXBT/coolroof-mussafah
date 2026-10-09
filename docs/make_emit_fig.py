#!/usr/bin/env python3
"""Rebuild 10_emit_final.png from the committed artefacts, with correct aspect.

The original figure used aspect="auto", which stretches a lon/lat image to
whatever shape the subplot happens to be. At 24.38 N the AOI window is
15.2 km east-west by 6.4 km north-south (true aspect 2.39), so the maps were
rendered roughly square and every shape in them was wrong.

A lon/lat image needs aspect = 1/cos(latitude) to be geographically correct:
one degree of longitude at this latitude is 101.4 km against 110.6 km for one
degree of latitude.

Inputs are the GeoTIFFs, CSV and NPZ already in results/ — no re-download.
"""
import os, math
import numpy as np, pandas as pd
import rasterio
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SRC = "/home/claude/emit_final"
OUT = "/home/claude/deck/fig/10_emit_final.png"

plt.rcParams.update({
    "font.family": "Inter", "font.size": 11,
    "axes.titlesize": 12, "axes.titleweight": 600,
    "figure.facecolor": "white", "savefig.facecolor": "white",
})

FEATURES = {"fe_oxide_900": 900, "bitumen_1730": 1730,
            "alOH_2200": 2200, "carbonate_2340": 2340}
names = list(FEATURES)
K, TARGET, ARI = 5, 0.60, 0.092


def load(name):
    with rasterio.open(f"{SRC}/{name}.tif") as s:
        return s.read(1), s.bounds


cls, b = load("emit_material_classes")
alb, _ = load("emit_albedo")
bit, _ = load("emit_depth_bitumen_1730")

ext = [b.left, b.right, b.bottom, b.top]
lat0 = (b.top + b.bottom) / 2
ASPECT = 1.0 / math.cos(math.radians(lat0))      # geographic aspect for lon/lat

km_w = (b.right - b.left) * 111.320 * math.cos(math.radians(lat0))
km_h = (b.top - b.bottom) * 110.574
print(f"AOI window {km_w:.1f} x {km_h:.1f} km, true aspect {km_w/km_h:.2f}, "
      f"imshow aspect {ASPECT:.4f}")

z = np.load(f"{SRC}/emit_class_spectra.npz")
wl = z["wavelengths"]
mat = pd.read_csv(f"{SRC}/emit_material_classes.csv")
hero = int(mat.loc[mat.z_bitumen_1730.idxmax(), "material_class"])

fig = plt.figure(figsize=(17.5, 9.6))
gs = fig.add_gridspec(2, 3, height_ratios=[1, 1.12], hspace=0.30, wspace=0.17)


def mapax(pos, arr, cmap, title, vmin=None, vmax=None, ticks=None, ylab=True):
    ax = fig.add_subplot(gs[pos])
    im = ax.imshow(arr, cmap=cmap, extent=ext, vmin=vmin, vmax=vmax,
                   aspect=ASPECT, interpolation="nearest")
    ax.set_title(title, pad=9)
    ax.set_xticks([54.45, 54.50, 54.55])
    ax.set_yticks([24.36, 24.38, 24.40])
    ax.set_xticklabels(["54.45°E", "54.50°E", "54.55°E"], fontsize=8.5)
    ax.set_yticklabels(["24.36°N", "24.38°N", "24.40°N"] if ylab else [],
                       fontsize=8.5)
    ax.tick_params(length=2, colors="#7a8690")
    for sp in ax.spines.values():
        sp.set_color("#c3ccd5")
    cb = plt.colorbar(im, ax=ax, fraction=0.030, pad=0.015, ticks=ticks)
    cb.ax.tick_params(labelsize=8.5, length=2)
    cb.outline.set_visible(False)
    return ax


mapax((0, 0), alb, "gray", "Broadband albedo\n(what Sentinel-2 also sees)",
      0.12, 0.42)
mapax((0, 1), bit, "inferno",
      "1730 nm C–H band depth\n(bitumen — no Sentinel-2 band exists here)",
      float(np.nanpercentile(bit, 2)), float(np.nanpercentile(bit, 98)), ylab=False)
ax = mapax((0, 2), cls, "tab10", f"Material classes\nARI vs brightness-only = {ARI:.2f}",
           0, K - 1, ticks=range(K), ylab=False)

# ---- scale bar on the first panel, so the geometry is checkable by eye ------
ax0 = fig.axes[0]
bar_km = 2.0
dlon = bar_km / (111.320 * math.cos(math.radians(lat0)))
x0 = b.left + 0.012
y0 = b.bottom + (b.top - b.bottom) * 0.085
ax0.plot([x0, x0 + dlon], [y0, y0], color="#ffffff", lw=4, solid_capstyle="butt",
         zorder=5)
ax0.plot([x0, x0 + dlon], [y0, y0], color="#15202b", lw=2, solid_capstyle="butt",
         zorder=6)
ax0.text(x0 + dlon / 2, y0 + (b.top - b.bottom) * 0.045, f"{bar_km:.0f} km",
         ha="center", fontsize=8.5, color="#15202b", zorder=6,
         bbox=dict(fc="white", ec="none", alpha=.75, pad=1.2))

# ---- class spectra ---------------------------------------------------------
ax = fig.add_subplot(gs[1, :2])
order = mat.sort_values("mean_albedo").material_class.astype(int).tolist()
for k in order:
    row = mat.loc[mat.material_class == k].iloc[0]
    ax.plot(wl, z[f"class_{k}"], lw=2.6 if k == hero else 1.4,
            label=f"c{k}   α={row.mean_albedo:.3f}   ({row.pixel_share_pct:.1f}%)   "
                  f"{row.interpretation}")
for n, c in FEATURES.items():
    ax.axvspan(c - 25, c + 25, color="k", alpha=0.08)
    ax.text(c, ax.get_ylim()[1] * 0.985, n.split("_")[0], ha="center", fontsize=8)
ax.set_xlabel("Wavelength (nm)"); ax.set_ylabel("Surface reflectance")
ax.set_title("Mean spectrum per class — atmospheric water bands removed; "
             "shaded = diagnostic features; bold = the bituminous class", pad=9)
ax.legend(fontsize=9, loc="lower right", framealpha=.92)
ax.grid(alpha=0.28)
for sp in ["top", "right"]:
    ax.spines[sp].set_visible(False)

# ---- composition fingerprint ----------------------------------------------
ax = fig.add_subplot(gs[1, 2])
mz = mat.set_index("material_class")[[f"z_{n}" for n in names]]
im = ax.imshow(mz.values, cmap="RdBu_r", vmin=-2, vmax=2, aspect="auto")
ax.set_xticks(range(len(names)))
ax.set_xticklabels([n.split("_")[0] for n in names], rotation=32, ha="right", fontsize=9)
ax.set_yticks(range(len(mz)))
ax.set_yticklabels([f"c{i}" for i in mz.index], fontsize=9)
for i in range(len(mz)):
    for j in range(len(names)):
        v = mz.values[i, j]
        ax.text(j, i, f"{v:+.1f}", ha="center", va="center", fontsize=9.5,
                fontweight="bold" if abs(v) >= 1.0 else "normal",
                color="white" if abs(v) > 1.25 else "#15202b")
ax.set_title("Composition fingerprint\n(σ from scene mean)", pad=9)
ax.tick_params(length=0)
for sp in ax.spines.values():
    sp.set_visible(False)
cb = plt.colorbar(im, ax=ax, fraction=0.040, pad=0.03)
cb.outline.set_visible(False)
cb.ax.tick_params(labelsize=8.5, length=2)

fig.text(0.5, 0.012,
         f"EMIT granule EMIT_L2A_RFL_001_20260520T110418_2614007_042, 2026-05-20 15:04 local · "
         f"maps drawn at true geographic aspect ({km_w:.1f} × {km_h:.1f} km) · "
         f"the wedge is the EMIT swath corner clipping the AOI, 43.5% GLT fill",
         ha="center", fontsize=9, color="#7a8690")

fig.savefig(OUT, dpi=135, bbox_inches="tight", pad_inches=0.22)
print("wrote", OUT, round(os.path.getsize(OUT) / 1e6, 2), "MB")
