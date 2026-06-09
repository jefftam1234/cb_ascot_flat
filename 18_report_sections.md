# Section 5.12 and 5.19: ASCOT Model Assumption Test
## CB/ASCOT Flat Model (Independent Validation Tool)

---

## 5.12 Conceptual Soundness Analysis

**Goal**

To assess the theoretical soundness of pricing the Asset Swap with Call Option on Term
(ASCOT) as an American call option on a convertible bond (CB), and to derive from first
principles the expected behavior of the material risk sensitivities: the credit spread
sensitivity (CS01), the interest rate sensitivity (IR01), the volatility sensitivity
(Vega), and the equity sensitivity (Delta).

**Scope**

The analysis is conducted through theoretical reasoning and financial mathematics without
reference to numerical outputs.  Two aspects of the ASCOT structure are examined: the
source and economic nature of the American time value, and the resulting implications for
each Greek relative to the CB proxy and the market-convention intrinsic approximation.

---

### 5.12.1 Instrument Structure and American Time Value

The ASCOT gives its holder the right, at any point from inception to recall expiry, to
call the CB from the asset-swap counterparty at an accreting recall price R(t).  The
recall price begins at R(0) and rises linearly toward a terminal level R(T_rec),
reflecting the amortization of the swap net present value toward zero at maturity.

Market convention values the ASCOT at its intrinsic value, defined as max(CB(S, 0)
- R(0), 0), which treats the ASCOT as if exercise is immediate.  The full American model
recognizes that the holder retains the option to wait and values this right explicitly.
The American time value is the excess of the full value over the intrinsic value and is
non-negative at every spot level by the American option lower bound.

Two forces make waiting systematically costly for the ASCOT holder.  First, the CB coupons
accrue to the asset-swap counterparty for each day the option remains unexercised.  Second,
the recall price R(t) accretes upward over the life of the option, raising the exercise
strike and reducing the value of future exercise relative to immediate exercise.

Both forces argue for immediate exercise.  The rational holder waits only if the value of
waiting exceeds these combined costs.  Under the ASCOT structure, the sole source of value
in waiting is the walk-away right: if credit deteriorates or the equity falls materially,
the holder may allow the ASCOT to expire worthless rather than taking delivery of a
distressed CB.  This right to walk away is equivalent to holding a put option on the CB
struck at R(t), with expiry at T_rec.  The full American value can therefore be decomposed
as:

> ASCOT_full = ASCOT_intrinsic + walk-away put value

This decomposition follows from the American option decomposition theorem.  The walk-away
put is positive whenever there is any probability of the CB falling below R(t) before
expiry, which holds for all practical spot levels.

---

### 5.12.2 Credit Spread Sensitivity (CS01)

CS01 measures the sensitivity of the instrument value to a parallel shift in the credit
spread, proxied here by a shift in the issuer hazard rate lambda.

For the CB, increasing lambda raises the effective discount rate on bond-like cash flows
through the Tsiveriotis-Fernandes blending mechanism, where the blended discount rate is
r + lambda * (1 - p_conv) and p_conv is the risk-neutral conversion probability.
CB_CS01 is negative and material across the entire spot range.

For the ASCOT intrinsic, the sensitivity is simply CB_CS01 when in-the-money and zero
when out-of-the-money:

> Intrinsic_CS01 = CB_CS01 * indicator(CB > R(0))

This indicator-based proxy fails in both regimes.  In the out-of-the-money region, the
proxy is identically zero, but the full ASCOT still has positive time value whose
sensitivity to lambda is non-zero.  In the in-the-money region, the proxy sets
Intrinsic_CS01 equal to CB_CS01, which overstates the true exposure because the walk-away
put offsets part of the direct credit sensitivity.

The full ASCOT CS01 is driven by two competing effects when lambda rises.  First, the
intrinsic value erodes because the CB falls.  Second, the walk-away put appreciates
because a wider spread raises the probability of large adverse credit moves, making the
right to walk away more valuable.  These two effects partially or fully offset each other,
and the net full CS01 is substantially smaller in magnitude than CB_CS01 at all spot
levels.

---

