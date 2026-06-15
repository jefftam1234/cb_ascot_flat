# ASCOT Greeks — Economic Commentary

This document explains the economic intuition behind the Greek plots for the full American
ASCOT and the CB proxy.  The CB proxy is what a trader applying the market-convention
intrinsic approximation would use as a hedge ratio: it copies the CB Greek where the
ASCOT is in-the-money (CB > R₀) and is zero where it is out-of-the-money.  The central
question is how much the two diverge, and why.

---

## 1. Instrument structure

The **ASCOT** is an American call option on a convertible bond, struck at an accreting
recall price R(t).  It can be decomposed exactly as:

> ASCOT full = ASCOT intrinsic + walk-away put

The **intrinsic** is `max(CB − R₀, 0)` — the value from exercising immediately.  The
**walk-away put** is the holder's right to let the ASCOT expire worthless rather than take
delivery of a CB that has deteriorated below R(t).  This right has value as long as there
is any probability that the CB will fall below R(t) before the recall expiry.

Two forces make waiting costly for the ASCOT holder: CB coupons accrue to the asset-swap
counterparty for every day the option is unexercised, and R(t) accretes upward over time,
eroding future intrinsic value.  Both forces push toward immediate exercise.  The only
reason to remain unexercised is the walk-away right.  This decomposition drives every
qualitative feature of the Greek profiles below.

---

## 2. CB plot

The CB price moves through three regimes as spot increases.  At low spot, the conversion
option is far out-of-the-money and the CB trades near its **credit-adjusted bond floor**:
the present value of all coupon and principal cash flows discounted at a rate that
incorporates the issuer's default probability.  As spot rises toward the conversion price,
the conversion option gains delta and the CB departs from the bond floor.  At high spot,
the conversion option is deep in-the-money and the CB trades near its conversion value κS.

The **initial recall price R₀** marks where the ASCOT enters the money: when the CB
crosses R₀, intrinsic value becomes positive.  R₀ is set below par (typically 95 per 100),
but for a long-dated or low-coupon issuer the credit-adjusted bond floor can sit well
below R₀, so the ASCOT can be out-of-the-money over a wide range of spot.  For Kansai
(long-dated zero-coupon), the bond floor is around 78, and the ASCOT remains OTM until
spot reaches roughly 79% of the conversion price.

---

## 3. PV plot

The shaded region between the full and intrinsic curves is the walk-away put value.
The separate walk-away put plot shows its value and delta across the full spot range,
and two features are worth noting.

**The put value peaks near S*, not deep OTM.**  In the OTM region the put value rises
steadily as spot increases: as the ASCOT moves closer to becoming exercisable, the
walk-away right also becomes more valuable — both the prospect of exercise and the
protection against not needing it grow together.  The value peaks near S* where the put
is approximately at-the-money, then declines as the ASCOT moves deeper in-the-money and
the probability of a credit event serious enough to matter before expiry falls.

**The put retains substantial value even deep in-the-money.**  For Kansai the put is
worth around 8 per 100 even at 145% parity.  The long maturity means there is always
meaningful time for a credit deterioration event to occur before the recall expiry.  The
market-convention intrinsic approximation ignores this entirely — it assigns zero value
to the walk-away right at every spot level — and that is the direct measure of the
approximation error.

---

## 4. Delta and Gamma

The walk-away put delta plot makes the delta story precise: the walk-away put delta is
positive in the OTM region, peaks near S*, then flips negative in the ITM region.  The
full ASCOT delta is the CB proxy delta plus this walk-away put delta at every point.

**OTM region.**  The CB proxy is zero, consistent with the intrinsic payoff being zero
when CB < R₀.  The full ASCOT carries positive delta because the walk-away put delta is
positive here: as spot rises toward S*, the walk-away put value rises (the ASCOT is
becoming more likely to be exercised profitably), so the put contributes positive delta
on top of the zero intrinsic.  The full ASCOT delta therefore leads the CB proxy well
before the exercise boundary.

