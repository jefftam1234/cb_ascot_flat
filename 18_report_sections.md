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

Market convention values the ASCOT at its intrinsic value, defined as max(CB(S, 0)- R(0), 0), which treats the ASCOT as if exercise is immediate.  The full American model
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

### 5.12.2 Equity Sensitivity (Delta and Gamma)

**Delta**

The full ASCOT delta equals the CB proxy delta plus the walk-away put delta:

> Delta_full = Delta_proxy + Delta_walk-away

where Delta_proxy is zero in the OTM region and equals CB_Delta in the ITM region.

The walk-away put delta changes sign across S*, and this sign change is the mechanism
behind the full ASCOT delta behaviour in both regions.

In the **OTM region**, the walk-away put is the entirety of the ASCOT value.  As spot
rises toward S*, the probability of future exercise increases and the walk-away put value
rises with it: Delta_walk-away > 0.  The full ASCOT therefore carries positive delta even
where the CB proxy assigns zero.

In the **ITM region**, the walk-away put is out-of-the-money on the CB.  Its residual
value is positive but shrinking — as the CB moves further above R(t), a credit event
serious enough to push the CB back below R(t) becomes progressively less likely.  As spot
rises, that residual shrinks further: Delta_walk-away < 0.  The full ASCOT delta is
therefore below CB_Delta, and the CB proxy, which tracks CB_Delta with no offset,
overstates the true equity exposure.

The sign of Delta_walk-away immediately above S* determines whether a crossover between
Delta_full and CB_Delta occurs.  By the smooth-pasting condition, Delta_full is continuous
at S*, which constrains:

> Delta_walk-away at S+* = OTM delta(S*) − CB_Delta(S*)

If the ASCOT's accumulated OTM delta at S* exceeds CB_Delta(S*), the walk-away put delta
is still positive just above S*, Delta_full briefly overshoots CB_Delta, and a crossover
occurs later.  If the CB is already carrying meaningful equity sensitivity at S*, the
walk-away put delta is immediately negative above S* and no crossover occurs.

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

### 5.12.3 Volatility Sensitivity (Vega)

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

### 5.12.4 Credit Spread Sensitivity (CS01)

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

The economic reason for the offset is structural.  The ASCOT holder does not bear the
default loss the way a CB holder does: if the issuer defaults, the ASCOT holder simply
does not exercise — there is no delivery obligation and no loss of principal.  The
walk-away right provides this insulation precisely because it is long the credit tail risk
that the CB holder is short.  A credit spread widening that harms the CB holder therefore
partially benefits the ASCOT holder through the appreciating walk-away put.

---

### 5.12.5 Interest Rate Sensitivity (IR01)

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

**Conclusion**

The American time value of the ASCOT — the walk-away put — is economically material and
produces risk profiles that differ notably from both the market-convention intrinsic
approximation and the raw CB proxy across all Greeks.  The intrinsic approximation assigns
zero value and zero sensitivity in the OTM region where the walk-away put is the entirety
of the ASCOT, and it misrepresents the direction or magnitude of every Greek in the ITM
region: it overstates equity delta, understates vega, overstates credit sensitivity, and
inverts the sign of rate sensitivity.  These differences are not small corrections but
structural errors arising from ignoring the walk-away right.  Section 5.19 tests and
quantifies these differences numerically across a representative CB and translates them
into portfolio-level model risk exposures.

---

## 5.19 Model Assumption Analysis

**Goal**

To test the model assumption: *is using intrinsic valuation adequate and appropriate for
pricing and hedging the ASCOT?*  Market convention values the ASCOT at its intrinsic
value max(CB − R(0), 0), discarding the walk-away put that an American model prices
explicitly.  This section tests numerically whether that discarded time value is material
to the risk sensitivities used in hedging.

**Scope**

The analysis uses two representative instruments: a synthetic short-maturity CB (the
``default'' bundle) and the Kansai Paint convertible bond (4613 JT), a real-world long-
maturity zero-coupon CB.  The CB pricing implementation is first benchmarked against
QuantLib to confirm correctness of the obstacle surface.  The full suite of Greeks is
then computed across the spot range for each instrument under three pricing conventions:
the full American ASCOT, the intrinsic approximation (market convention), and the raw CB
proxy.

**Methodology**

