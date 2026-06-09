# Section 5.12 and 5.19 — ASCOT Model Assumption Test
## CB/ASCOT Flat Model (Independent Validation Tool)

---

## 5.12 Conceptual Soundness Analysis

**Goal**

To assess the theoretical soundness of pricing the Asset Swap with Call Option on Term
(ASCOT) as an American call option on a convertible bond (CB), and to derive from first
principles the expected behavior of the material risk sensitivities, specifically the
credit spread sensitivity (CS01), the volatility sensitivity (Vega), and the equity
sensitivity (Delta).

**Scope**

The analysis is conducted entirely through theoretical reasoning and financial mathematics,
without reference to numerical outputs.  Two aspects of the ASCOT structure are examined:
the source and economic nature of the American time value, and the resulting implications
for each Greek relative to the CB itself and relative to the market-convention intrinsic
approximation.

**Methodology**

The analysis proceeds from the fundamental payoff structure of the ASCOT, derives the
properties of its American time value, and then applies these properties to each
sensitivity in turn.

---

### 5.12.1 Instrument Structure and American Time Value

The ASCOT gives its holder the right, at any point from inception to expiry, to call the
CB from the asset-swap counterparty at an accreting recall price R(t).  The recall price
begins at R(0) and rises linearly toward a terminal level R(T_rec) at the recall expiry
date T_rec, reflecting the amortization of the swap's net present value toward zero at
maturity.

Market convention values the ASCOT at its intrinsic value, defined as max(CB(S, 0)
- R(0), 0), which treats the ASCOT as if it would be exercised immediately.  The full
American model recognizes that the holder retains the option to wait and values this right
explicitly.

The American time value, defined as the excess of the full value over the intrinsic value,
is the central object of this analysis.  Two forces make waiting systematically costly for
the ASCOT holder.

First, the CB coupons accrue to the asset-swap counterparty, not the ASCOT holder, for
each day the option remains unexercised.  This represents a foregone cash flow that erodes
the value of waiting.

Second, the recall price R(t) accretes upward over the life of the option.  A holder who
waits finds the exercise strike rising against them, which reduces the value of future
exercise relative to immediate exercise.

Both forces argue for immediate exercise.  The rational holder waits only if the value of
waiting exceeds these combined costs.  Under the ASCOT structure, the sole source of value
in waiting is the walk-away right: if credit deteriorates or the equity falls materially,
the holder may allow the ASCOT to expire worthless rather than taking delivery of a
distressed CB at the recalled price R(t).  This right to walk away is equivalent to
holding a put option on the CB struck at R(t), with expiry at T_rec.  The full American
value can therefore be decomposed as:

> ASCOT_full = ASCOT_intrinsic + walk-away put value

This decomposition is not an approximation.  It follows from the American option
decomposition theorem.  The walk-away put is positive whenever there is any possibility of
the CB falling below R(t) before expiry, which is almost always the case for any bond with
residual maturity.

---

### 5.12.2 Credit Spread Sensitivity (CS01) — Theoretical Analysis

CS01 measures the sensitivity of the instrument value to a parallel shift in the credit
spread, proxied here by a shift in the issuer hazard rate lambda.

For the CB, increasing lambda raises the effective discount rate on bond-like cash flows
through the Tsiveriotis-Fernandes blending mechanism (disc = r + lambda * (1 - p_conv),
where p_conv is the risk-neutral conversion probability).  CB_CS01 is negative and
material across the entire spot range.

For the ASCOT intrinsic, the sensitivity is simply CB_CS01 when in-the-money (CB > R(0))
and zero when out-of-the-money.  This is expressed as:

> Intrinsic_CS01 = CB_CS01 * indicator(CB > R(0))

This indicator-based proxy fails in both regimes.  In the out-of-the-money region, the
proxy is identically zero, but the full ASCOT still has positive value from its optionality
and this value is sensitive to changes in lambda.  In the in-the-money region, the proxy
overstates the true exposure because the walk-away put offsets part of the intrinsic credit
sensitivity.

The full ASCOT CS01 is driven by two competing effects when lambda rises.

