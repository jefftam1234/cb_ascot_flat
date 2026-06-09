"""QuantLib regression tests for the flat ASCOT toy."""

from __future__ import annotations

import os
from dataclasses import replace

import numpy as np

from core_pricing import (
    CBPricer,
    build_grid_full,
    load_pricer_config,
    load_terms,
    periodic_dates,
)


BASE_DIR = os.path.dirname(__file__)
DEFAULT_TERMS = os.path.join(BASE_DIR, "json", "default")
DEFAULT_CONFIG = os.path.join(BASE_DIR, "json", "default", "pricer_config.json")


def require_quantlib():
    try:
        import QuantLib as ql
    except ImportError as exc:
        raise RuntimeError("Install QuantLib with `python -m pip install QuantLib`.") from exc
    return ql


def ql_date_from_year_fraction(ql, reference_date, t):
    return reference_date + int(round(365.0 * t))


class QuantLibCBPricer:
    def __init__(self, market, cb, numerics, reference_date=None, engine_type="crr"):
        self.ql = require_quantlib()
        self.market = market
        self.cb = cb
        self.numerics = numerics
        self.engine_type = engine_type
        self.reference_date = reference_date or self.ql.Date(1, 1, 2026)
        self.day_counter = self.ql.Actual365Fixed()
        self.calendar = self.ql.NullCalendar()

    def price(self, spot):
        bond = self._build_bond()
        bond.setPricingEngine(self._build_engine(spot))
        return float(bond.NPV())

    def price_many(self, spots):
        return np.array([self.price(float(s)) for s in spots])

    def _build_bond(self):
        ql = self.ql
        ql.Settings.instance().evaluationDate = self.reference_date
        cb = self.cb
        issue = self.reference_date
        maturity = ql_date_from_year_fraction(ql, issue, cb.maturity)
        exercise_start = ql_date_from_year_fraction(ql, issue, cb.conversion_start_time)
        exercise_end = ql_date_from_year_fraction(ql, issue, cb.conversion_end_time if cb.conversion_end_time is not None else cb.maturity)
        exercise = ql.AmericanExercise(exercise_start, exercise_end)
        callability = self._build_callability_schedule()
        schedule, coupons = self._build_coupon_schedule()
        return ql.ConvertibleFixedCouponBond(
            exercise, cb.conversion_ratio, callability, issue, 0, coupons,
            self.day_counter, schedule, cb.face
        )

    def _build_coupon_schedule(self):
        ql = self.ql
        cb = self.cb
        dates = [self.reference_date]
        if cb.coupon_dates is not None:
            coupon_dates = cb.coupon_dates
        else:
            coupon_dates = periodic_dates(cb.coupon_frequency_per_year, cb.maturity)
        for t in coupon_dates:
            dates.append(ql_date_from_year_fraction(ql, self.reference_date, t))
        schedule = ql.Schedule(
            dates, self.calendar, ql.Unadjusted, ql.Unadjusted, ql.Period(),
            ql.DateGeneration.Forward, False
        )
        if cb.coupon_amounts is not None:
            coupon_amounts = cb.coupon_amounts
        else:
            coupon_amounts = [cb.coupon / cb.coupon_frequency_per_year] * (len(dates) - 1)
        coupons = []
        for (start, end), coupon_amount in zip(zip(dates[:-1], dates[1:]), coupon_amounts):
            accrual = self.day_counter.yearFraction(start, end)
            coupons.append(coupon_amount / (cb.face * accrual))
        return schedule, coupons

    def _build_callability_schedule(self):
        ql = self.ql
        cb = self.cb
        schedule = ql.CallabilitySchedule()
        if cb.call_dates is not None:
            call_dates = cb.call_dates
        else:
            grid_times = np.linspace(0.0, cb.maturity, self.numerics.num_time_steps + 1)
            call_dates = [float(t) for t in grid_times if cb.call_start_time <= t < cb.maturity - 1e-12]
        for t in call_dates:
            if t < cb.maturity - 1e-12:
                schedule.append(
                    ql.Callability(
                        ql.BondPrice(cb.call_price, ql.BondPrice.Dirty),
                        ql.Callability.Call,
                        ql_date_from_year_fraction(ql, self.reference_date, float(t)),
                    )
                )
        if cb.put_dates is not None:
            put_dates = cb.put_dates
        else:
            put_dates = periodic_dates(cb.put_frequency_per_year, cb.maturity, cb.put_start_time)
        for t in put_dates:
            if t < cb.maturity - 1e-12:
                schedule.append(
                    ql.Callability(
                        ql.BondPrice(cb.put_price, ql.BondPrice.Dirty),
                        ql.Callability.Put,
                        ql_date_from_year_fraction(ql, self.reference_date, t),
                    )
                )
        return schedule

    def _build_engine(self, spot):
        ql = self.ql
        market = self.market
        ref = self.reference_date
        spot_handle = ql.QuoteHandle(ql.SimpleQuote(float(spot)))
        dividend_ts = ql.YieldTermStructureHandle(ql.FlatForward(ref, market.q, self.day_counter))
        risk_free_ts = ql.YieldTermStructureHandle(ql.FlatForward(ref, market.r, self.day_counter))
        vol_ts = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(ref, self.calendar, market.sigma, self.day_counter))
        process = ql.BlackScholesMertonProcess(spot_handle, dividend_ts, risk_free_ts, vol_ts)
        credit_spread = ql.QuoteHandle(ql.SimpleQuote(market.lam))
        return ql.BinomialConvertibleEngine(process, self.engine_type, self.numerics.num_time_steps, credit_spread)