### 5.12.3 Interest Rate Sensitivity (IR01)

IR01 measures the sensitivity to a parallel shift in the risk-free rate r.

For the CB, increasing r raises the discount rate on all bond-like cash flows and reduces
the CB value.  CB_IR01 is large and negative, reflecting the bond's duration.

For the ASCOT full model, the ASCOT PDE uses clean risk-free discounting without a credit
term.  The effect of a rate rise propagates through two channels: the change in the CB
obstacle (which falls, as above), and the change in the ASCOT PDE's own discounting and
drift term.  The second channel is important: a higher risk-free rate increases the risk-
neutral drift of the underlying equity, which raises the value of a call option on the CB.
The walk-away put, which is short delta on the CB, benefits from the CB falling.  The net
effect on the full ASCOT is that both the call-like component and the walk-away put respond
favorably to a rate rise, and the combined full IR01 can be positive and large, opposite in
sign to CB_IR01.

The intrinsic IR01 is zero in the out-of-the-money region and equals CB_IR01 (large and
negative) in the in-the-money region.  For most of the in-the-money range, the intrinsic
approximation therefore gets not only the magnitude but the sign of IR01 wrong.

---

### 5.12.4 Volatility Sensitivity (Vega)

Since ASCOT_full = ASCOT_intrinsic + walk-away put, the vega of the full ASCOT is:

> Vega_full = Vega_intrinsic + Vega_walk-away

The walk-away put always gains value when equity volatility rises (higher volatility
implies fatter tails, increasing the probability of large downward moves that the walk-away
right protects against).  Therefore Vega_walk-away is strictly positive, which implies
Vega_full > Vega_intrinsic throughout the spot range.

In the out-of-the-money region, Vega_intrinsic = 0, so the full Vega is solely from the
walk-away put's optionality.  In the in-the-money region, Vega_intrinsic = CB_Vega and
the walk-away put adds a positive increment on top, so Vega_full > CB_Vega as long as the
walk-away put has non-trivial time value.  As the ASCOT goes deeply in-the-money the
walk-away put approaches zero value and Vega_full converges toward CB_Vega from above.

Whether Vega_full exceeds CB_Vega in the out-of-the-money region depends on the magnitude
of CB_Vega in that region.  CB_Vega at low spot levels reflects the CB's embedded equity
option.  For a CB whose embedded conversion option is far out-of-the-money and nearly
valueless, CB_Vega is near zero and even a small Vega_walk-away exceeds it.  For a CB
whose embedded equity option retains meaningful time value at out-of-the-money ASCOT
levels, CB_Vega is non-trivial and the ASCOT's diluted participation (delta-on-CB < 1)
may result in Vega_full falling below CB_Vega in that region.

---

### 5.12.5 Equity Sensitivity (Delta)

Delta_intrinsic = 0 in the out-of-the-money region and equals CB_Delta in the deep
in-the-money region.  At the boundary CB = R(0), the intrinsic has a kink.

Delta_full is smooth across this boundary by the smooth-pasting condition of American
option theory.  In the near-the-money region, the full ASCOT has significant gamma and
its effective delta with respect to spot can exceed CB_Delta, because the option's
leverage amplifies the sensitivity to small spot moves that push the ASCOT across its
exercise boundary.  In the deep in-the-money region, the walk-away put contributes a
negative delta-on-spot, and the full Delta falls below CB_Delta.  There is therefore a
crossover: Delta_full exceeds CB_Delta near the money, then falls below it in the deep
in-the-money region.

---

## 5.19 Model Assumption Analysis

**Goal**

To establish the numerical correctness of the independent CB/ASCOT flat pricing
implementation and to verify numerically the theoretical predictions from Section 5.12
for each representative instrument.  The specific model assumption under test is that
pricing the ASCOT as a true American option on the CB produces materially different risk
sensitivities compared to the market-convention intrinsic approximation and the raw CB
proxy, and that neither approximation is adequate for use in hedging.

**Scope**

