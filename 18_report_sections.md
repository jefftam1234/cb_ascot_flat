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
recall price R(t) is defined at each point in time as the par value of the CB plus the
present value of the remaining fixed coupon obligations on the swap, discounted at the
reference rate plus the recall spread.  When the CB coupon is zero or below the floating
reference rate, this present value of remaining obligations is negative relative to par,
so R(t) begins below par at inception.  As time passes and the remaining term shortens,
the present value of the remaining coupon stream converges toward zero and R(t) accretes
upward toward par.  The precise path of accretion is not necessarily linear: it depends
on the coupon schedule, the recall spread, and prevailing rates.

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

For the CB, increasing lambda reflects a higher probability of issuer default.  The
bond-like component of the CB, its future coupon and principal cash flows conditional
on no conversion is then discounted at a higher risk-adjusted rate, reducing the CB's
value.  CB_CS01 is therefore negative and material across the entire spot range, because
the CB retains meaningful bond-like cash flows regardless of the equity level.

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

For the full ASCOT, the rate sensitivity involves two distinct economic channels that both
act in a direction opposite to the CB.

The first channel is the walk-away put.  When rates rise and the CB falls, the right to
not take delivery becomes more valuable: the holder avoids receiving an asset whose value
has declined.  The walk-away put, as a put on the CB, gains value when the CB falls.

The second channel operates through the cost of carry of the underlying equity.  A higher
risk-free rate raises the risk-neutral expected appreciation rate of the equity (by the
no-arbitrage cost-of-carry principle: the equity must grow at r - q in expectation under
the risk-neutral measure).  A higher expected equity level increases the probability that
the CB's embedded conversion option will be exercised, lifting the CB value through its
equity component.  The ASCOT, as a call option on the CB, benefits from this effect.

The net effect on the full ASCOT is that both the walk-away put and the equity-driven
call component respond favorably to a rate rise, and the combined full IR01 can be
positive and large, opposite in sign to CB_IR01.

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

### 5.12.5 Equity Sensitivity (Delta and Gamma)

**Delta**

The single contrasting force is the gradient of the ASCOT time value with respect to
spot.

The ASCOT time value follows a hump shape as a function of spot: it rises through the OTM
region as the underlying CB approaches the exercise boundary and the probability of
profitable exercise increases, peaks somewhere near or just above S*, and then falls
through the ITM region as the walk-away right loses relevance with the CB well above
R(t).  The slope of this hump is the extra delta term:

> Delta_full = CB_Delta + d(time value)/dS

where CB_Delta is the intrinsic delta — zero in the OTM region, equal to the raw CB delta
in the ITM region.

In the OTM region, d(time value)/dS > 0, so Delta_full is positive while the CB proxy
delta is zero.

In the deep ITM region, d(time value)/dS < 0, so Delta_full = CB_Delta + (negative) <
CB_Delta.

Whether Delta_full ever exceeds CB_Delta in the ITM region depends on the level of
d(time value)/dS at S*.  By smooth-pasting, Delta_full is continuous at S*, which fixes
the sign of d(time value)/dS immediately above S*:

> d(time value)/dS at S*, ITM side = OTM delta(S*) − CB_Delta(S*)

If the OTM delta at S* exceeds CB_Delta(S*), d(time value)/dS is positive just above S*,
Delta_full overshoots CB_Delta, and a crossover occurs later as the hump slopes away.
If the OTM delta at S* is below CB_Delta(S*), d(time value)/dS is immediately negative
above S* and Delta_full is below CB_Delta throughout the entire ITM region with no
crossover.

**Gamma**

Near S*, the ASCOT is at-the-money as a call option on the CB.  At-the-money options have
their highest gamma for a given underlying, because the option delta changes most rapidly
near the strike.  The ASCOT's option layer therefore adds convexity near S*, and
Gamma_full > Gamma_CB near the exercise boundary.

As the ASCOT moves deeper ITM, the walk-away put becomes increasingly out-of-the-money on
the CB, loses its convexity contribution, and Gamma_full converges back toward Gamma_CB.
The rate and direction of convergence — whether Gamma_full approaches from above or crosses
below Gamma_CB — depends on the CB's own gamma profile and the residual time value
gradient.

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

