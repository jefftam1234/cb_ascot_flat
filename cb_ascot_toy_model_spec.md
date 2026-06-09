# CB + ASCOT Flat Toy Model Specification

This specification describes the flattened implementation in this folder.
It is intended as a practical handoff spec for rebuilding or validating the flat
version, not as a theoretical research paper.

## 1. Scope

The model prices:

- a convertible bond (CB) with American conversion, hard call, investor put,
  discrete coupons, and optional soft-call approximation;
- an ASCOT as an American call option on the CB with strike equal to recall
  price `R(t)`.

Outputs include PV and Greeks (delta, gamma, vega) over a spot sweep, plus a
QuantLib comparison harness for regression.

## 2. Core Model Choices

### 2.1 Equity process

Single-factor equity process under risk-neutral measure:

$$
dS_t = (r-q)S_t dt + \sigma S_t dW_t
$$

with flat `r`, `q`, `sigma` over the horizon.

### 2.2 Credit handling

Two modes:

- `credit_spread` (default): TF-style blended discounting with conversion
  probability, aligned to the QuantLib comparison convention.
- `hazard_recovery`: reduced-form jump-to-default style PDE with hazard/recovery
  source term.

Default validation and reporting should be interpreted through `credit_spread`.

## 3. Contract Features

### 3.1 Convertible bond

Supported CB features:

- conversion floor;
- hard call cap;
- put floor on put dates;
- coupons on coupon dates;
- conversion window via `conversion_start_time` / `conversion_end_time`;
- explicit schedules via `coupon_dates`, `coupon_amounts`, `put_dates`,
  `call_dates`.

When explicit schedules are absent, periodic schedules are generated from
frequency/start fields.

### 3.2 ASCOT

ASCOT is solved as an American option on the CB surface with obstacle:

$$
A(S,t) \ge CB(S,t) - R(t)
$$

Recall models:

- `linear`
- `swap_pv`

## 4. Numerics

- Spatial coordinate: log-spot.
- Time stepping: Crank-Nicolson.
- LCP solver: PSOR (single/double obstacle).
- Shared grid for CB and ASCOT for tight coupling.

## 5. Input Format

Use split bundle folders under `json/`.

Each bundle contains:

- `market.json`
- `cb_ascot.json`
- `numerics_plotting.json`
- `pricer_config.json`

Typical bundles in this folder:

- `json/default/`
- `json/kansai_paint/`

## 6. Output Basis

`pricer_config.json` supports an output basis switch:

- `per_100`
- `per_denomination`

If `per_denomination` is selected and `cb.denomination` exists, reported values
are scaled by:

$$
\text{scale} = \frac{\text{denomination}}{\text{face}}
$$

Core PDE valuation remains unchanged; only displayed/reporting values are scaled.

## 7. Validation Expectations

Regression harness (`testing.py`) compares local CB prices vs QuantLib on the
same terms and should pass baseline tolerances in default setup.

## 8. Commands

Setup:

```bash
python -m pip install -r requirements.txt
```

Run default plots:

```bash
python output_plotting.py
```

Run regression:

```bash
python testing.py
```

Run Kansai bundle plots:

```bash
python output_plotting.py json/kansai_paint json/kansai_paint/pricer_config.json output
```