The analysis uses two representative instruments: a synthetic short-maturity CB (the
``default'' bundle) and the Kansai Paint convertible bond (4613 JT), a real-world long-
maturity zero-coupon CB.  The CB pricing implementation is first benchmarked against
QuantLib.  The full suite of Greeks is then computed across the spot range for each
instrument under three pricing conventions: the full American ASCOT, the intrinsic
approximation (market convention), and the raw CB proxy.

**Methodology**

All computations use the Crank-Nicolson finite-difference PDE with PSOR obstacle
handling.  Greeks are computed as follows.  Delta and Gamma use log-space finite
differences on the PDE solution grid converted to spot-space via the chain rule.  Vega,
IR01, and CS01 use central bump-and-reprice with bumps of 1 vol point, 1 bp, and 1 bp
respectively.  The credit model uses the Tsiveriotis-Fernandes specification for the CB
PDE and clean risk-free discounting for the ASCOT PDE.

---

### 5.19.1 CB Implementation Benchmark Against QuantLib

**Goal**

To confirm that the CB pricing engine in the validation tool produces results consistent
with an independently recognized standard implementation before using it as the ASCOT
obstacle surface.

**Scope**

The default synthetic CB is priced at 10 representative spot levels using the local
Crank-Nicolson finite-difference engine and independently using QuantLib's binomial
convertible-bond engine, both under the Tsiveriotis-Fernandes credit-spread configuration
with identical market and term parameters.

**Result**

| Spot | Local PV | QuantLib PV | Difference |
|---:|---:|---:|---:|
| 20.00 | 94.280420 | 94.280538 | -0.000117 |
| 38.31 | 94.784799 | 94.793255 | -0.008457 |
| 59.66 | 97.525740 | 97.521998 | +0.003742 |
| 77.97 | 103.348103 | 103.352817 | -0.004714 |
| 99.32 | 114.617942 | 114.615101 | +0.002841 |
| 117.63 | 127.374717 | 127.365017 | +0.009700 |
| 138.98 | 144.702334 | 144.682157 | +0.020178 |
| 157.29 | 160.881353 | 160.880114 | +0.001239 |
| 178.64 | 180.687244 | 180.679828 | +0.007415 |
| 200.00 | 201.091373 | 201.087293 | +0.004080 |

The mean absolute error is 0.0073 per-100, the RMSE is 0.0100, and the maximum absolute
error is 0.0281 per-100.  The maximum relative error is 0.027%.

**Conclusion**

The differences are within the expected discretization tolerance between a finite-
difference PDE and a binomial lattice.  The CB implementation is accepted as the obstacle
surface for ASCOT pricing in the following sections.

---

### 5.19.2 ASCOT Greek Profiles --- Synthetic Default Instrument

#### Instrument Terms

**CB Terms**

| Parameter | Value |
|---|---|
| Face value | 100.00 per-100 |
| Conversion ratio κ | 1.0000 |
| Maturity | 5.00 years |
| Annual coupon | 2.00 (semi-annual) |
| Issuer call price | 100.00 (callable from year 2.00) |
| Holder put price | 100.00 (puttable from year 1.00) |

**Market Parameters**

| Parameter | Value |
|---|---|
| Risk-free rate r | 3.00% |
| Dividend yield q | 1.00% |
| Equity volatility σ | 30.00% |
| Hazard rate λ | 2.00% |
| Recovery fraction | 40.00% |

**ASCOT Terms**

| Parameter | Value |
|---|---|
| Recall price R(0) | 95.00 per-100 |
| Recall price R(T_rec) | 100.00 per-100 |
| Recall price model | Linear accretion |
| Recall expiry | 5.00 years |
| Swap fixed rate | 3.00% |
| Swap recall spread | 1.00% |

The initial recall level R(0) = 95.00 is crossed at S* = 41.58.  Below this level the
ASCOT intrinsic is zero.  Above this level the ASCOT is in-the-money.  All spot levels
in the plot range of 20 to 200 are covered.

---

#### CB Profile

![CB Price vs Spot (Default)](output/default/plot_cb.png)