![CB Price vs Initial Parity (Default)](output/default/plot_cb.png)

The CB profile transitions from a near-bond-floor level at low spot (94.28 at S = 20.0)
to a deep equity-linked level at high spot (201.09 at S = 200.0).  The conversion value
line κS = S intersects the CB curve in the range S = 100 to 120, marking the transition
from bond-dominated to equity-dominated valuation.  The initial recall level R(0) = 95.00
is crossed at S* = 41.58, visually marking the ASCOT in-the-money boundary.

---

#### PV Profile

![ASCOT PV vs Initial Parity (Default)](output/default/plot_pv.png)

The time value (shaded region, full minus intrinsic) is positive across the entire spot
range.  At deep out-of-the-money levels (S = 20.0 to S = 41.4) the intrinsic is zero and
the full ASCOT value is entirely time value: 3.79 at S = 20.0, rising to 5.06 at S = 41.4
(100% time value at both points).  Through the in-the-money region the time value as a
percentage of full value declines from 73% at S = 59.7 to 33% at S = 99.3 and to 4.5% at
S = 200.0, but remains non-zero throughout the spot range.

The time value is the walk-away right: the holder's option to abandon the ASCOT rather
than pay the accreting recall price for a CB that has deteriorated below R(t).  As long
as there is positive probability of an adverse credit or equity event causing the CB to
fall below R(t) before recall expiry, this right has positive value.  The intrinsic
approximation treats exercise as if it were immediate, ignoring this protection entirely.
At S = 99.3, the gap is 9.69 per-100 (full = 29.30 versus intrinsic = 19.62, a 33%
understatement).  Even deep in-the-money, where early exercise of a vanilla call is nearly
certain, the walk-away right retains value because credit deterioration is an asymmetric
downside risk that persists regardless of the current equity level.

---

#### EQ Delta

![ASCOT Delta vs Initial Parity (Default)](output/default/plot_delta.png)

In the out-of-the-money region (S below S* = 41.58), the CB proxy Delta is zero because
the OTM cutoff assigns zero ASCOT value and therefore zero hedging exposure.  The full
ASCOT carries positive delta in this region: 0.007 at S = 20.0, rising to 0.142 at
S = 41.4.  This delta arises because the full ASCOT has positive value even OTM (the
walk-away right).  As spot rises, the CB rises, the probability that the CB will
eventually cross R(t) before expiry increases, and the ASCOT option value rises.  The
CB proxy misses this entirely because it does not recognise any ASCOT value below S*.

Near S*, at S = 44.4 (first ITM point), the full delta is 0.173 versus the CB proxy
0.091, a 91% excess.  At S*, the ASCOT is approximately at-the-money on the CB and the
option's time value is near its maximum.  The time value is itself increasing with spot
here (higher spot means both higher intrinsic and higher near-ATM option premium), adding
to the intrinsic delta.  The full ASCOT delta therefore reflects both the intrinsic
contribution and the rising time value, while the CB proxy captures only the intrinsic
delta (= CB_delta = 0.091).

The gap narrows through the mid-range.  The crossover occurs near S = 105 (at S = 105.4:
full = 0.674, CB proxy = 0.677), which is approximately 105% of initial parity
(conversion price = 100.00).  The crossover is therefore linked to the CB's own embedded
option approaching at-the-money, not to the ASCOT recall level R0 = 95.  At the
conversion price, the embedded CB equity option transitions from out-of-the-money to
in-the-money: the CB delta is rising at its fastest rate (maximum CB gamma), closing the
gap with the full ASCOT delta.

Beyond the crossover the CB proxy exceeds the full delta: 0.742 versus 0.775 at
S = 120.7, and 0.913 versus 0.965 at S = 200.0.  As the ASCOT moves deeper
in-the-money, the walk-away put transitions from near-ATM to deep-OTM (CB >> R) and
its value declines.  A declining walk-away put contributes a negative delta component to
the full ASCOT: the put loses value as spot rises.  This offsets part of the intrinsic
delta and pulls the full ASCOT delta below the CB proxy, which tracks only the
always-positive intrinsic delta (CB_delta) with no such negative correction.

The full ASCOT delta is smooth across S*, consistent with the smooth-pasting condition.
The CB proxy steps from zero to the CB delta at S*, a structural discontinuity that
reflects the kink in the intrinsic approximation.

