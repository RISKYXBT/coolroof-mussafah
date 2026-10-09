#!/usr/bin/env python3
"""Bespoke figures for the submission deck.

These are NOT the notebook's diagnostic figures. A deck slide carries one claim;
the notebook panels carry six. Every number here is traceable to README.md §9.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = os.path.dirname(os.path.abspath(__file__)) + "/fig"
os.makedirs(OUT, exist_ok=True)

NAVY = "#1f3a5f"
RED = "#c62828"
AMBER = "#ef6c00"
GREY = "#9aa5b1"
LIGHT = "#e7ebef"
INK = "#15202b"

plt.rcParams.update({
    "font.family": "Inter",
    "font.size": 15,
    "axes.edgecolor": "#c3ccd5",
    "axes.labelcolor": INK,
    "text.color": INK,
    "xtick.color": "#5b6770",
    "ytick.color": "#5b6770",
    "axes.titlesize": 17,
    "axes.titleweight": 600,
    "axes.titlecolor": INK,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
})


def finish(fig, name, pad=0.25):
    fig.savefig(f"{OUT}/{name}.png", dpi=200, bbox_inches="tight", pad_inches=pad)
    plt.close(fig)
    print("  ", name)


# ---------------------------------------------------------------------------
# F1 · the headline: albedo sensitivity, three methods + the error we caught
# ---------------------------------------------------------------------------
def f1_sensitivity():
    fig, ax = plt.subplots(figsize=(11, 3.5))

    rows = [
        ("Random forest + WorldCover\n(adopted)", -5.86, -7.54, -4.35, NAVY, True),
        ("NDBI > 0 alone  —  rejected", +20.49, None, None, RED, False),
    ]
    ys = np.arange(len(rows))[::-1]

    ax.axvline(0, color="#aab4bd", lw=1.2, zorder=1)
    for y, (lab, v, lo, hi, col, bold) in zip(ys, rows):
        if lo is not None:
            ax.plot([lo, hi], [y, y], color=col, lw=7, alpha=0.22,
                    solid_capstyle="round", zorder=2)
            ax.plot([lo, lo], [y - .14, y + .14], color=col, lw=2.4, zorder=3)
            ax.plot([hi, hi], [y - .14, y + .14], color=col, lw=2.4, zorder=3)
        ax.scatter([v], [y], s=230 if bold else 140, color=col, zorder=4,
                   edgecolor="white", linewidth=1.6)
        ax.text(v, y + .30, f"{v:+.2f}", ha="center", va="bottom",
                fontsize=15 if bold else 13,
                fontweight="bold" if bold else "normal", color=col)

    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in rows], fontsize=13.5)
    ax.get_yticklabels()[0].set_fontweight("bold")
    ax.set_xlim(-10.5, 24.5)
    ax.set_ylim(-0.95, len(rows) - 0.05)
    ax.set_xlabel("Slope  (°C per unit of surface albedo)", fontsize=14)
    ax.text(0.0, -0.32, "300 spatial block bootstraps · 175,033 px in 188 blocks · "
            "both masks are computed on every run and both values kept in summary.json",
            transform=ax.transAxes, fontsize=10.5, color="#8a949d")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", alpha=0.22, lw=0.8)

    ax.annotate("sign-inverted — water (dark + cold) and\nbright sabkha (bright + hot) "
                "in the mask.\nWe caught it; both values stay in summary.json.",
                xy=(20.49, 0), xytext=(12.6, 1.42), fontsize=11.5, color=RED,
                ha="center", linespacing=1.4,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.4,
                                connectionstyle="arc3,rad=-0.22"))
    ax.text(-3.4, 1.0, "95% CI  [−7.54, −4.35]", fontsize=12, color="#4a5a6a",
            ha="left", va="center")
    finish(fig, "f1_sensitivity")


# ---------------------------------------------------------------------------
# F2 · why ranking matters: benefit concentration
# ---------------------------------------------------------------------------
def f2_concentration():
    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    labels = ["Untargeted\n(any 100 roofs)", "Ranked\n(our top 100)"]
    vals = [2.8, 20.9]
    bars = ax.bar(labels, vals, width=0.52, color=[GREY, NAVY], zorder=3)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, v + 0.7, f"{v:.1f}%",
                ha="center", fontsize=19, fontweight="bold",
                color=b.get_facecolor())
    ax.set_ylabel("Share of the district's available cooling", fontsize=13.5)
    ax.set_ylim(0, 26)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.22, lw=0.8)
    ax.annotate("", xy=(1, 20.8), xytext=(0, 2.8),
                arrowprops=dict(arrowstyle="-|>", color=AMBER, lw=2.6,
                                connectionstyle="arc3,rad=-0.35"))
    ax.text(0.5, 13.6, "7.5×", fontsize=26, fontweight="bold", color=AMBER,
            ha="center")
    ax.set_title("100 roofs out of 3,603 — which 100 decides the outcome",
                 pad=14, fontsize=15)
    finish(fig, "f2_concentration")


# ---------------------------------------------------------------------------
# F3 · classifier: what the escalation bought
# ---------------------------------------------------------------------------
def f3_classifier():
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    metrics = ["accuracy", "precision", "recall", "F1", "IoU"]
    ndbi = [0.458, 0.422, 0.844, 0.563, 0.392]
    rf = [0.768, 0.673, 0.854, 0.753, 0.604]
    x = np.arange(len(metrics)); w = 0.37
    ax.bar(x - w/2, ndbi, w, label="NDBI > 0 baseline", color=GREY, zorder=3)
    ax.bar(x + w/2, rf, w, label="Random forest + texture", color=NAVY, zorder=3)
    for i, (xi, v) in enumerate(zip(x - w/2, ndbi)):
        pass
        ax.text(xi, v + .018, f"{v:.3f}", ha="center", fontsize=11, color="#6b7680")
    for i, (xi, v) in enumerate(zip(x + w/2, rf)):
        ax.text(xi, v + .018, f"{v:.3f}", ha="center", fontsize=11.5,
                fontweight="bold", color=NAVY)
    ax.set_xticks(x); ax.set_xticklabels(metrics, fontsize=13)
    ax.set_ylim(0, 1.0); ax.set_ylabel("Score on held-out spatial blocks", fontsize=13)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.22, lw=0.8)
    ax.legend(frameon=False, fontsize=12.5, loc="upper left",
              bbox_to_anchor=(0.005, 1.03), ncol=2)
    ax.text(0.5, -0.22, "2 km blocks · 60/40 split · n = 95,346 test pixels · "
            "recall is unchanged, so the whole gain is in false positives: "
            "45,533 → 16,345",
            transform=ax.transAxes, ha="center", fontsize=11, color="#5b6770")
    finish(fig, "f3_classifier", pad=0.35)


# ---------------------------------------------------------------------------
# F4 · the hyperspectral payoff: composition fingerprints
# ---------------------------------------------------------------------------
def f4_fingerprint():
    classes = ["c3", "c2", "c1", "c4", "c0"]
    share = [12.5, 13.9, 24.7, 30.1, 18.9]
    albedo = [0.250, 0.270, 0.271, 0.284, 0.324]
    feats = ["Fe-oxide\n900 nm", "Bitumen\n1730 nm", "Al–OH\n2200 nm",
             "Carbonate\n2340 nm"]
    Z = np.array([
        [-1.9, +0.2, -0.9, +0.1],   # c3
        [+0.5, +1.2, +1.4, -0.7],   # c2
        [+0.0, +0.4, -0.6, +0.0],   # c1
        [+0.4, -0.7, -0.1, -0.6],   # c4
        [+0.3, -0.5, +0.5, +1.3],   # c0
    ])
    reading = ["iron-depleted; possibly shadowed",
               "BITUMINOUS + CEMENT-BEARING  ←  the result",
               "spectrally average", "spectrally average",
               "carbonate — bare sabkha sand"]

    fig, ax = plt.subplots(figsize=(10.6, 4.5))
    im = ax.imshow(Z, cmap="RdBu_r", vmin=-2, vmax=2, aspect="auto")
    ax.set_xticks(range(4)); ax.set_xticklabels(feats, fontsize=12.5)
    ax.set_yticks(range(5))
    ax.set_yticklabels([f"{c}   {s:.1f}%   α={a:.3f}"
                        for c, s, a in zip(classes, share, albedo)], fontsize=12.5)
    ax.get_yticklabels()[1].set_fontweight("bold")
    for i in range(5):
        for j in range(4):
            v = Z[i, j]
            ax.text(j, i, f"{v:+.1f}", ha="center", va="center", fontsize=13,
                    fontweight="bold" if abs(v) >= 1.0 else "normal",
                    color="white" if abs(v) > 1.25 else INK)
        ax.text(3.68, i, reading[i], va="center", fontsize=12,
                color=NAVY if i == 1 else "#5b6770",
                fontweight="bold" if i == 1 else "normal")
    ax.add_patch(Rectangle((-0.5, 0.5), 4, 1, fill=False, edgecolor=NAVY,
                           lw=2.4, zorder=5))
    ax.set_xlim(-0.5, 8.6)
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.text(3.68, 4.95, "red = enriched vs the scene mean   ·   blue = depleted",
            fontsize=11, color="#8a949d", va="center")
    ax.set_title("Adjusted Rand Index against brightness-only clustering = 0.092  —  "
                 "composition is almost independent of albedo",
                 fontsize=13.5, pad=12, loc="left")
    finish(fig, "f4_fingerprint", pad=0.3)


# ---------------------------------------------------------------------------
# F5 · what a decade of Landsat actually shows, including the null
# ---------------------------------------------------------------------------
def f5_warming():
    fig, ax = plt.subplots(figsize=(9.4, 4.3))
    labels = ["Built-up vs desert,\ntoday",
              "Built fabric warming\nvs desert, per decade",
              "Desert→built conversion,\nextra warming"]
    vals = [2.35, 0.23, -0.028]
    cols = [RED, AMBER, GREY]
    stats = ["53.82 vs\n51.48 °C", "t = 47.0\nd = 0.24", "d = −0.025\n(negligible)"]
    bars = ax.bar(labels, vals, width=0.46, color=cols, zorder=3)
    for b, v, s in zip(bars, vals, stats):
        xc = b.get_x() + b.get_width()/2
        ax.text(xc, v + 0.085 if v > 0 else 0.16, f"{v:+.2f} °C",
                ha="center", fontsize=17, fontweight="bold", color=b.get_facecolor())
        ax.text(xc, -0.32, s, ha="center", fontsize=11, color="#5b6770")
    ax.axhline(0, color="#aab4bd", lw=1.2)
    ax.set_ylabel("Δ surface temperature (°C)", fontsize=13)
    ax.set_ylim(-0.52, 2.95)
    ax.spines[["top", "right", "bottom"]].set_visible(False)
    ax.grid(axis="y", alpha=0.22, lw=0.8)
    ax.tick_params(axis="x", length=0, pad=26, labelsize=12.5)
    ax.text(2, 1.30, "flagged significant, and meaningless —\nd = 0.025 with n in the "
            "hundreds of thousands.\nThat land was already 2.48 °C hotter\nbefore anything "
            "was built on it.",
            fontsize=11, color="#4a5a6a", ha="center", va="bottom", linespacing=1.5)
    ax.set_title("The heat problem is intensifying inside the city that already exists",
                 fontsize=15, pad=12, loc="left")
    finish(fig, "f5_warming", pad=0.3)


# ---------------------------------------------------------------------------
# F6 · the pipeline, as a diagram
# ---------------------------------------------------------------------------
def f6_pipeline():
    fig, ax = plt.subplots(figsize=(12.4, 3.5))
    ax.set_xlim(0, 100); ax.set_ylim(0, 34); ax.axis("off")

    stages = [
        ("Landsat 8/9 C2 L2\n80 scenes, 2 epochs", "surface temperature\n+ reflectance"),
        ("Sentinel-2 L2A\n20 scenes", "broadband albedo\nBonafoni 2020"),
        ("NASA EMIT L2A\n230 bands, 60 m", "material class\nband depths"),
        ("OpenStreetMap\n8,503 footprints", "3,603 roofs\n>400 m²"),
    ]
    w, gap = 20.5, 5.8
    for i, (src, got) in enumerate(stages):
        x = i * (w + gap)
        ax.add_patch(Rectangle((x, 19), w, 13, facecolor=LIGHT,
                               edgecolor="#c3ccd5", lw=1.2, zorder=2))
        ax.text(x + w/2, 27.4, src, ha="center", va="center", fontsize=11.5,
                fontweight=600, color=INK, linespacing=1.35)
        ax.text(x + w/2, 22.2, got, ha="center", va="center", fontsize=10.5,
                color="#5b6770", style="italic", linespacing=1.3)
        ax.annotate("", xy=(x + w/2, 13.2), xytext=(x + w/2, 18.6),
                    arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.8))

    ax.add_patch(Rectangle((0, 5.5), 3*(w+gap) + w, 7.4, facecolor=NAVY,
                           edgecolor="none", zorder=2))
    ax.text((3*(w+gap)+w)/2, 9.2,
            "zonal statistics per roof  →  ΔT = 4.56 × (0.60 − α)  →  "
            "ranked worklist, three objectives",
            ha="center", va="center", fontsize=13, color="white",
            fontweight=600)
    ax.text((3*(w+gap)+w)/2, 1.8,
            "every input free and open · no credentials · reproducible from the repo",
            ha="center", va="center", fontsize=11, color="#5b6770")
    finish(fig, "f6_pipeline", pad=0.15)


if __name__ == "__main__":
    print("figures ->", OUT)
    f1_sensitivity()
    f2_concentration()
    f3_classifier()
    f4_fingerprint()
    f5_warming()
    f6_pipeline()
    print("done")


# ---------------------------------------------------------------------------
# F7 · the roof-level cross-section does not confirm the pixel-level effect
# ---------------------------------------------------------------------------
def f7_roof_confound():
    import pandas as pd, scipy.stats as sps
    r = pd.read_csv("/home/claude/run2/results/roof_priority_ranked.csv")
    r["q"] = pd.qcut(r.area_m2, 5, labels=False)
    xs, ys, ps, ns, med = [], [], [], [], []
    for q in range(5):
        s = r[r.q == q]
        lr = sps.linregress(s.albedo, s.lst_c)
        xs.append(q); ys.append(lr.slope); ps.append(lr.pvalue)
        ns.append(len(s)); med.append(s.area_m2.median())
    big = r[r.area_m2 >= 5000]
    lrb = sps.linregress(big.albedo, big.lst_c)

    fig, ax = plt.subplots(figsize=(10.4, 4.5))
    cols = [RED if p < 0.01 else AMBER if p < 0.05 else GREY for p in ps]
    ax.bar(xs, ys, width=.52, color=cols, zorder=3)
    for x, y, p, n in zip(xs, ys, ps, ns):
        ax.text(x, y + .28, f"{y:+.1f}", ha="center", fontsize=14,
                fontweight="bold", color=RED if p < .01 else AMBER if p < .05 else GREY)
        ax.text(x, -0.75, f"n={n}", ha="center", fontsize=9.5, color="#7a8690")

    ax.bar([5.1], [lrb.slope], width=.52, color=GREY, zorder=3)
    ax.text(5.1, lrb.slope + .28, f"{lrb.slope:+.1f}", ha="center", fontsize=14,
            fontweight="bold", color=GREY)
    ax.text(5.1, -0.75, f"n={len(big)}", ha="center", fontsize=9.5, color="#7a8690")
    ax.text(5.1, lrb.slope + 1.25, f"p = {lrb.pvalue:.2f}\nnot significant",
            ha="center", fontsize=10.5, color="#4a5a6a", linespacing=1.4)

    ax.axhline(0, color="#aab4bd", lw=1.2)
    ax.axhline(-5.86, color=NAVY, lw=2, ls="--", zorder=2)
    ax.text(-0.42, -5.86, " pixel-level marginal effect  −5.86", va="bottom",
            fontsize=11, color=NAVY, fontweight=600)

    ax.set_xticks(xs + [5.1])
    ax.set_xticklabels([f"Q{q+1}\n{m:,.0f} m²\n{m/900:.1f} px" for q, m in zip(xs, med)]
                       + ["≥5,000 m²\n~5.5 px\n(cleanest)"], fontsize=10)
    ax.set_ylabel("Roof-level slope\n(°C per unit albedo)", fontsize=12)
    ax.set_ylim(-7.4, 11.0)
    ax.spines[["top", "right", "bottom"]].set_visible(False)
    ax.tick_params(axis="x", length=0, pad=16)
    ax.grid(axis="y", alpha=0.22, lw=0.8)
    ax.set_title("Between buildings, brighter roofs are not cooler. The association is "
                 "strongest where\nthe thermal pixel is dirtiest — but it does not vanish "
                 "when the pixel is clean.",
                 fontsize=13.5, pad=12, loc="left")
    finish(fig, "f7_roof_confound", pad=0.3)
