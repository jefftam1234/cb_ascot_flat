# Flat CB + ASCOT Toy Model

This folder is the flattened handoff version of the CB + ASCOT toy pricer.
It mirrors the pricing capability of `../cb_ascot/` while keeping a compact
single-module runtime (`core_pricing.py`) for easy transfer.

## Handoff Summary

- Pricing stack included: CB PDE + ASCOT PDE + Greeks sweep + QuantLib comparison.
- QuantLib-aligned default mode: `credit_spread` (TF-style blended discounting).
- Supported contract extensions: conversion windows and explicit dated schedules.
- Output basis toggle: values can be shown either per 100 face or per denomination.
- Bundle-ready inputs: split JSON folders for default and Kansai Paint examples.

For a more session-style handoff note, see `HANDOFF.md` in this same folder.

## Folder Layout

```text
cb_ascot_flat/
  core_pricing.py
  output_plotting.py
  testing.py
  requirements.txt
  HANDOFF.md
  cb_ascot_toy_model_spec.md
  json/
    default/
      market.json
      cb_ascot.json
      numerics_plotting.json
      pricer_config.json
    kansai_paint/
      market.json
      cb_ascot.json
      numerics_plotting.json
      pricer_config.json
  output/
    default/
      plot_*.png
    kansai/
      plot_*.png
  report_material/
    quantlib_regression_table.tex
    quantlib_regression_summary.tex
    includegraphics_snippets.tex
```

## Setup

```bash
python -m pip install -r requirements.txt
```

## Run Plots

Default bundle:

```bash
python output_plotting.py
```

Explicit default paths:

```bash
python output_plotting.py json/default json/default/pricer_config.json output
```

This writes plots to:

```text
output/default/
```

Kansai bundle:

```bash
python output_plotting.py json/kansai_paint json/kansai_paint/pricer_config.json output
```

This writes plots to:

```text
output/kansai/
```

You can override the output bundle name with a fourth argument:

```bash
python output_plotting.py json/kansai_paint json/kansai_paint/pricer_config.json output kansai
```

## Run Master Report Material

This generates both default and Kansai plot bundles, plus LaTeX-ready validation
material:

```bash
python master_report.py
```

Outputs:

```text
output/default/
output/kansai/
report_material/quantlib_regression_table.tex
report_material/quantlib_regression_summary.tex
report_material/includegraphics_snippets.tex
```

The includegraphics snippets use paths such as:

```latex
\includegraphics[width=0.90\textwidth]{default/plot_pv.png}
\includegraphics[width=0.90\textwidth]{kansai/plot_pv.png}
```

## Run QuantLib Regression

```bash
python testing.py
```

Current regression checks:

- default credit-spread full term sheet
- risk-free full term sheet
- credit-only no coupon/call/put

## Input Conventions

- `market.json`: market state and optional ticker-indexed stock data.
- `cb_ascot.json`: CB terms and ASCOT terms.
- `numerics_plotting.json`: solver and plotting controls.
- `pricer_config.json`: model switches (`credit_model`, `soft_call`) and output basis.

Output basis options in `pricer_config.json`:

```json
"output": {
  "basis": "per_100"
}
```

or

```json
"output": {
  "basis": "per_denomination"
}
```

## Notes

- This flat folder is intended for handoff portability.
- Ongoing development should still happen primarily in `../cb_ascot/`.
- The legacy combined `json/terms.json` format is intentionally omitted here;
  use the bundle folders under `json/default/` and `json/kansai_paint/`.