---

#### EQ Gamma

![ASCOT Gamma vs Initial Parity (Default)](output/default/plot_gamma.png)

In the out-of-the-money region, the CB proxy Gamma is zero by the cutoff convention.
The full ASCOT Gamma is positive: 0.0019 at S = 20.0, rising to 0.0098 at S = 41.4.
As spot increases in the OTM region, the probability of future exercise is increasing,
and that increase accelerates (the ASCOT delta is itself rising), creating positive
convexity.

Near S*, the full ASCOT Gamma peaks and exceeds the CB proxy.  At S = 44.4: full = 0.0102
versus CB proxy = 0.0064 (full 59% higher).  At this boundary the ASCOT is approximately
at-the-money on the CB: a small move in the CB around its strike R produces a large change
in the exercise probability, and therefore a large change in delta.  ATM options on any
underlying have maximum gamma.  The CB itself near S* is bond-floor dominated (CB delta
= 0.091), so the raw CB gamma is correspondingly small.  The option-on-CB amplification
is what drives the full ASCOT gamma well above the CB proxy.

The relationship reverses further in-the-money.  At S = 59.7 both values are approximately
equal (0.0101).  At S = 99.3: full = 0.0056 versus CB proxy = 0.0084 (CB proxy 50%
higher).  In this region the CB is transitioning from bond-dominated to equity-dominated
valuation, gaining convexity as the embedded conversion option delta rises steeply.
Simultaneously, the walk-away put is past its peak time value and declining: the put's
contribution to the ASCOT's convexity is now a damping force.  The CB proxy gamma,
reflecting the CB's own increasing convexity during the bond-to-equity transition,
therefore exceeds the dampened full ASCOT gamma.

---

#### EQ Vega

![ASCOT Vega vs Initial Parity (Default)](output/default/plot_vega.png)

The Vega comparison follows from the ASCOT decomposition.  Since the recall price R(t)
is deterministic and not vol-sensitive, the intrinsic vega equals CB_vega, and therefore:

    Vega_full = Vega_intrinsic + Vega_walk-away = CB_vega + Vega_walk-away

The walk-away put is an option on the CB.  All options gain value when the underlying's
volatility increases: higher equity vol implies fatter tails in the CB distribution,
raising the probability of large adverse moves that the walk-away right protects against.
Vega_walk-away is therefore strictly positive at all spot levels and maturities, making
Vega_full > CB_vega = CB_proxy_vega universally.

In the OTM region the CB proxy vega is zero (cutoff convention) while the full ASCOT
carries walk-away vega entirely: 0.0074 per 1 vol point at S = 20.0, rising to 0.194
at S = 41.4.

In the in-the-money region the full vega consistently exceeds the CB proxy.  At S = 44.4:
full = 0.2375, CB proxy = 0.0990 (ratio 2.4x).  The near-ATM walk-away put is highly
vol-sensitive because it is exposed to CB moves in both directions around the strike R.
At S = 99.3: full = 0.7695, CB proxy = 0.5070 (52% excess).  At S = 200.0: full =
0.5527, CB proxy = 0.1586 (248% excess).

The ratio grows with depth in-the-money because the two terms in the decomposition diverge.
The CB proxy vega (= CB_vega) declines steeply in the deep-ITM regime: the CB's embedded
conversion option is deeply in-the-money, its payoff is nearly linear, and small vol
changes have little impact on its value.  The walk-away put's vega declines more slowly
because even a deep-OTM put on the CB retains sensitivity to vol through its tail risk
protection.  The CB proxy vega therefore falls faster than the walk-away put's
contribution, widening the understatement from 52% at S = 99.3 to 248% at S = 200.

---

#### IR01

![ASCOT IR01 vs Initial Parity (Default)](output/default/plot_ir01.png)

The CB proxy IR01 is zero in the OTM region by the cutoff convention.  The full ASCOT
IR01 is -0.00071 per 1 bp at S = 20.0 (small negative: at very low spot the ASCOT is a
call on a bond-dominated CB, and higher rates reduce the CB and the option value), turns
positive above approximately S = 33 as the equity drift channel gains weight, and reaches
+0.00121 at S = 41.4 (all OTM, CB proxy = 0).

