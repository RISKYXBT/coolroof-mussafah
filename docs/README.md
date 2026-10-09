# docs/

The submission slide deck and everything needed to rebuild it.

| File | What it is |
|---|---|
| `CoolRoofPriorityIndex_T0050.pdf` | the deck — 14 slides, 16:9, text-searchable |
| `deck.html` | the deck source; every slide is a `<section class="slide">` |
| `make_figs.py` | builds `fig/f1`–`f6` from the numbers in the root `README.md` §9 |
| `fig/` | the deck figures, plus `10_emit_final.png` copied from `results/` |

The deck figures are **not** the notebooks' diagnostic panels. A notebook figure
carries six panels because it is diagnosing something; a slide carries one claim.
Every number in `make_figs.py` is traceable to a row in the root README §9, which
in turn comes from `results/summary.json` and `results/emit_final_summary.json`.

## Rebuilding

```bash
python3 docs/make_figs.py                      # regenerates fig/f1-f6
chromium --headless --no-pdf-header-footer \
  --print-to-pdf=docs/CoolRoofPriorityIndex_T0050.pdf \
  docs/deck.html
```

The deck uses the Inter typeface. `calt` and `case` are disabled in the stylesheet
on purpose: with them on, Chromium emits contextual alternate glyphs that have no
Unicode mapping, and every digit, hyphen and bracket in the exported PDF becomes
unsearchable and uncopyable.
