# ASCOT Greeks — Economic Commentary

This document explains the economic intuition behind the seven output plots produced by
`master_report.py` for each input bundle (default and Kansai Paint).  It covers why the
full American ASCOT, its intrinsic approximation, and the raw CB proxy behave differently
across the spot range.

---

## 1. Instrument structure recap

**ASCOT (Asset Swap with Call Option on Term)** is an American call option on a
convertible bond (CB), struck at an accreting recall price R(t).

| Quantity | Definition |
|---|---|
| ASCOT intrinsic | `max(CB(S, 0) − R(0), 0)` — immediate exercise value at inception |
| ASCOT full | American option value solved via PDE — includes time value |
| CB proxy | Raw CB price, used as a naïve upper proxy for ASCOT sensitivity |
| Time value | `ASCOT full − ASCOT intrinsic ≥ 0` by American option theory |

Market convention prices the ASCOT as its intrinsic value.  The full model prices it as
a true American option.  The gap between them is the subject of much of this analysis.

---

## 2. PV plot — what the time value region means

The shaded region between the full and intrinsic PV curves is the **American time value**.
It peaks near the ATM crossing point (where CB ≈ R₀) and shrinks toward zero as the ASCOT
goes deeply in-the-money.

**Why does time value exist at all, if early exercise is almost always optimal?**

There are two forces that make waiting expensive:
1. **Coupon bleed**: CB coupons flow to the asset-swap buyer, not the ASCOT holder; every
   day unexercised is a day of foregone coupon.
2. **Strike accretion**: R(t) accretes upward over time (the swap PV declines toward zero
   at maturity, so the recall price rises), which erodes the intrinsic value.

Both forces argue for exercising immediately — yet the ASCOT holder still waits.  The
**only** rational reason to hold unexercised is the **right to walk away**: if credit
deteriorates before maturity, the holder can simply let the ASCOT expire worthless rather
than taking delivery of a distressed CB.  That walk-away right is the entirety of the
American time value.

---

## 3. CS01 plot — why ASCOT full CS01 ≈ 0

CS01 is computed as `dPV / dλ` where λ is the hazard rate proxy for credit spread.

### CB CS01
When λ rises, the CB discount rate rises on the bond-like nodes (via the
Tsiveriotis–Fernandes blended discount `r + λ(1 − p_conv)`), so CB PV falls.
`CB_CS01 < 0` and is large in magnitude across the whole spot range.

### ASCOT intrinsic CS01
`Intrinsic = max(CB − R₀, 0)`, so `d(Intrinsic)/dλ = dCB/dλ × 1{CB > R₀}`.  This equals
CB CS01 when in-the-money, and is exactly zero when out-of-the-money.  It is therefore a
poor proxy in both regimes (see below).

### ASCOT full CS01 — the near-zero result

When λ rises by 1bp, two opposing effects act on the full ASCOT value:

| Effect | Direction | Mechanism |
|---|---|---|
| Intrinsic erodes | Negative | CB falls → CB − R₀ falls |
| Walk-away put gains | Positive | Higher spread → higher probability of a large credit move → walk-away right is worth more |

These two effects **substantially offset** each other.  The net `CS01_full` is much smaller
in magnitude than `CB_CS01`.

**Why the offset is economic, not a PDE artefact:**
The ASCOT PDE uses clean risk-free discounting (no λ term in the ASCOT PDE itself).
Credit enters only through the CB obstacle.  So the ASCOT is fundamentally a call on an
asset that has credit risk; holding the ASCOT rather than the CB means you are **long the
walk-away right** on that credit risk.  The equity-option layer insulates the ASCOT holder
from default: if the CB defaults, the ASCOT expires worthless — no delivery obligation.

**Why `Intrinsic CS01 = CB_CS01 × 1{CB > R₀}` is a bad proxy:**

- **Out-of-the-money region**: Intrinsic CS01 = 0, but full CS01 is small and negative
  (the time value itself has modest credit sensitivity).  The proxy understates the
  exposure.
- **In-the-money region**: Intrinsic CS01 = CB CS01, but full CS01 << CB CS01 because the
  walk-away put partially offsets.  The proxy overstates the exposure — sometimes by a
  factor of 5–10×.

The correct intuition: the ASCOT holder is an **equity option holder, not a bond holder**.
The credit-spread widening corrodes the CB (the underlying), but the optionality of the
ASCOT partially shields that loss.  The CB CS01 proxy ignores this shield entirely.

---

## 4. Vega plot — why full > intrinsic everywhere, and how it compares to CB

### Full vs intrinsic

`ASCOT full = intrinsic + walk-away put`

The walk-away put gains value when vol rises (higher vol → fatter tails → greater chance
of a large adverse move in credit/equity → walk-away right is worth more).  Therefore:

`vega_full = vega_intrinsic + vega_walk_away > vega_intrinsic` always.