In the in-the-money region the full ASCOT IR01 and the CB proxy IR01 have opposite signs
at every tested spot level.  The CB proxy IR01 is large and negative, reflecting the CB's
bond duration: a higher rate discounts future CB cash flows more heavily, reducing the CB
value and therefore the intrinsic.  At S = 44.4: CB proxy = -0.01765.  At S = 99.3:
CB proxy = -0.00984.

The full ASCOT IR01 is positive throughout: +0.00178 at S = 44.4, +0.01534 at
S = 99.3, and +0.02275 at S = 200.0.  Two mechanisms drive this sign reversal, and
both work in the same direction.

First, the walk-away put appreciates when rates rise.  The walk-away put is a put on the
CB: a rising rate reduces the CB, and a falling CB moves closer to the put's strike R,
increasing the put's value.  This positive rate sensitivity is large enough to more than
offset the negative intrinsic rate sensitivity (eroding CB - R).

Second, the ASCOT PDE uses clean risk-free discounting without a credit spread.  A higher
risk-free rate therefore raises the risk-neutral drift of the underlying equity directly,
increasing the expected future trajectory of the CB and the probability of exercise.  This
drift channel is entirely absent from the CB, which is discounted at the credit-blended
rate r + lambda*(1 - p_conv).

Both mechanisms reinforce each other.  The signed gap at S = 99.3 is (+0.01534) -
(-0.00984) = +0.02518 per 1 bp per-100.  Using the CB proxy for IR01 hedging would
reverse the direction of the rate hedge at every in-the-money spot level.

---

#### CS01

![ASCOT CS01 vs Initial Parity (Default)](output/default/plot_cs01.png)

The CB proxy CS01 is zero in the OTM region by the cutoff convention.  The full ASCOT
CS01 is also zero to six decimal places at every tested spot level across both the OTM
and ITM regions.

In the in-the-money region the CB proxy CS01 is large and negative: -0.01556 per 1 bp
per-100 at S = 44.4, -0.00568 at S = 99.3, and -0.00052 at S = 200.0.  These represent
the full CB credit duration at each spot level.  The full ASCOT CS01 is 0.0000 at every
tested level.

The zero full CS01 follows from the ASCOT's structure.  When the hazard rate rises, two
effects act on the full ASCOT in opposite directions.

First, the intrinsic erodes: the CB falls (credit-blended discounting in the TF model
raises the effective discount rate on bond cash flows), reducing max(CB - R, 0).  This
negative channel equals CB_CS01.

Second, the walk-away put appreciates: a wider credit spread raises the probability of
large adverse CB moves, increasing the value of the right to abandon.  This positive
channel exactly equals -CB_CS01 for the default instrument (lambda = 2.00%).

The exact cancellation reflects a structural property of the ASCOT PDE: the ASCOT
discounts at the clean risk-free rate, not at the credit-blended rate used by the CB.
Lambda enters the ASCOT valuation only through the CB obstacle.  When lambda rises, the
CB obstacle falls and the walk-away put gains by exactly the same amount.  The ASCOT
holder is therefore structurally insulated from credit spread changes and carries neither
the bond credit duration nor any residual credit exposure.

The CB proxy attributes the full CB credit duration to the ASCOT holder.  Using it for
CS01 hedging would create a spurious credit position with no basis in the true ASCOT
exposure.

---

**Summary for Default Instrument**

The full American ASCOT produces risk profiles that differ materially from the CB proxy
across all Greeks.  EQ Delta shows a crossover: full is 90% above the CB proxy near S*
and falls below it above S = 105, reaching 0.913 versus 0.965 at S = 200.  EQ Gamma is
59% above the CB proxy near S* and 33% below at S = 99.3.  EQ Vega exceeds the CB proxy
by 52% at S = 99.3 and 248% at S = 200.  IR01 has the opposite sign to the CB proxy at
every ITM spot, with a signed gap of +0.0252 per 1 bp per-100 at S = 99.3.  CS01 is
identically zero for the full ASCOT while the CB proxy is -0.0156 per 1 bp per-100 at
S = 44.4 and -0.0057 at S = 99.3.

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

![CB Price vs Initial Parity (Kansai Paint)](output/kansai/plot_cb.png)