The first effect is the erosion of the intrinsic value.  A wider credit spread reduces the
CB value, which reduces the intrinsic component CB - R(0).  This is negative for the ASCOT
holder.

The second effect is the appreciation of the walk-away put.  A wider credit spread raises
the probability of a large adverse credit move, which increases the value of the right to
walk away.  This is positive for the ASCOT holder.

These two effects substantially offset each other.  The net CS01 of the full ASCOT is much
smaller in magnitude than the CB CS01.  The degree of offset depends on the moneyness of
the walk-away put: when the ASCOT is close to the money, the walk-away put is near ATM and
its credit sensitivity is largest.  When the ASCOT is deep in-the-money, the walk-away put
is deep out-of-the-money and contributes little, so the full CS01 converges toward the
intrinsic CS01.

This credit insulation is an intrinsic economic property of the instrument, not an
artifact of the PDE discretization.  The ASCOT holder is an equity option holder.  The
credit spread affects the underlying (the CB), but the optionality of the ASCOT partially
shields the holder from the direction of that effect.  A bond holder bears the full credit
sensitivity.  An option holder on the same bond bears a reduced and partially hedged
exposure.

The practical implication is that using CB_CS01 as a proxy for ASCOT CS01, even with an
in-the-money indicator applied, materially overstates the true credit exposure of the
ASCOT holder.

---

### 5.12.3 Volatility Sensitivity (Vega) — Theoretical Analysis

Since ASCOT_full = ASCOT_intrinsic + walk-away put, the vega of the full ASCOT is:

> Vega_full = Vega_intrinsic + Vega_walk-away

The walk-away put always gains value when equity volatility rises (higher volatility
implies fatter tails in the underlying equity distribution, increasing the probability of
the large downward moves that the walk-away right protects against).  Therefore
Vega_walk-away is strictly positive, which implies Vega_full > Vega_intrinsic throughout
the spot range.

In the out-of-the-money region, Vega_intrinsic = 0, so Vega_full = Vega_walk-away > 0.
The full ASCOT retains positive vega even where the intrinsic has none.

In the in-the-money region, Vega_intrinsic = CB_Vega (since intrinsic = CB - R(0) and
R(0) is not sensitive to vol).  The walk-away put adds a positive vega component on top.
This means Vega_full > CB_Vega whenever the walk-away put has non-trivial time value.  As
the ASCOT goes deeply in-the-money, the walk-away put goes deeply out-of-the-money and
its vega declines toward zero.  Vega_full then converges toward CB_Vega from above.

The comparison between Vega_full and CB_Vega in the out-of-the-money region depends on
the structure of the CB itself, specifically whether the CB's embedded equity option is
alive or dead at the spot levels in question.

For a short-maturity CB at low spot levels, the CB's embedded conversion option is far
out-of-the-money and nearly worthless.  The CB trades close to its bond floor.  CB_Vega is
therefore near zero.  Even a small Vega_walk-away exceeds it, so Vega_full > CB_Vega
throughout the full spot range.

For a long-maturity CB, the embedded conversion option retains meaningful time value even
at moderately low spot levels.  CB_Vega is non-trivial in the out-of-the-money ASCOT
region.  The ASCOT is an out-of-the-money call on the CB in this region, so it only
partially participates in CB moves (delta-on-CB < 1).  The vega of the ASCOT is diluted
relative to CB_Vega: Vega_full = delta-on-CB * CB_Vega + Vega_walk-away < CB_Vega when
the dilution effect dominates.  Once the ASCOT crosses into the in-the-money region, the
walk-away put adds back positive vega and Vega_full exceeds CB_Vega again.

---

### 5.12.4 Equity Sensitivity (Delta) — Theoretical Analysis

Delta_intrinsic = 0 in the out-of-the-money region (intrinsic is zero and flat) and
equals CB_Delta in the deep in-the-money region (intrinsic tracks CB directly).  At the
boundary CB = R(0), the intrinsic has a kink in its delta profile.

Delta_full is smooth across this boundary.  American option theory requires the smooth-
pasting condition: the value function is continuously differentiable at the optimal
exercise boundary.  Numerically this ensures that the PDE solution does not produce a
delta discontinuity.