In the OTM region, `vega_intrinsic = 0` but `vega_full > 0`: the full ASCOT retains vol
sensitivity from the out-of-the-money optionality itself.

### Full vs CB — the interesting comparison

Whether `vega_full` is greater or less than `CB_vega` depends on **what the CB's own vega
is** in the relevant spot region.  The ASCOT interacts with CB vega through two competing
mechanisms:

1. **Dilution** (reduces vega relative to CB): ASCOT is a call option on the CB, so it
   only partially participates in CB moves.  In the OTM region, `Δ_{ASCOT/CB} < 1`, which
   suppresses `vega_full` relative to `CB_vega`.
2. **Amplification** (increases vega relative to CB): The walk-away put adds a positive
   vega component on top of whatever the CB contributes.

The relative magnitude of these two effects differs between the default and Kansai bundles.

---

## 5. Default vs Kansai — vega comparison by region

### Default bundle (short maturity)

At low spot values (OTM ASCOT region), the CB's embedded equity option is deep out-of-the-
money.  The CB trades close to bond floor — essentially a straight bond.  Therefore
`CB_vega ≈ 0` in the OTM region.

Even though `vega_full` is small in absolute terms in the OTM region, it exceeds the
near-zero `CB_vega`.  As spot rises through the ATM crossing and into the ITM region, the
walk-away put adds its own vega on top of CB vega, keeping `vega_full > CB_vega`
throughout.

**Default pattern: `vega_full > CB_vega` across the entire spot range.**

### Kansai bundle (long maturity)

Kansai Paint is a long-dated CB.  Even at the lower end of its spot range, the CB's
embedded equity option has real time value (long maturity keeps the equity option alive).
`CB_vega` is therefore non-trivial throughout the range, not near-zero.

In the OTM ASCOT region (CB < R₀), the dilution effect dominates: the ASCOT is an OTM
call on the CB with `Δ_{ASCOT/CB} < 1`, so it captures only a fraction of `CB_vega`.
The walk-away component at this point is also OTM, so its vega contribution is limited.
The net result is `vega_full < CB_vega` in the OTM region.

Once the ASCOT crosses into the ITM region (CB > R₀), the walk-away put adds back
positive vega on top of `CB_vega`, and `vega_full > CB_vega` resumes.

**Kansai pattern: `vega_full < CB_vega` in the OTM region; `vega_full > CB_vega` in the
ITM region.**

| Region | Default | Kansai | Root cause |
|---|---|---|---|
| Deep OTM | `full > CB` | `full < CB` | Default: CB equity option dead → CB_vega ≈ 0. Kansai: CB equity option alive → CB_vega meaningful; ASCOT dilution (Δ<1) wins. |
| ATM crossing | `full > CB` | `full > CB` | Walk-away put is near-ATM → maximum own-optionality vega for both. |
| ITM | `full > CB` | `full > CB` | Walk-away put vega adds to CB_vega in both cases. |
| Deep ITM | `full → CB` | `full → CB` | Walk-away put goes deep OTM → time-value vega → 0; full vega converges to CB_vega. |

The core asymmetry between the two bonds is entirely explained by the maturity of the CB's
embedded equity option.  Short-dated bonds (default) have a near-dead equity option at low
spots; long-dated bonds (Kansai) preserve a live equity option throughout their realistic
spot range.

---

## 6. Delta and Gamma plots

**Delta** (`∂PV/∂S`) follows logically from the above:

- `delta_intr = kappa × 1{CB > R₀} × delta_cb_equity` — zero when OTM, ramps through 1
  as the ASCOT goes deep ITM.
- `delta_full` is smooth across the ATM crossing (American option has no kink at exercise
  boundary; the smooth-pasting condition applies).
- `delta_cb` (CB proxy) overstates ASCOT delta because the CB holder has full delta
  exposure to the equity, while the ASCOT holder's equity exposure is filtered through the
  call on CB structure.

**Gamma** is positive throughout for the full ASCOT (it is an option; you are always long
convexity).  The intrinsic gamma is spike-like at the ATM crossing (reflecting the
indicator-function kink) and zero elsewhere.  The full model smooths this out.

---

## 7. IR01 plot

IR01 (`∂PV/∂r`) for the ASCOT has both a direct and indirect channel:

- **Direct**: The ASCOT PDE discounts at the risk-free rate r; lower r → higher PV.
- **Indirect**: r affects both CB valuation and the recall price R(t) (the recall price is
  computed as a discounted cash-flow on the swap leg).  A consistent IR01 bump shifts both
  simultaneously.

The ASCOT IR01 is smaller in magnitude than CB IR01 for the same reason as CS01: the
ASCOT filters interest-rate sensitivity through its own delta on the CB.  In the ITM
region the two converge (deep-ITM ASCOT ≈ CB − R₀, both sensitive to r).  In the OTM
region the ASCOT has positive IR01 via the time value alone (lower r makes the OTM call
more valuable through its optionality), which can differ in sign from the CB IR01.