All computations use the Crank-Nicolson finite-difference PDE with PSOR obstacle
handling.  Greeks are computed as follows.  Delta and Gamma use log-space finite
differences on the PDE solution grid converted to spot-space via the chain rule.  Vega,
IR01, and CS01 use central bump-and-reprice with bumps of 1 vol point, 1 bp, and 1 bp
respectively.  The credit model uses the Tsiveriotis-Fernandes specification for the CB
PDE and clean risk-free discounting for the ASCOT PDE.

---

### 5.19.1 CB Implementation Benchmark Against QuantLib

A synthetic default CB is constructed with simple, controlled parameters to provide a
clean benchmark.  The instrument is a short-dated coupon CB with both issuer call and
holder put provisions, chosen so that all CB sub-model components (credit-adjusted
discounting, conversion option, embedded call, embedded put) are simultaneously active
and testable.

| Parameter | Value |
|---|---|
| Face value | 100.00 per-100 |
| Conversion ratio κ | 1.0000 |
| Maturity | 5.00 years |
| Coupon | 2.00% (semi-annual) |
| Issuer call | 100.00 from year 2.00 |
| Holder put | 100.00 from year 1.00 |
| Risk-free rate r | 3.00% |
| Dividend yield q | 1.00% |
| Equity volatility σ | 30.00% |
| Hazard rate λ | 2.00% |
| Recovery fraction | 40.00% |

The same instrument is used in Appendix A for the ASCOT Greek profile analysis, where
the ASCOT recall terms are introduced.

The CB is priced at 10 representative spot levels using the local Crank-Nicolson
finite-difference engine and independently using QuantLib's binomial convertible-bond
engine, both under the Tsiveriotis-Fernandes credit-spread configuration with identical
market and term parameters.

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
error is 0.0281 per-100.  The maximum relative error is 0.027%.  The differences are
within the expected discretization tolerance between a finite-difference PDE and a
binomial lattice.  The CB implementation is accepted as the obstacle surface for ASCOT
pricing in the following sections.

---

### 5.19.2 ASCOT Greek Profiles --- Kansai Paint (4613 JT)

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

Kansai is selected as the primary case because it is a plain vanilla CB — no issuer call
and no holder put — so the CB price evolves smoothly as a function of equity spot without
any embedded optionality introducing additional kinks or early-exercise boundaries.  This
isolates the dynamic we want to study: how the moneyness of the CB relative to the recall
price R(t) interacts with the American nature of the ASCOT payoff, without the CB's own
optionality obscuring the picture.

---

#### CB Profile

![CB Price vs Initial Parity (Kansai Paint)](output/kansai/plot_cb.png)

The CB price is bond-floor-dominated at low spot, where the zero-coupon structure and
long maturity produce a floor well below par.  As spot rises, the embedded conversion
option gains value and the CB transitions progressively toward its conversion value κS.
The initial recall level R(0) = 95.00 is crossed at S* = 2,196.12 (79.3% of the
conversion price), marking the point at which the ASCOT enters the money.  The CB
therefore already carries meaningful equity sensitivity before the ASCOT becomes
in-the-money.

---

#### PV Profile

![ASCOT PV vs Initial Parity (Kansai Paint)](output/kansai/plot_pv.png)

The plot shows the full ASCOT value and the intrinsic, with the shaded gap between them
representing the walk-away put value.  Below S*, the intrinsic is zero and the shaded
region spans the entire ASCOT value.  Through the ITM region the intrinsic grows but the
shaded gap remains material throughout the spot range: even at 144.5% parity the
walk-away put accounts for approximately 14% of the full value (8.14 per-100 on a full
value of 58.65 per-100), reflecting the long recall period over which a credit event
could occur.  The intrinsic approximation understates the full ASCOT value at every spot
level and by a growing absolute amount through the middle of the range.

---

#### Walk-Away Put Profile

![Walk-Away Put Value and Delta (Kansai Paint)](output/kansai/plot_walk_away_put.png)

The walk-away put value and delta are isolated as value = ASCOT_full − ASCOT_intrinsic
and delta = Delta_full − Delta_intrinsic.

**Value panel.**  The walk-away put value rises through the OTM region, peaks near S*,
and then declines gradually through the ITM range.  The rising OTM profile is notable:
as spot approaches S*, the ASCOT becomes increasingly likely to be exercised in the
future, making the protection against a bad outcome more valuable.  The gradual ITM
decline reflects the falling probability that a credit event will be severe enough to
push the CB back below R(t) before recall expiry, but the long maturity keeps this
residual value material even at the top of the spot range.

**Delta panel.**  The walk-away put delta is positive and rising through the OTM region,
peaks near S*, then flips to a roughly constant negative level in the ITM region (approximately −0.10).
This sign flip at S* is the direct mechanism behind the full ASCOT delta behaviour
described in the next section.