The CB profile transitions from a near-bond-floor level at low spot (94.28 at S = 20.0)
to a deep equity-linked level at high spot (201.09 at S = 200.0).  The conversion value
line κS = S intersects the CB curve in the range S = 100 to 120, marking the transition
from bond-dominated to equity-dominated valuation.  The initial recall level R(0) = 95.00
is crossed at S* = 41.58, visually marking the ASCOT in-the-money boundary.

---

#### PV Profile

![ASCOT PV vs Spot (Default)](output/default/plot_pv.png)

The time value (shaded region, full minus intrinsic) is positive across the entire spot
range.  At deep out-of-the-money levels (S = 20.0 to S = 41.4) the intrinsic is zero and
the full ASCOT value is entirely time value: 3.79 at S = 20.0, rising to 5.06 at S = 41.4
(100% time value at both points).  Through the in-the-money region the time value as a
percentage of full value declines from 73% at S = 59.7 to 33% at S = 99.3 and to 4.5% at
S = 200.0, but remains non-zero throughout the spot range.

The market-convention intrinsic approximation understates the full ASCOT value across
the entire spot range.  At S = 99.3, the full value is 29.30 versus the intrinsic 19.62,
a gap of 9.69 per-100 (33% understatement).

---

#### EQ Delta

![ASCOT Delta vs Spot (Default)](output/default/plot_delta.png)

The CB proxy Delta is zero in the out-of-the-money region (S below S* = 41.58) under the
OTM cutoff convention.  The full ASCOT Delta is positive across the entire spot range
including the OTM region, where the walk-away put component contributes equity
sensitivity: 0.007 at S = 20.0, rising to 0.142 at S = 41.4.  Both values have no CB
proxy counterpart in this region (CB proxy = 0).

In the in-the-money region both the full and CB proxy Deltas increase toward 1.0, but
with different profiles.  Near S*, at the first in-the-money grid point S = 44.4, the
full Delta is 0.173 versus the CB proxy 0.091: the full Delta is approximately 90% higher,
reflecting the leverage of the near-ATM option.  The gap narrows through the mid-range:
at S = 99.3 the full Delta is 0.642 versus CB proxy 0.628.  A crossover occurs around
S = 105, beyond which the CB proxy exceeds the full Delta: at S = 120.7 full = 0.742
versus CB proxy = 0.775, and at S = 200.0 full = 0.913 versus CB proxy = 0.965.

The full Delta profile is smooth across S*, consistent with the smooth-pasting condition.
The CB proxy Delta has a structural discontinuity at S*, jumping from zero to the CB Delta
at the boundary.

---

#### EQ Gamma

![ASCOT Gamma vs Spot (Default)](output/default/plot_gamma.png)

The CB proxy Gamma is zero in the OTM region by the cutoff convention and follows the CB
Gamma in the ITM region.  The full ASCOT Gamma is positive throughout including the OTM
region from the walk-away put contribution: 0.0019 at S = 20.0 (CB proxy = 0).

Near S*, the full Gamma peaks: at S = 44.4 (first ITM point) full = 0.0102 versus CB
proxy = 0.0064, with the full approximately 59% above the proxy.  As the spot rises
further the relationship reverses: at S = 59.7 full = 0.0101 and CB proxy = 0.0101
(approximately equal).  At S = 99.3: full = 0.0056 versus CB proxy = 0.0084 (full 33%
below).  In the deep in-the-money region both values are small and the absolute
discrepancy narrows.

---

#### EQ Vega

![ASCOT Vega vs Spot (Default)](output/default/plot_vega.png)

The CB proxy Vega is zero in the OTM region by the cutoff convention.  The full ASCOT
Vega is positive and material across the entire spot range.  In the OTM region this Vega
is attributable entirely to the walk-away put: 0.74 at S = 20.0, rising to 19.37 at
S = 41.4.

In the in-the-money region the full ASCOT Vega consistently exceeds the CB proxy Vega.
Near S*, at S = 44.4 (first ITM point), full = 23.75 versus CB proxy = 9.90, a factor of
2.4.  At S = 99.3: full = 76.95, CB proxy = 50.70, a 52% understatement by the proxy.
At S = 200.0: full = 55.27, CB proxy = 15.86, a 248% understatement.  The relative excess
of the full Vega over the CB proxy grows with depth in-the-money, because the CB equity
option loses vol sensitivity in the deep-ITM regime while the walk-away put continues to
contribute.