**ITM region.**  Once the ASCOT crosses S*, the CB proxy jumps to the CB delta while the
full ASCOT transitions smoothly.  Deeper in-the-money, the full ASCOT delta falls below
the CB proxy because the walk-away put delta has now flipped negative.  The put is
increasingly out-of-the-money (CB >> R₀), and its residual value — which remains
positive but small due to the long maturity — shrinks slightly as spot rises further.
That small loss in put value for each unit of spot rise is the negative put delta, and it
directly subtracts from CB_delta to give the full ASCOT delta.  For Kansai this offset
is roughly −0.10 throughout the ITM region, which is why the full delta runs persistently
below the CB proxy by that margin.

**Why no crossover for Kansai.**  Near S*, the sign of the walk-away put delta is
flipping from positive to negative.  Whether the full ASCOT delta is above or below the
CB proxy just above S* depends on which side of zero the put delta lands immediately
after the crossing.  For Kansai, S* sits at about 79% of the conversion price, so the
CB already carries meaningful equity sensitivity at S*.  The put delta turns negative
immediately above S* and the full ASCOT delta is below the CB proxy from the start of
the ITM region with no crossover.  (A case where the put delta is still briefly positive
just above S*, causing a crossover, is shown in the Appendix.)

**Gamma.**  The full ASCOT gamma is positive and smooth across the spot range.  It peaks
near S*, where the ASCOT is approximately at-the-money as a call on the CB — ATM options
have their highest gamma — and fades as the walk-away put moves further out-of-the-money
deep in the ITM region.  The CB proxy gamma shows numerical noise near S* from finite
differencing of the step-function intrinsic; this has no economic content and should be
disregarded.

---

## 5. Vega

The full ASCOT vega always exceeds the CB proxy vega.  This follows from the
decomposition: since the walk-away put gains value when volatility rises (higher vol
implies fatter tails and a greater chance of a large adverse credit or equity move), it
contributes strictly positive vega.

In the **OTM region**, the CB proxy vega is zero while the full ASCOT carries the
walk-away put's vega.  In the **ITM region**, the CB proxy vega equals the CB standalone
vega, while the full ASCOT adds the walk-away put's vega on top.  The understatement by
the proxy grows with depth in-the-money: the CB's own vega declines steeply deep ITM
(the conversion option becomes nearly linear), while the walk-away put's vega declines
more slowly because the tail credit risk it protects against persists regardless of how
far in-the-money the ASCOT is.

The CB standalone vega is included on the plot to show how the full ASCOT relates to the
underlying instrument's own vol sensitivity.  For Kansai, the long-dated equity option
keeps the CB's vega material throughout the spot range.  In the OTM region, the ASCOT
only partially participates in the CB's moves (its delta-on-CB is less than 1), so it
captures less than the full CB vega; `vega_full < CB standalone` there.  Once the ASCOT
crosses into the ITM region, the walk-away put adds back positive vega and
`vega_full > CB standalone` resumes.  (For a short-dated CB where the conversion option
is near-dead at low spot, the relationship is different; see the Appendix.)

---

## 6. CS01

When credit spreads widen (λ rises), two effects act on the full ASCOT in opposite
directions.  The intrinsic erodes — the CB falls, reducing CB − R₀.  Simultaneously,
the walk-away put gains value — a wider spread raises the probability of a large adverse
credit move, making the right to walk away more valuable.  These effects partially or
fully offset each other, so the full ASCOT CS01 is substantially smaller in magnitude
than the CB proxy CS01.

The economic reason for the offset is structural: the ASCOT holder does not bear the
default loss the way a CB holder does.  If the issuer defaults, the ASCOT holder simply
does not exercise — there is no delivery obligation and no loss of principal.  The
walk-away right is exactly the mechanism that provides this insulation; it is **long**
the credit tail risk that the CB holder is short.

For Kansai, the cancellation is partial rather than complete.  The full CS01 is small and
negative — roughly 6% to 19% of the CB proxy in magnitude across the ITM range.  The CB
proxy overstates the true credit exposure by a factor of 5× to 17×.  Using it as a hedge
would create a credit position that the ASCOT does not actually carry.  (For a
short-dated instrument the two effects cancel almost exactly, leaving the full CS01
near zero across the entire spot range; see the Appendix.)