---

#### EQ Delta

![ASCOT Delta vs Initial Parity (Kansai Paint)](output/kansai/plot_delta.png)

Delta is plotted per parity point (raw spot-space delta multiplied by dS/dParity =
conversion price / 100), removing the mechanical scale effect from the low conversion
ratio κ = 0.036119.

**OTM region.**  The CB proxy Delta is zero by the cutoff convention.  The full ASCOT
Delta is positive and rising throughout, driven entirely by the walk-away put delta being
positive in this region.  As spot rises toward S*, the walk-away put gains value and its
positive delta adds directly to the full ASCOT delta.

**ITM region.**  The walk-away put delta flips to approximately −0.10 immediately above
S* and remains near that level throughout the ITM range.  This roughly constant offset
pulls the full ASCOT delta below the CB proxy by a stable margin across the entire ITM
region.  The gap is approximately equal to the walk-away put delta, confirming that the
delta shortfall is entirely attributable to the residual walk-away put value shrinking as
spot rises.

**No crossover.**  As derived in Section 5.12.2, a crossover requires the walk-away put
delta to be positive immediately above S*.  For Kansai, S* sits at 79.3% of the
conversion price, where the CB already carries meaningful equity sensitivity.  The
accumulated OTM ASCOT delta entering S* (0.018 spot-space) is already below the CB delta
at S* (0.021 spot-space), the walk-away put delta is negative from the first ITM point,
and no crossover occurs.

The full Delta profile is smooth across S*.  The CB proxy Delta has a structural
discontinuity at S*, jumping from zero to the CB Delta at the boundary.

---

#### EQ Gamma

![ASCOT Gamma vs Initial Parity (Kansai Paint)](output/kansai/plot_gamma.png)

Gamma is plotted in parity-space using the squared chain-rule factor (dS/dParity)².
The full ASCOT Gamma is positive throughout and smooth.  In the OTM region the CB proxy
Gamma is zero while the full ASCOT carries positive convexity, broadly flat across the
OTM range.  In the ITM region the full Gamma runs modestly below the CB proxy.  The
localized spike in the intrinsic approximation near S* is numerical noise from finite
differencing of the step-function payoff and carries no economic content.

The overall gamma profile is modest for both the full ASCOT and the CB proxy, reflecting
the bond-floor-dominated nature of this CB across the tested spot range.

---

#### EQ Vega

![ASCOT Vega vs Initial Parity (Kansai Paint)](output/kansai/plot_vega.png)

The CB proxy Vega is zero OTM and tracks the CB standalone Vega in the ITM region.  The
full ASCOT Vega exceeds the CB proxy throughout all regions; the gap widens progressively
deeper in-the-money, reaching approximately double the CB proxy at the top of the tested
range.  This widening occurs because the CB standalone Vega declines steeply as the
conversion option becomes nearly linear deep ITM, while the walk-away put Vega declines
more slowly — tail credit risk persists regardless of how far in-the-money the ASCOT is.

A distinctive feature of Kansai is visible on the CB standalone line: in the OTM region,
the full ASCOT Vega is below the CB standalone Vega.  This is because the ASCOT only
partially participates in the CB's long-dated option vega (its delta-on-CB is less than 1
OTM).  Once the ASCOT crosses into the ITM region the walk-away put's vega amplification
dominates and the full ASCOT Vega exceeds the CB standalone.

---

#### CS01

![ASCOT CS01 vs Initial Parity (Kansai Paint)](output/kansai/plot_cs01.png)

Both curves are negative throughout.  In the OTM region the CB proxy is zero while the
full ASCOT carries a small negative CS01: a higher credit spread reduces the expected
future CB value and therefore the probability of profitable exercise, slightly reducing
the walk-away put value.

In the ITM region the two curves diverge sharply.  The CB proxy CS01 is large and
negative near S*, reflecting the CB's full credit duration, and declines gradually in
magnitude as spot rises and the bond component diminishes.  The full ASCOT CS01 by
contrast is small and roughly flat across the entire ITM range — close to zero
throughout.  The gap between the two is therefore widest immediately above S* and narrows
with depth in-the-money as the CB proxy CS01 itself decreases.  Using the CB proxy for
CS01 hedging would establish a credit position far larger than the ASCOT actually carries
at any ITM spot level.

---

#### IR01

![ASCOT IR01 vs Initial Parity (Kansai Paint)](output/kansai/plot_ir01.png)