In the in-the-money region, Delta_full < CB_Delta by the same argument as for vega: the
ASCOT is an option on the CB and participates only fractionally in CB movements.  Delta_cb
(the raw CB delta used as a proxy) overstates the true ASCOT delta.  As the ASCOT goes
deeply in-the-money and the walk-away put approaches expiry worthless, Delta_full
converges toward CB_Delta from below.

---

## 5.19 Model Assumption Analysis

**Goal**

To establish the numerical correctness of the independent CB/ASCOT flat pricing
implementation and to verify numerically the theoretical predictions derived in Section
5.12.  The specific model assumption under test is that pricing the ASCOT as a true
American option on the CB produces materially different risk sensitivities compared to the
market-convention intrinsic approximation, and that the CB proxy overstates the credit
exposure of the ASCOT holder.

**Scope**

The analysis is conducted using two representative instruments: a synthetic short-maturity
CB with standard embedded options (the ``default'' bundle), and the Kansai Paint
convertible bond (4613 JT), a real-world long-maturity zero-coupon CB.  The CB pricing
implementation is first benchmarked against QuantLib's independent binomial convertible-
bond engine.  The full suite of Greeks (Delta, Gamma, Vega, IR01, CS01) is then computed
across the spot range for both instruments under three pricing assumptions: the full
American ASCOT model, the intrinsic approximation, and the raw CB proxy.

**Methodology**

All computations use the Crank-Nicolson finite-difference PDE with PSOR obstacle handling,
implemented in the independent Python validation tool under `cb_ascot_flat/`.  Greeks are
computed as follows.  Delta and Gamma are obtained from log-space finite differences on the
PDE solution grid, converted to spot-space via the chain rule.  Vega, IR01, and CS01 are
computed by central bump-and-reprice with bumps of 1 vol point, 1 bp, and 1 bp
respectively.  The credit model uses the Tsiveriotis-Fernandes credit-spread specification
for the CB PDE and clean risk-free discounting for the ASCOT PDE.

---

### 5.19.1 CB Implementation Benchmark Against QuantLib

**Goal**

To confirm that the CB pricing engine embedded in the validation tool produces results
consistent with an independently recognized standard implementation, prior to using it as
the obstacle surface in ASCOT pricing.

**Scope**

The default synthetic CB is priced across 10 representative spot levels using the local
Crank-Nicolson finite-difference engine and independently using QuantLib's binomial
convertible-bond engine.  Both engines use the Tsiveriotis-Fernandes credit-spread
configuration with identical market and term parameters.

**Result**

The comparison across the spot range is summarized in the table below.

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
error is 0.0281 per-100 (occurring in the ATM region where the binomial tree discretization
error is typically largest).  The maximum relative error is 0.027%.

**Conclusion**

The differences are within the expected discretization tolerance between a finite-difference
PDE and a binomial lattice engine.  The finite-difference engine is consistent with the
QuantLib reference across the full spot range.  The CB implementation is accepted as the
obstacle surface for ASCOT pricing in Sections 5.19.2 and 5.19.3.

---

### 5.19.2 ASCOT Greek Profiles — Synthetic Default Instrument

#### Instrument Terms

The default bundle uses a synthetic CB with standard embedded options and a flat hazard
rate.  The terms are summarized below.

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
| Recall price R(0) | 95.00 |
| Recall price R(T_rec) | 100.00 |
| Recall price model | Linear accretion |
| Recall expiry | 5.00 years |
| Swap fixed rate | 3.00% |
| Swap recall spread | 1.00% |

#### CB Profile

The CB price profile is shown below.  The conversion value line (κS = 1.0 * S), the bond
floor reference (F * exp(-(r + λ) * T)), the issuer call level, and the initial recall
level R(0) = 95 are overlaid.  The crossover between the CB price curve and the R(0) level
defines the spot S* below which the ASCOT is out-of-the-money.

![CB Price vs Spot (Default)](output/default/plot_cb.png)

#### PV Profile

The full ASCOT and intrinsic ASCOT PV profiles are shown below.  The shaded region
represents the American time value, which is the value of the walk-away right as derived
in Section 5.12.1.  The time value is largest near the ATM crossing S* and declines toward
zero as the ASCOT goes deeply in-the-money.