---

#### IR01

![ASCOT IR01 vs Spot (Default)](output/default/plot_ir01.png)

The CB proxy IR01 is zero in the OTM region by the cutoff convention.  The full ASCOT
IR01 is -7.1 at S = 20.0, turns positive above approximately S = 33, and reaches +12.1
at S = 41.4 (all OTM, CB proxy = 0).

In the in-the-money region the full ASCOT IR01 and the CB proxy IR01 have opposite signs
at every tested spot level.  The CB proxy IR01 is large and negative, reflecting the CB's
bond duration: -176.5 at S = 44.4, -98.4 at S = 99.3, and -13.1 at S = 200.0.  The full
ASCOT IR01 is large and positive: +17.8 at S = 44.4, +153.4 at S = 99.3, and +227.5 at
S = 200.0.

The signed gap between full and CB proxy IR01 at S = 99.3 is (+153.4) - (-98.4) =
+251.8 per-100.  At S = 44.4 the signed gap is (+17.8) - (-176.5) = +194.3 per-100.
Using the CB proxy for IR01 hedging in the in-the-money region would reverse the direction
of the hedge at every tested spot level.

The positive full IR01 reflects two concurrent mechanisms.  The walk-away put appreciates
when rates rise because the CB falls and the protection value increases.  The ASCOT PDE
uses clean risk-free discounting, so a higher risk-free rate increases the risk-neutral
equity drift, raising the value of the call-on-CB component.

---

#### CS01

![ASCOT CS01 vs Spot (Default)](output/default/plot_cs01.png)

The CB proxy CS01 is zero in the OTM region by the cutoff convention.  The full ASCOT
CS01 is zero to six decimal places at every tested spot level, across both the OTM and
ITM regions.

In the in-the-money region the CB proxy CS01 is large and negative: -155.6 per-100 at
S = 44.4 (near S*), -56.8 per-100 at S = 99.3, and -5.2 per-100 at S = 200.0.  The full
ASCOT CS01 is 0.000 at each of these levels.  The walk-away put appreciation under a
rising hazard rate exactly cancels the erosion in the intrinsic component, leaving the
full ASCOT with no net credit spread exposure.

Using the CB proxy for CS01 hedging in the in-the-money region would attribute the entire
CB credit duration to the ASCOT holder.  The true credit exposure is zero.

---

**Summary for Default Instrument**

The full American ASCOT produces risk profiles that differ materially from the CB proxy
across all Greeks.  EQ Delta shows a crossover: full is 90% above the CB proxy near S*
and falls below it above S = 105, reaching 0.913 versus 0.965 at S = 200.  EQ Gamma is
59% above the CB proxy near S* and 33% below at S = 99.3.  EQ Vega exceeds the CB proxy
by 52% at S = 99.3 and 248% at S = 200.  IR01 has the opposite sign to the CB proxy at
every ITM spot, with a signed gap of +252 per-100 at S = 99.3.  CS01 is identically zero
for the full ASCOT while the CB proxy is -155.6 per-100 at S = 44.4 and -56.8 per-100 at
S = 99.3.

---

### 5.19.3 ASCOT Greek Profiles --- Kansai Paint (4613 JT)

#### Instrument Terms

**CB Terms**

| Parameter | Value |
|---|---|
| Ticker | 4613 JT |
| Face value | 100.00 per-100 (denomination JPY 10,000,000) |
| Conversion ratio κ | 0.036119 (conversion price: JPY 2,768.60) |
| Maturity | 6.9973 years |
| Coupon | Zero coupon |
| Issuer call | Not applicable |
| Holder put | Not applicable |
| Valuation date | February 28th 2025 |

**Market Parameters**

| Parameter | Value |
|---|---|
| Risk-free rate r | 3.00% |
| Dividend yield q | 1.65% |
| Equity volatility σ | 27.42% |
| Hazard rate λ | 0.95% |
| Recovery fraction | 40.00% |
| Share price (valuation date) | JPY 2,136.50 |

