# Flat CB + ASCOT Handoff

This folder is the flattened delivery package for the CB + ASCOT toy model.
It mirrors the pricing behavior in `../cb_ascot/` while keeping a minimal file
layout for easier transfer to another machine.

## What Is Included

- Convertible bond PDE pricer (American conversion, hard call, put, coupons,
  optional soft-call proxy).
- ASCOT PDE pricer (American call on the CB with linear or swap-PV recall).
- Greeks sweep (PV, delta, gamma, vega).
- QuantLib regression harness.

## Current Input Organization

Inputs are split into bundle folders under `json/`:

- `json/default/`: baseline toy inputs.
- `json/kansai_paint/`: Kansai bundle with relevant transcribed terms.

Each bundle contains:

- `market.json`
- `cb_ascot.json`
- `numerics_plotting.json`
- `pricer_config.json`

## Pricing Conventions

- Default credit mode: `credit_spread` (QuantLib-aligned TF blended discounting).
- Alternative mode: `hazard_recovery` is available.
- Put/coupon ordering follows the same QuantLib comparison convention used in
  the main codebase (`coupon_paid_on_put=true` default).
- Conversion windows and explicit schedules are supported:
  `conversion_start_time`, `conversion_end_time`, `coupon_dates`,
  `coupon_amounts`, `put_dates`, `call_dates`.

## Output Basis Toggle

`pricer_config.json` supports:

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

When `per_denomination` is selected and `cb.denomination` is provided, displayed
PV/Greeks and comparison output are scaled by `denomination / face`.

## Latest Validation

Flat regression currently passes:

- default credit-spread full term sheet
- risk-free full term sheet
- credit-only no coupon/call/put

Run command:

```bash
python testing.py
```

## Portability Setup

```bash
python -m pip install -r requirements.txt
```

## Report Material

Run the master report script before shipping:

```bash
python master_report.py
```

It writes:

- `output/default/`
- `output/kansai/`
- `report_material/quantlib_regression_table.tex`
- `report_material/quantlib_regression_summary.tex`
- `report_material/includegraphics_snippets.tex`

The `includegraphics` snippets intentionally reference paths such as
`default/plot_pv.png` and `kansai/plot_pv.png`, so the `default/` and `kansai/`
output folders can be copied directly next to the LaTeX source.

## Recommended Next Steps

- Keep feature development in `../cb_ascot/` and backport here only when stable.
- If shipping externally, include both `json/default/` and `json/kansai_paint/`.
- The old combined `json/terms.json` input is not used in this flat handoff.