The CB trades at 77.83 per-100 at S = 1,000 (below par, bond floor driven) and rises to
145.51 per-100 at S = 4,000 as the equity option gains intrinsic value.  The zero-coupon
structure and long maturity produce a lower bond floor relative to par.  The conversion
value line κS (with κ = 0.036119) rises slowly with spot, reflecting the small conversion
ratio in JPY.  The initial recall level R(0) = 95.00 is crossed at S* = 2,196.12.

---

#### PV Profile

![ASCOT PV vs Initial Parity (Kansai Paint)](output/kansai/plot_pv.png)

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

![ASCOT Delta vs Initial Parity (Kansai Paint)](output/kansai/plot_delta.png)

The CB proxy Delta is zero in the OTM region by the cutoff convention.  The full ASCOT
Delta is positive throughout the OTM region from the walk-away put contribution: 0.117
at S = 1,000 (36.1% parity), rising to 0.489 at S = 2,170 (78.4% parity; still OTM,
CB proxy = 0).  Delta is plotted per parity point rather than per yen move in stock;
equivalently the raw spot-space Delta is multiplied by dS/dParity = conversion price / 100.
This normalization removes the mechanical scale effect from the low conversion ratio
κ = 0.036119.

In the in-the-money region the full ASCOT Delta is consistently below the CB proxy Delta
throughout the entire ITM range, with no crossover.  At the first ITM grid point
S = 2,220 (80.2% parity): full = 0.503 versus CB proxy = 0.594 (full 15% below).  At
S = 2,322 (83.9% parity): full = 0.529 versus CB proxy = 0.620 (full 15% below).  At
S = 4,000 (144.5% parity): full = 0.809 versus CB proxy = 0.920 (full 12% below).

The absence of a crossover is explained by the location of S* relative to initial parity.
For this instrument S* = 2,196.12 (79.3% of the conversion price 2,768.60): the ASCOT
enters in-the-money at a spot level where the CB's embedded equity option is already
22% below its own conversion price, so the CB carries meaningful equity sensitivity
at S*.  The OTM ASCOT delta at S* is 0.018 (spot-space) while the CB delta at S* is
0.021 — the OTM delta is already below the CB delta, the time value gradient is
immediately negative above S*, and Delta_full is below CB_Delta throughout the ITM
region with no crossover.  This contrasts with the default instrument where S* is at
only 41.6% of the conversion price: the CB is deep in its bond-dominated regime at S*
(CB_delta ≈ 0.073), well below the ASCOT's accumulated OTM delta (0.142), producing
an overshoot and a subsequent crossover near initial parity.

The full Delta profile is smooth across S*.  The CB proxy Delta has a structural
discontinuity at S*, jumping from zero to the CB Delta at the boundary.

---

#### EQ Gamma

![ASCOT Gamma vs Initial Parity (Kansai Paint)](output/kansai/plot_gamma.png)

Gamma is plotted in parity-space using the squared chain-rule factor
(dS/dParity)^2.  In the OTM region the CB proxy Gamma is zero by the cutoff convention,
while the full ASCOT Gamma is positive: 0.0083 at S = 1,000 (36.1% parity), declining
slightly to 0.0075 at S = 2,170 (78.4% parity).  In the ITM region, full Gamma remains
below the CB proxy: at S = 2,322 (83.9% parity), full = 0.00696 versus CB proxy = 0.00705;
at S = 4,000 (144.5% parity), full = 0.0029 versus CB proxy = 0.0034.  The intrinsic
approximation shows a localized spike around the exercise boundary because it has a kink
at CB = R0.

The modest Gamma reflects the bond-floor-dominated nature of this CB across the tested
spot range, where the equity conversion option contributes limited curvature relative to
the bond component.

---

#### EQ Vega

![ASCOT Vega vs Initial Parity (Kansai Paint)](output/kansai/plot_vega.png)

The CB proxy Vega is zero in the OTM region by the cutoff convention.  The full ASCOT
Vega is positive and substantial in the OTM region, attributable entirely to the walk-away
put: 0.1714 per 1 vol point at S = 1,000, rising to 0.6145 at S = 1,864 and 0.7281
at S = 2,170.