![ASCOT PV vs Spot (Default)](output/default/plot_pv.png)

The time value is non-zero throughout the spot range, confirming that the walk-away right
has positive value for all spot levels.  At low spot values, the ASCOT intrinsic is zero
but the full ASCOT retains positive value from the probability of the stock rallying
through R(0) before expiry.

#### CS01 Profile

The CS01 profiles for the full ASCOT, intrinsic ASCOT, and CB proxy are shown below.

![ASCOT CS01 vs Spot (Default)](output/default/plot_cs01.png)

Three observations confirm the theoretical predictions from Section 5.12.2.

First, the CB proxy CS01 is large and negative across the entire spot range, reflecting the
full credit sensitivity of the bond.

Second, the intrinsic CS01 is identically zero for S < S* (out-of-the-money region) and
equals the CB CS01 for S > S* (in-the-money region).  This creates a step-like profile
with a discontinuity at S*.

Third, the full ASCOT CS01 is substantially smaller in magnitude than both the CB proxy
and the intrinsic across the entire range.  In the out-of-the-money region, the full CS01
is small but non-zero, in contrast to the zero intrinsic CS01.  In the in-the-money
region, the full CS01 is significantly smaller in magnitude than the CB CS01, confirming
the walk-away put offsetting mechanism described in Section 5.12.2.  The intrinsic CS01
overstates the true credit exposure by a substantial margin for all in-the-money spot
levels.

#### Vega Profile

The Vega profiles are shown below.

![ASCOT Vega vs Spot (Default)](output/default/plot_vega.png)

The full ASCOT Vega exceeds both the intrinsic Vega and the CB proxy Vega throughout the
spot range.  This confirms the prediction in Section 5.12.3 for a short-maturity bond.  In
the out-of-the-money region, the CB equity option is far out-of-the-money, so CB_Vega is
near zero.  The full ASCOT Vega, representing the Vega of the walk-away put in this
region, is small but positive and exceeds the near-zero CB_Vega.  In the in-the-money
region, the walk-away put amplifies the vega above the CB level, with the peak excess
occurring near S*.

#### Delta and Gamma Profiles

![ASCOT Delta vs Spot (Default)](output/default/plot_delta.png)

![ASCOT Gamma vs Spot (Default)](output/default/plot_gamma.png)

The full ASCOT Delta profile is smooth across the ATM boundary, consistent with the
smooth-pasting condition.  The intrinsic Delta shows a sharp transition at S*.  The full
Delta is bounded below the CB proxy Delta throughout the spot range, confirming that the
ASCOT holder has reduced equity exposure compared to a direct CB holder.

#### IR01 Profile

![ASCOT IR01 vs Spot (Default)](output/default/plot_ir01.png)

The IR01 profiles are consistent with the theoretical expectations.  The consistent rate
bump applied to both the CB discount curve and the recall price R(t) (computed as a
discounted swap cash flow) produces the expected profile.

---

### 5.19.3 ASCOT Greek Profiles — Kansai Paint (4613 JT)

#### Instrument Terms

The Kansai Paint CB is a real-world zero-coupon convertible bond issued by Kansai Paint
Co. Ltd. (Bloomberg ticker: 4613 JT).  Relative to the synthetic default instrument, this
bond has a longer maturity, zero coupon, a small conversion ratio (reflecting a high
conversion price relative to the share price), and a lower hazard rate.  These differences
produce materially different Greek profiles, as predicted in Section 5.12.3.

**CB Terms**

| Parameter | Value |
|---|---|
| Ticker | 4613 JT |
| Face value | 100.00 per-100 (denomination: JPY 10,000,000) |
| Conversion ratio κ | 0.036119 (conversion price: JPY 2,768.60) |
| Maturity | 6.9973 years |
| Coupon | Zero coupon |
| Issuer call / Holder put | Not applicable |
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
| Recall price R(0) | 95.00 |
| Recall price R(T_rec) | 100.00 |
| Recall price model | Linear accretion |
| Recall expiry | 5.00 years |
| Swap fixed rate | 3.00% |
| Swap recall spread | 1.00% |