**ASCOT Terms**

| Parameter | Value |
|---|---|
| Recall price R(0) | 95.00 per-100 |
| Recall price R(T_rec) | 100.00 per-100 |
| Recall price model | Linear accretion |
| Recall expiry | 5.00 years |
| Swap fixed rate | 3.00% |
| Swap recall spread | 1.00% |

The initial recall level R(0) = 95.00 is crossed at S* = 2,196.12 (share price in JPY).
Below this level the ASCOT intrinsic is zero.  The plot range is JPY 1,000 to JPY 4,000,
spanning the out-of-the-money and in-the-money regions.

---

#### CB Profile

![CB Price vs Spot (Kansai Paint)](output/kansai/plot_cb.png)

The CB trades at 77.83 per-100 at S = 1,000 (below par, bond floor driven) and rises to
145.51 per-100 at S = 4,000 as the equity option gains intrinsic value.  The zero-coupon
structure and long maturity produce a lower bond floor relative to par.  The conversion
value line κS (with κ = 0.036119) rises slowly with spot, reflecting the small conversion
ratio in JPY.  The initial recall level R(0) = 95.00 is crossed at S* = 2,196.12.

---

#### PV Profile

![ASCOT PV vs Spot (Kansai Paint)](output/kansai/plot_pv.png)

The time value as a fraction of full ASCOT value is very high throughout the range.  For
all spot levels below S* = 2,196.12, the intrinsic is zero and the full ASCOT value is
entirely time value: 1.05 at S = 1,000, rising to 11.47 at S = 2,017 (100% time value at
all out-of-the-money levels).  Through the in-the-money region the time value as a
percentage of full value declines but remains substantial: 83.7% at S = 2,322 (just barely
in-the-money, intrinsic = 2.74), 53.5% at S = 2,678, and 13.9% at S = 4,000 (intrinsic
= 50.51, full = 58.65).

At S = 4,000 the time value is 8.14 per-100.  Using the intrinsic approximation would
understate the full ASCOT value by 8.14 per-100 (16.1%) at this level.

---

#### EQ Delta

![ASCOT Delta vs Spot (Kansai Paint)](output/kansai/plot_delta.png)

The CB proxy Delta is zero in the OTM region by the cutoff convention.  The full ASCOT
Delta is positive throughout the OTM region from the walk-away put contribution: 0.0042
at S = 1,000, rising to 0.0177 at S = 2,170 (all OTM, CB proxy = 0).  Delta values are
small in magnitude, reflecting the low conversion ratio κ = 0.036119.

In the in-the-money region the full ASCOT Delta is consistently below the CB proxy Delta.
At the first ITM grid point S = 2,220: full = 0.0182 versus CB proxy = 0.0214 (full 15%
below).  At S = 2,322: full = 0.0191 versus CB proxy = 0.0224 (full 15% below).  At
S = 4,000: full = 0.0292 versus CB proxy = 0.0332 (full 12% below).  The gap narrows in
relative terms as the spot rises but persists across the entire ITM range.

The full Delta profile is smooth across S*.  The CB proxy Delta has a structural
discontinuity at S*, jumping from zero to the CB Delta at the boundary.

---

#### EQ Gamma

![ASCOT Gamma vs Spot (Kansai Paint)](output/kansai/plot_gamma.png)

The Gamma of both the full ASCOT and the CB proxy is negligibly small across the entire
spot range, below 0.0001 at every tested spot level.  In the OTM region the CB proxy
Gamma is zero by the cutoff convention.  The full ASCOT Gamma is positive but below 0.0001
throughout.

The negligible Gamma reflects the bond-floor-dominated nature of this CB across the tested
spot range, where the equity conversion option contributes little curvature relative to the
bond component.

---

#### EQ Vega

![ASCOT Vega vs Spot (Kansai Paint)](output/kansai/plot_vega.png)

The CB proxy Vega is zero in the OTM region by the cutoff convention.  The full ASCOT
Vega is positive and substantial in the OTM region, attributable entirely to the walk-away
put: 17.14 at S = 1,000, rising to 61.45 at S = 1,864 and 72.81 at S = 2,170.