---

## 7. IR01

The ASCOT full IR01 has the **opposite sign** to the CB proxy IR01 in the ITM region.
This is the most consequential divergence between the two.

The CB proxy IR01 is large and negative in the ITM region, reflecting the CB's bond
duration: higher rates reduce the present value of the CB's coupon and principal cash
flows, and the intrinsic (CB − R₀) falls with the CB.  The full ASCOT IR01 is positive
throughout the ITM region.  Two channels drive this reversal, and both act in the same
direction.

**Walk-away put appreciation.** When rates rise, the CB falls (bond duration).  A
falling CB moves closer to R(t), the walk-away put's strike, making the put more
valuable.  The walk-away put is **long** the CB's rate sensitivity: it gains when rates
rise and the CB falls.  This positive contribution more than offsets the loss in intrinsic
value, reversing the sign of the total ASCOT IR01.

**Equity drift.** A higher risk-free rate raises the risk-neutral expected growth rate of
the equity.  A higher expected equity path raises the expected future CB value and
increases the probability of profitable exercise.  This benefits the ASCOT holder as an
option holder — it has no direct counterpart for a CB holder who already owns the
instrument regardless of its future path.

In the **OTM region**, the full ASCOT IR01 is also positive (the equity drift channel
already operates, raising the probability of future exercise), while the CB proxy is zero.

The consequence for hedging is direct: an ASCOT trader using the CB proxy IR01 would
establish a rate hedge in the wrong direction.  The full ASCOT is long rates; the CB is
short rates.  A hedge built on the CB proxy would double the rate exposure rather than
neutralise it.

---

## Appendix: Default Bundle — Contrasting Cases

The default bundle is a synthetic short-maturity coupon CB used primarily as a
calibration instrument for the QuantLib benchmark.  Its Greek profiles are qualitatively
consistent with the Kansai analysis but differ in three specific ways that are
instructive to note.

**Delta — crossover.**  For the default bundle, the full ASCOT delta briefly exceeds the
CB proxy delta just above S* before falling below it further in-the-money.  This
crossover occurs because S* lies well below the CB's own conversion price: at S*, the CB
is still bond-dominated and carries low equity delta.  The full ASCOT, however, has accumulated positive delta from the entire OTM region
through the walk-away put, and this accumulated delta entering S* exceeds the CB's low
delta there.  Just above S*, the walk-away put still has substantial value and its
residual shrinks only gradually as spot rises, so the offset to the intrinsic delta is
modest at first — producing a brief overshoot above the CB proxy.  Only further into the
ITM region, as the residual walk-away value shrinks more rapidly, does the full delta
fall below the CB proxy.  For Kansai no such overshoot occurs because the CB already
carries meaningful equity sensitivity at S*, so the offset to intrinsic delta outweighs
the accumulated OTM delta from the very start of the ITM region.

**Vega.**  Because the default bundle is short-dated, the CB's embedded conversion option
is near-dead at low spot values — CB vega is negligible in the OTM region.  Even the
modest walk-away put vega exceeds this near-zero CB vega, so the full ASCOT vega exceeds
the CB standalone vega across the entire spot range.  There is no region where
`vega_full < CB standalone`, in contrast to the Kansai OTM region where the long-dated
CB option keeps CB vega material and the ASCOT's partial participation leads to
`vega_full < CB standalone`.

**CS01.**  For the default bundle, the walk-away put's gain from a spread widening
cancels the intrinsic loss almost exactly.  The full CS01 is indistinguishable from zero
across the entire spot range: the ASCOT holder is effectively credit-neutral.  For
Kansai, the cancellation is only partial (full CS01 is 6% to 19% of the CB proxy in the
ITM region) because the longer maturity and lower hazard rate mean the walk-away put does
not gain as much from the same spread widening relative to the intrinsic loss.