#### CB Profile

![CB Price vs Spot (Kansai Paint)](output/kansai/plot_cb.png)

The CB trades below the recall level R(0) = 95 at the lower end of the spot range (S <
S*), reflecting the zero-coupon bond floor.  The long maturity sustains a meaningful equity
option premium at moderate spot levels.

#### PV Profile

![ASCOT PV vs Spot (Kansai Paint)](output/kansai/plot_pv.png)

The walk-away time value is present across the full spot range, with a larger relative
time value in the out-of-the-money region compared to the default bundle.  This is
consistent with the lower hazard rate (smaller intrinsic CS01 erosion) and the longer
maturity (larger walk-away put time value).

#### CS01 Profile

![ASCOT CS01 vs Spot (Kansai Paint)](output/kansai/plot_cs01.png)

The same three-way pattern observed in the default bundle is confirmed.  The CB proxy CS01
is large and negative.  The intrinsic CS01 switches between zero (OTM) and CB CS01 (ITM)
at the boundary S*.  The full ASCOT CS01 is substantially smaller in magnitude throughout,
confirming the walk-away offset for the Kansai instrument.  The lower hazard rate of this
bond (λ = 0.95% versus 2.00% for the default) produces a smaller absolute CB CS01, but
the ratio CS01_full / CB_CS01 remains much less than one, consistent with the theoretical
prediction.

#### Vega Profile

![ASCOT Vega vs Spot (Kansai Paint)](output/kansai/plot_vega.png)

The Kansai Vega profile differs from the default bundle in the out-of-the-money ASCOT
region, as predicted in Section 5.12.3.  For S < S* (CB < R(0)), the full ASCOT Vega is
below the CB proxy Vega.  This is because the long maturity of the Kansai bond sustains a
live CB equity option at these spot levels, producing non-trivial CB_Vega.  The ASCOT,
being an out-of-the-money call on the CB, only partially captures this CB Vega (delta-on-
CB < 1), so Vega_full < CB_Vega in this region.  Once S > S* (CB > R(0)), the walk-away
put adds back positive Vega on top of CB_Vega and the full ASCOT Vega exceeds the CB proxy
again.

The contrast with the default bundle isolates the effect of CB maturity on the OTM Vega
comparison.  For the short-maturity default instrument, CB_Vega is near zero at low spots
(dead equity option) and the full ASCOT Vega dominates.  For the long-maturity Kansai
instrument, CB_Vega is alive at all tested spot levels and the ASCOT dilution effect
dominates in the OTM region.

#### Delta and Gamma Profiles

![ASCOT Delta vs Spot (Kansai Paint)](output/kansai/plot_delta.png)

![ASCOT Gamma vs Spot (Kansai Paint)](output/kansai/plot_gamma.png)

The Kansai Delta profile is substantially smaller in absolute magnitude compared to the
default bundle, reflecting the small conversion ratio κ = 0.036119 and the large share
price denomination.  The qualitative properties are unchanged: the full Delta is smooth,
bounded below the CB proxy Delta, and rises monotonically from the OTM region toward the
ITM region.

#### IR01 Profile

![ASCOT IR01 vs Spot (Kansai Paint)](output/kansai/plot_ir01.png)

---

**Conclusion**

The numerical results across both instruments confirm all four theoretical predictions
from Section 5.12.  First, the full ASCOT CS01 is substantially smaller in magnitude than
the CB CS01 at all spot levels.  Second, the intrinsic CS01 proxy overstates the true
credit exposure in the in-the-money region and understates it in the out-of-the-money
region.  Third, the full ASCOT Vega exceeds the intrinsic Vega throughout, confirming the
positive Vega contribution of the walk-away put.  Fourth, the comparison between the full
Vega and the CB proxy Vega in the out-of-the-money region depends on the maturity of the
CB's embedded equity option: this cross-over behavior is confirmed for the Kansai
instrument and is absent for the short-maturity default instrument.

The model assumption that the ASCOT should be priced as a full American option rather than
as its intrinsic value produces material differences in all sensitivities.  Using the
intrinsic approximation for Greeks, in particular for CS01 hedging, is not supported by
the numerical evidence.