The most prominent feature is the sign reversal between the full ASCOT and the CB proxy
in the ITM region.  The CB proxy IR01 is zero OTM and large negative ITM, reflecting the
CB's bond duration.  The full ASCOT IR01 is positive throughout — both OTM and ITM — and
the two curves lie on opposite sides of zero at every ITM spot level.

In the OTM region, the full ASCOT IR01 is positive and rising, driven by the equity drift
channel.  In the ITM region, both the walk-away put appreciation and the equity drift
channel push the full ASCOT IR01 positive, more than offsetting the negative intrinsic
rate sensitivity.  Using the CB proxy for IR01 hedging would reverse the direction of
the rate hedge at every in-the-money spot level.

---

### 5.19.3 Model Risk Exposure Analysis (MREA)

The MREA quantifies the aggregate error from using the intrinsic approximation across the
ASCOT book.  It is computed using the notional-weighted maturity (NWM) of all ASCOT
positions in the book:

> NWM = sum_i (N_i * T_i) / sum_i N_i

where N_i is the signed notional of position i (positive = long, negative = short) and
T_i is its remaining recall expiry.  For the current ASCOT book, the NWM is 2.7570 years
and the total signed notional is JPY −2.664 billion (net short, after converting all
USD-denominated positions to JPY).  The representative Greek profiles for a 2.7570-year
effective ASCOT on Kansai Paint (all other parameters unchanged from Section 5.19.2) are
used to characterise each position's misstatement.

MREA figures represent the average difference (full American ASCOT minus intrinsic
approximation) across the 80–120% initial parity range, scaled to the signed portfolio
notional.  EQ Delta and EQ Gamma are expressed per 1 parity point move, which is
equivalent to approximately 1% of the conversion price and provides a consistent
normalisation across CBs with different underlying stock prices.  Positive MREA denotes
an exposure the intrinsic convention underestimates in the direction adverse for the net
short book; negative MREA denotes a hidden loss or over-hedge that intrinsic obscures.

**ASCOT sensitivity assumptions**

| Sensitivity | Bump assumption |
|---|---|
| EQ Delta | 1 parity point move (dS = JPY 27.69) |
| EQ Gamma | 1 parity point move (Δdelta per parity point) |
| Vega | 1 vol point (1% absolute shift in σ) |
| IR01 | 1 bp parallel shift in r |
| CS01 | 1 bp parallel shift in λ (credit hazard rate) |

**MREA results**

| Risk metric | Per-100 error (avg 80–120% parity) | Portfolio MREA (JPY −2.664bn net short) |
|---|---|---|
| PV (walk-away put) | +7.44 per 100 | −JPY 198.3M |
| EQ Delta | −0.1054 per 100 per pp | +JPY 2.81M per pp |
| EQ Gamma | −0.00578 per 100 per pp² | +JPY 0.15M per pp |
| Vega | +0.0519 per 100 per vol pt | −JPY 1.38M per vol pt |
| IR01 | +0.0298 per 100 per bp | −JPY 0.79M per bp |
| CS01 | +0.0244 per 100 per bp | −JPY 0.65M per bp |

**Interpretation**

The PV MREA of −JPY 198.3M is a structural overstatement of the short book's value.
The intrinsic assigns zero value to the walk-away put; as a net short book, this means
the liability is understated by JPY 198.3M on average across the at-the-money region.
The book appears JPY 198.3M more profitable than a full valuation would show.

The EQ Delta MREA of +JPY 2.81M per parity point means the intrinsic over-hedges equity.
The full ASCOT delta is lower than the intrinsic delta in the ITM region (walk-away put's
negative delta offsets the CB delta); for a net short book the intrinsic therefore
instructs the desk to sell more stock than necessary, leaving a hidden long delta of
+JPY 2.81M per parity point in the equity hedge.

The Vega MREA of −JPY 1.38M per vol point means the intrinsic understates vol exposure.
The book is more short vega than the intrinsic implies; a vol-hedged book would carry
an unhedged short vega of JPY 1.38M per vol point.

The IR01 MREA of −JPY 0.79M per bp reflects the sign reversal identified in Section
5.12.5.  The full ASCOT carries positive IR01 per position; for the net short book this
produces a negative portfolio IR01.  The intrinsic, assigning negative IR01 to each long
ASCOT, gives the net short book a positive portfolio IR01.  The two are not only
different in magnitude but opposite in sign, and a rate hedge built on intrinsic would be
on the wrong side of the market.