def without_default_credit(market):
    return replace(market, lam=0.0, recovery_fraction=0.0)


def feature_variant(cb, *, coupon=True, put=True, call=True):
    variant = replace(cb)
    if not coupon:
        variant.coupon = 0.0
        if variant.coupon_dates is not None:
            if variant.coupon_amounts is None:
                variant.coupon_amounts = [0.0] * len(variant.coupon_dates)
            else:
                variant.coupon_amounts = [0.0] * len(variant.coupon_amounts)
    if not put:
        variant.put_start_time = cb.maturity + 1.0
        variant.put_dates = []
    if not call:
        variant.call_start_time = cb.maturity + 1.0
        variant.call_dates = []
    return variant


def local_cb_prices(spots, market, cb, ascot, numerics, plot, pricer_config):
    grid = build_grid_full(market, cb, ascot, numerics, plot)
    pricer = CBPricer(
        market, cb, grid, theta=numerics.theta, omega=numerics.psor_omega,
        tol=numerics.psor_tol, max_iter=numerics.psor_max_iter,
        pricer_config=pricer_config,
    )
    surface = pricer.price_surface()
    return np.array([pricer.price_at_spot(float(s), surface) for s in spots])


def assert_close_to_quantlib(name, spots, market, cb, ascot, numerics, plot, pricer_config, max_abs_tol, mean_abs_tol):
    local = local_cb_prices(spots, market, cb, ascot, numerics, plot, pricer_config)
    quantlib = QuantLibCBPricer(market, cb, numerics).price_many(spots)
    diff = np.abs(local - quantlib)
    max_abs = float(diff.max())
    mean_abs = float(diff.mean())
    print(f"{name}: max_abs={max_abs:.6f} (tol {max_abs_tol:.6f}), mean_abs={mean_abs:.6f} (tol {mean_abs_tol:.6f})")
    assert max_abs <= max_abs_tol, f"{name} max_abs {max_abs} > {max_abs_tol}"
    assert mean_abs <= mean_abs_tol, f"{name} mean_abs {mean_abs} > {mean_abs_tol}"


def run_quantlib_regression(terms_path=DEFAULT_TERMS, config_path=DEFAULT_CONFIG):
    market, cb, ascot, numerics, plot = load_terms(terms_path)
    pricer_config = replace(load_pricer_config(config_path), credit_model="credit_spread")
    pricer_config.output.basis = "per_100"
    spots = np.linspace(plot.spot_min, plot.spot_max, plot.spot_points)

    assert_close_to_quantlib(
        "default credit_spread full term sheet",
        spots, market, cb, ascot, numerics, plot, pricer_config,
        max_abs_tol=0.04, mean_abs_tol=0.01,
    )
    assert_close_to_quantlib(
        "risk-free full term sheet",
        spots, without_default_credit(market), cb, ascot, numerics, plot, pricer_config,
        max_abs_tol=0.02, mean_abs_tol=0.005,
    )
    assert_close_to_quantlib(
        "credit-only no coupon/call/put",
        spots, market, feature_variant(cb, coupon=False, call=False, put=False),
        ascot, numerics, plot, pricer_config,
        max_abs_tol=0.08, mean_abs_tol=0.025,
    )
    print("PASS: QuantLib regression checks")


if __name__ == "__main__":
    run_quantlib_regression()