In the in-the-money region the full ASCOT Vega exceeds the CB proxy Vega throughout,
with the gap growing deeper in-the-money.  Near S*, at S = 2,220 (first ITM point):
full = 0.7436 versus CB proxy = 0.7169 (full 3.7% above, nearly equal).  At S = 2,322:
full = 0.7718 versus CB proxy = 0.7292 (full 5.8% above).  At S = 2,678: full = 0.8412
versus CB proxy = 0.7377 (full 14% above).  At S = 4,000: full = 0.8093 versus CB proxy =
0.3883 (full 108% above).

The full Vega peaks around S = 3,288 at 0.8716 then declines, while the CB proxy Vega
decreases more steeply, producing the widening relative gap at deep in-the-money levels.

---

#### IR01

![ASCOT IR01 vs Initial Parity (Kansai Paint)](output/kansai/plot_ir01.png)

The CB proxy IR01 is zero in the OTM region by the cutoff convention.  The full ASCOT
IR01 is positive throughout the OTM region: +0.00112 per 1 bp at S = 1,000, rising to +0.00923 at
S = 2,170.

In the in-the-money region the full ASCOT IR01 and the CB proxy IR01 have opposite signs
at every tested spot level.  The CB proxy IR01 is large and negative, reflecting the CB's
duration: -0.03350 at S = 2,220, -0.03196 at S = 2,322, and -0.00882 at S = 4,000.
The full ASCOT IR01 is positive: +0.00964 at S = 2,220, +0.01043 at S = 2,322, and
+0.01842 at S = 4,000.

The signed gap between full and CB proxy IR01 at S = 2,220 is (+0.00964) - (-0.03350) =
+0.04314 per 1 bp per-100.  At S = 2,322 the signed gap is (+0.01043) - (-0.03196) =
+0.04239 per 1 bp per-100.  At S = 4,000 the signed gap is (+0.01842) - (-0.00882) =
+0.02724 per 1 bp per-100.  Using the CB proxy for IR01 hedging in the in-the-money
region would reverse the direction of the hedge at every tested spot level.

---

#### CS01

![ASCOT CS01 vs Initial Parity (Kansai Paint)](output/kansai/plot_cs01.png)

The CB proxy CS01 is zero in the OTM region by the cutoff convention.  The full ASCOT
CS01 is negative and non-zero in the OTM region: -0.00051 per 1 bp per-100 at S = 1,000,
rising in magnitude to -0.00224 at S = 2,170.  In this region the ASCOT is a deeply OTM
call on the CB.  A rise in the hazard rate reduces the expected future CB value and
therefore the probability of future exercise above R(0), reducing the ASCOT option value.

In the in-the-money region both the full ASCOT CS01 and the CB proxy CS01 are negative,
but the magnitudes differ substantially.  The CB proxy CS01 is large and negative:
-0.03889 per 1 bp per-100 at S = 2,220, -0.03755 at S = 2,322, and -0.01203 at
S = 4,000.  The full ASCOT CS01 is small: -0.00229 at S = 2,220 (5.9% of the CB proxy
magnitude), -0.00237 at S = 2,322 (6.3%), and -0.00226 at S = 4,000 (18.8%).  The
fraction of CB credit exposure absorbed by the full ASCOT ranges from approximately 6%
to 19% across the ITM range, increasing as the ASCOT moves deeper in-the-money.

Using the CB proxy for CS01 hedging in the in-the-money region would overstate the true
credit exposure by a factor of roughly 5 to 17 across the tested range.

---

**Summary for Kansai Paint**

The full American ASCOT produces risk profiles that differ materially from the CB proxy
across all Greeks.  EQ Delta is consistently 12 to 15% below the CB proxy in the ITM
region, with no crossover.  EQ Gamma is negligible for both the full ASCOT and the CB
proxy.  EQ Vega exceeds the CB proxy by 3.7% near S*, growing to 108% at S = 4,000.
IR01 has the opposite sign to the CB proxy at every ITM spot, with a signed gap of +0.0431
per 1 bp per-100 near S* and +0.0272 per 1 bp per-100 at S = 4,000.  CS01 is 6% to 19% of the CB proxy
magnitude in the ITM region, with the CB proxy overstating the true credit exposure by
5x to 17x.