The CS01 MREA of −JPY 0.65M per bp captures the structural credit insulation of the full
ASCOT.  The intrinsic tracks the CB's full credit duration; the full ASCOT is nearly
credit-neutral through the walk-away put offset.  For the net short book, the intrinsic
instructs an over-sized credit hedge: the desk would sell more credit protection than the
position actually requires by JPY 0.65M per bp.

---

**Summary**

The intrinsic approximation is not adequate or appropriate for pricing or hedging the
ASCOT.  Across both instruments, the walk-away put — the time value discarded by the
intrinsic convention — produces material and directionally incorrect risk sensitivities in
every Greek.  EQ Delta is overstated ITM (the walk-away put's negative delta offsets the
CB proxy), and the intrinsic assigns zero delta where the full ASCOT carries positive
exposure OTM.  EQ Vega is understated at every spot level, with the gap widening with
depth in-the-money.  CS01 is overstated: the full ASCOT CS01 is small and roughly flat
near zero across the ITM range while the intrinsic tracks the CB's full credit duration.
IR01 has the wrong sign: the full ASCOT IR01 is positive throughout the ITM range while
the intrinsic IR01 is large and negative, so applying the intrinsic approximation as a
hedge would reverse the rate position.

The MREA quantifies these errors for the current book (JPY −2.664bn signed net notional
in JPY, NWM 2.7570 years) over the 80–120% parity range.  For the net short book, the
intrinsic overstates the portfolio value by JPY 198.3M (the walk-away put is a liability
that intrinsic ignores), over-hedges equity delta by JPY 2.81M per parity point,
understates short vega by JPY 1.38M per vol point, and applies rate and credit hedges
that are wrong in both sign and magnitude (IR01 error: JPY 0.79M per bp; CS01 error:
JPY 0.65M per bp).  The assumption that intrinsic valuation is adequate is rejected.

---

## Appendix A: ASCOT Greek Profiles — Synthetic Default Bundle

The synthetic default bundle is a short-maturity coupon CB used primarily to validate the
flat model against the QuantLib benchmark (Section 5.19.1).  Its Greek profiles are
qualitatively consistent with the Kansai analysis but exhibit three contrasting features —
a delta crossover, a different vega ordering OTM, and near-complete CS01 cancellation —
that are instructive for understanding the general behaviour of the ASCOT decomposition.
The ASCOT overlay uses recall price R(0) = 95.00 accreting to R(T) = 100.00 over a 5-year
recall period.  S* = 41.58 (41.6% of the conversion price / par).

---

#### CB Profile

![CB Price vs Initial Parity (Default Bundle)](output/default/plot_cb.png)

The default bundle CB is coupon-bearing and short-dated, placing its bond floor close to
par at low spot.  The CB has a steeper equity ramp than Kansai: because the conversion
ratio κ = 1, each unit of spot maps directly to one share, and the conversion value is
simply the spot level.  S* = 41.58 lies well below the conversion price (par = 100),
meaning the CB is still heavily bond-dominated — and carries low equity sensitivity —
when the ASCOT first enters the money.

---

#### PV Profile

![ASCOT PV vs Initial Parity (Default Bundle)](output/default/plot_pv.png)

The shaded walk-away put gap is clearly visible below S* and persists through the ITM
region.  Relative to Kansai, the time value premium in the ITM region is smaller as a
fraction of the full value, consistent with the shorter maturity reducing the residual
probability of a credit event.  The intrinsic approximation understates the full ASCOT
value at every spot level, though by a smaller margin than for the long-dated Kansai
instrument.

---

#### Walk-Away Put Profile

![Walk-Away Put Value and Delta (Default Bundle)](output/default/plot_walk_away_put.png)

The walk-away put value and delta follow the same qualitative pattern as Kansai: value
rises through the OTM region, peaks near S*, and declines through the ITM region; delta
is positive OTM and flips negative in the ITM region.  The key quantitative difference is
the smaller ITM value: the shorter maturity reduces the residual credit tail risk and the
put value declines more steeply through the ITM range.

---

#### EQ Delta

![ASCOT Delta vs Initial Parity (Default Bundle)](output/default/plot_delta.png)

**OTM region.**  As with Kansai, the CB proxy is zero and the full ASCOT carries positive
delta driven by the walk-away put's positive delta in this region.

**ITM region — crossover.**  The default bundle exhibits a delta crossover that Kansai
does not: immediately above S*, the full ASCOT delta briefly exceeds the CB proxy before
falling below it further in-the-money.