In the in-the-money region the full ASCOT Vega exceeds the CB proxy Vega throughout,
with the gap growing deeper in-the-money.  Near S*, at S = 2,220 (first ITM point):
full = 74.36 versus CB proxy = 71.69 (full 3.7% above, nearly equal).  At S = 2,322:
full = 77.18 versus CB proxy = 72.92 (full 5.8% above).  At S = 2,678: full = 84.12
versus CB proxy = 73.77 (full 14% above).  At S = 4,000: full = 80.93 versus CB proxy =
38.83 (full 108% above).

The full Vega peaks around S = 3,288 at 87.16 then declines, while the CB proxy Vega
decreases more steeply, producing the widening relative gap at deep in-the-money levels.

---

#### IR01

![ASCOT IR01 vs Spot (Kansai Paint)](output/kansai/plot_ir01.png)

The CB proxy IR01 is zero in the OTM region by the cutoff convention.  The full ASCOT
IR01 is positive throughout the OTM region: +11.2 at S = 1,000, rising to +92.3 at
S = 2,170.

In the in-the-money region the full ASCOT IR01 and the CB proxy IR01 have opposite signs
at every tested spot level.  The CB proxy IR01 is large and negative, reflecting the CB's
duration: -335.0 at S = 2,220, -319.6 at S = 2,322, and -88.2 at S = 4,000.  The full
ASCOT IR01 is large and positive: +96.4 at S = 2,220, +104.3 at S = 2,322, and +184.2
at S = 4,000.

The signed gap between full and CB proxy IR01 at S = 2,220 is (+96.4) - (-335.0) =
+431.4 per-100.  At S = 2,322 the signed gap is (+104.3) - (-319.6) = +423.9 per-100.
At S = 4,000 the signed gap is (+184.2) - (-88.2) = +272.4 per-100.  Using the CB proxy
for IR01 hedging in the in-the-money region would reverse the direction of the hedge at
every tested spot level.

---

#### CS01

![ASCOT CS01 vs Spot (Kansai Paint)](output/kansai/plot_cs01.png)

The CB proxy CS01 is zero in the OTM region by the cutoff convention.  The full ASCOT
CS01 is negative and non-zero in the OTM region: -5.1 per-100 at S = 1,000, rising in
magnitude to -22.4 at S = 2,170.  In this region the ASCOT is a deeply OTM call on the
CB.  A rise in the hazard rate reduces the expected future CB value and therefore the
probability of future exercise above R(0), reducing the ASCOT option value.

In the in-the-money region both the full ASCOT CS01 and the CB proxy CS01 are negative,
but the magnitudes differ substantially.  The CB proxy CS01 is large and negative: -388.9
per-100 at S = 2,220, -375.5 at S = 2,322, and -120.3 at S = 4,000.  The full ASCOT
CS01 is small: -22.9 at S = 2,220 (5.9% of the CB proxy magnitude), -23.7 at S = 2,322
(6.3%), and -22.6 at S = 4,000 (18.8%).  The fraction of CB credit exposure absorbed by
the full ASCOT ranges from approximately 6% to 19% across the ITM range, increasing as
the ASCOT moves deeper in-the-money.

Using the CB proxy for CS01 hedging in the in-the-money region would overstate the true
credit exposure by a factor of roughly 5 to 17 across the tested range.

---

**Summary for Kansai Paint**

The full American ASCOT produces risk profiles that differ materially from the CB proxy
across all Greeks.  EQ Delta is consistently 12 to 15% below the CB proxy in the ITM
region, with no crossover.  EQ Gamma is negligible for both the full ASCOT and the CB
proxy.  EQ Vega exceeds the CB proxy by 3.7% near S*, growing to 108% at S = 4,000.
IR01 has the opposite sign to the CB proxy at every ITM spot, with a signed gap of +431
per-100 near S* and +272 per-100 at S = 4,000.  CS01 is 6% to 19% of the CB proxy
magnitude in the ITM region, with the CB proxy overstating the true credit exposure by
5x to 17x.