At S* = 41.58 (41.6% of par), the CB is still bond-dominated and carries low equity
sensitivity.  The full ASCOT has accumulated positive delta from the entire OTM walk-away
region entering S*.  This accumulated delta exceeds the CB's low equity delta at S*, so
the walk-away put delta immediately above S* is still positive — it has not yet flipped
sign.  Just above S*, the put delta transitions from positive to negative gradually; during
this transition the full delta is above the CB proxy.  Once the put delta becomes
sufficiently negative the full delta falls below the CB proxy and remains there through the
rest of the ITM region.

For Kansai, S* is at 79% of the conversion price where the CB already carries meaningful
equity sensitivity, so the walk-away put delta is negative from the first ITM point and no
crossover occurs.

---

#### EQ Gamma

![ASCOT Gamma vs Initial Parity (Default Bundle)](output/default/plot_gamma.png)

The default bundle Gamma is qualitatively similar to Kansai but more pronounced near S*:
the shorter-dated option has higher curvature near the exercise boundary.  The spike in
the intrinsic approximation near S* is again numerical noise from finite differencing and
carries no economic content.  In the ITM region the full ASCOT Gamma declines toward the
CB proxy level.

---

#### EQ Vega

![ASCOT Vega vs Initial Parity (Default Bundle)](output/default/plot_vega.png)

The full ASCOT vega exceeds both the CB proxy and the CB standalone across the entire
spot range.  This is the key contrast with Kansai, where the full ASCOT vega is below the
CB standalone in the OTM region.

For this short-dated instrument, the embedded equity option is nearly worthless at low
spot: the CB trades close to its bond floor and the conversion option contributes
negligible vega.  Even the modest walk-away put vega exceeds this near-zero CB standalone
vega, placing the full ASCOT above the CB standalone everywhere.  In the ITM region the
CB standalone vega rises as the equity ramp steepens, but the walk-away put's additional
contribution keeps the full above both the CB proxy and the CB standalone throughout.

---

#### CS01

![ASCOT CS01 vs Initial Parity (Default Bundle)](output/default/plot_cs01.png)

The near-complete CS01 cancellation is the most striking feature of the default bundle.
The full ASCOT CS01 is indistinguishable from zero across the entire spot range, including
deep in-the-money, while the CB proxy CS01 is large and negative in the ITM region.  The
walk-away put's gain from a spread widening cancels the intrinsic loss almost exactly.

For Kansai, the cancellation is only partial because the longer maturity and lower hazard
rate mean the walk-away put does not gain as much from the same spread widening relative
to the intrinsic loss.  For the default bundle, the higher hazard rate (2%) and shorter
maturity combine to make the walk-away put's credit sensitivity closely track the
intrinsic's, producing near-complete offset.  The ASCOT holder is effectively
credit-neutral across the tested spot range.

---

#### IR01

![ASCOT IR01 vs Initial Parity (Default Bundle)](output/default/plot_ir01.png)

As with Kansai, the full ASCOT IR01 and the CB proxy IR01 have opposite signs at every
ITM spot level.  The CB proxy IR01 is negative (bond duration); the full ASCOT IR01 is
positive throughout.  Both the walk-away put appreciation channel and the equity drift
channel operate here in the same way as described for Kansai in Section 5.12.5.

The magnitude of the sign reversal is more pronounced for the default bundle relative to
Kansai, consistent with the near-complete CS01 cancellation: an instrument that is
effectively credit-neutral is also more strongly insulated from the bond-floor component
of rate sensitivity, producing a larger positive IR01 offset.

---

#### Summary

| Greek | Kansai (main case) | Default bundle (appendix) |
|---|---|---|
| EQ Delta (ITM) | ~−0.10 below CB proxy; no crossover | Crossover just above S*, then below CB proxy |
| EQ Gamma | Modest; numerical noise near S* | Similar; more pronounced at S* |
| EQ Vega (vs CB standalone) | Below CB standalone OTM; above ITM | Above CB standalone across entire range |
| CS01 (ITM) | Full small and flat; CB proxy large and negative near S* | Full ≈ 0 throughout; near-complete cancellation |
| IR01 (ITM) | Opposite sign to CB proxy | Opposite sign to CB proxy; larger reversal |

The contrast between the two instruments illustrates that the qualitative features of the
ASCOT decomposition — positive walk-away put delta OTM, CS01 structural insulation, IR01
sign reversal — are robust across instrument types, while the degree of cancellation and
the presence or absence of a delta crossover depend on the CB characteristics at S*.
