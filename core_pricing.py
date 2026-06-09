"""Core config, grid, CB pricing, ASCOT pricing, and Greeks for the flat ASCOT toy."""

from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass, field, replace

import numpy as np


@dataclass
class MarketParams:
    r: float
    q: float
    sigma: float
    lam: float
    recovery_fraction: float
    stock_ticker: str | None = None
    stock_borrow_cost: float = 0.0
    valuation_date: str | None = None
    market_price: float | None = None
    share_price: float | None = None
    annual_dividend_yield: float | None = None
    dividend_type: str | None = None
    absolute_dividends: list[dict] | None = None


@dataclass
class CBParams:
    face: float
    conversion_ratio: float
    maturity: float
    coupon: float
    coupon_frequency_per_year: int
    call_price: float
    call_start_time: float
    put_price: float
    put_frequency_per_year: int
    put_start_time: float
    conversion_start_time: float = 0.0
    conversion_end_time: float | None = None
    ticker: str | None = None
    denomination: float | None = None
    issue_price: float | None = None
    market_price: float | None = None
    conversion_price: float | None = None
    valuation_date: str | None = None
    settlement_date: str | None = None
    coupon_pattern: str | None = None
    first_coupon_type: str | None = None
    coupon_dates: list[float] | None = None
    coupon_amounts: list[float] | None = None
    call_dates: list[float] | None = None
    put_dates: list[float] | None = None


@dataclass
class ASCOTParams:
    recall_price_start: float
    recall_price_end: float
    recall_expiry: float
    recall_price_model: str = "linear"
    swap_fixed_rate: float = 0.0
    swap_recall_spread: float = 0.0
    swap_discount_rate: float | None = None


@dataclass
class NumericsParams:
    S_max_multiple: float
    num_space_steps: int
    num_time_steps: int
    psor_omega: float
    psor_tol: float
    psor_max_iter: int
    theta: float


@dataclass
class PlotParams:
    spot_min: float
    spot_max: float
    spot_points: int
    bump_spot_rel: float
    bump_vol_abs: float


@dataclass
class SoftCallConfig:
    enabled: bool = False
    method: str = "one_touch_vol_adjusted"
    start_time: float | None = None
    trigger_multiple: float = 1.30
    reference_spot: float | None = None
    m: int = 20
    n: int = 30
    trading_days_per_year: int = 252
    vol_buffer_stddevs: float = 0.5


@dataclass
class OutputConfig:
    basis: str = "per_100"


@dataclass
class PricerConfig:
    coupon_paid_on_put: bool = True
    credit_model: str = "credit_spread"
    soft_call: SoftCallConfig = field(default_factory=SoftCallConfig)
    output: OutputConfig = field(default_factory=OutputConfig)


@dataclass
class Grid:
    x: np.ndarray
    S: np.ndarray
    dx: float
    t: np.ndarray
    dt: float
    coupon_step_amounts: dict
    put_steps: set
    call_active: np.ndarray
    conversion_active: np.ndarray


# Load market, CB, ASCOT, numerical, and plotting terms from JSON.
def load_terms(path: str):
    if os.path.isdir(path):
        return load_terms_from_dir(path)

    with open(path) as f:
        d = json.load(f)

    return _load_terms_from_combined_dict(d)


def load_terms_from_dir(directory: str):
    with open(os.path.join(directory, "market.json")) as f:
        market_dict = json.load(f)
    with open(os.path.join(directory, "cb_ascot.json")) as f:
        cb_dict = json.load(f)
    with open(os.path.join(directory, "numerics_plotting.json")) as f:
        rest_dict = json.load(f)

    if "cb" in cb_dict and "ascot" in cb_dict:
        cb_section = cb_dict["cb"]
        ascot_section = cb_dict["ascot"]
    else:
        cb_section = cb_dict
        ascot_section = cb_dict.get("ascot", {})

    ticker = cb_section.get("ticker") or cb_dict.get("ticker")
    market_section = market_dict.get("market") if "market" in market_dict else market_dict
    stocks = market_dict.get("stocks")
    if isinstance(stocks, dict) and stocks:
        stock_section = None
        if ticker and ticker in stocks:
            stock_section = stocks[ticker]
        elif len(stocks) == 1:
            stock_section = next(iter(stocks.values()))
        if stock_section is not None:
            market_section = {
                **market_section,
                "q": stock_section.get("q", market_section.get("q")),
                "sigma": stock_section.get("sigma", market_section.get("sigma")),
                "stock_ticker": ticker,
                "stock_borrow_cost": float(stock_section.get("stock_borrow_cost", 0.0)),
                "valuation_date": stock_section.get("valuation_date", market_dict.get("valuation_date")),
                "market_price": stock_section.get("market_price"),
                "share_price": stock_section.get("share_price"),
                "annual_dividend_yield": stock_section.get("annual_dividend_yield"),
                "dividend_type": stock_section.get("dividend_type"),
                "absolute_dividends": stock_section.get("absolute_dividends"),
            }

    return _load_terms_from_combined_dict({
        "market": market_section,
        "cb": cb_section,
        "ascot": ascot_section,
        "numerics": rest_dict["numerics"],
        "plotting": rest_dict["plotting"],
    })


def _load_terms_from_combined_dict(d: dict):
    market = _build_market_params(d["market"])
    cb = _build_cb_params(d["cb"])
    ascot = _build_ascot_params(d["ascot"])
    numerics = _build_numerics_params(d["numerics"])
    plot = _build_plot_params(d["plotting"])

    validate_terms(market, cb, ascot, numerics, plot)
    return market, cb, ascot, numerics, plot


def _optional_float_list(values):
    if values is None:
        return None
    return [float(v) for v in values]


def _build_market_params(m):
    return MarketParams(
        r=float(m["r"]),
        q=float(m["q"]),
        sigma=float(m["sigma"]),
        lam=float(m["lambda"]),
        recovery_fraction=float(m["recovery_fraction"]),
        stock_ticker=m.get("stock_ticker"),
        stock_borrow_cost=float(m.get("stock_borrow_cost", 0.0)),
        valuation_date=m.get("valuation_date"),
        market_price=None if m.get("market_price") is None else float(m["market_price"]),
        share_price=None if m.get("share_price") is None else float(m["share_price"]),
        annual_dividend_yield=(None if m.get("annual_dividend_yield") is None else float(m["annual_dividend_yield"])),
        dividend_type=m.get("dividend_type"),
        absolute_dividends=m.get("absolute_dividends"),
    )


def _build_cb_params(c):
    coupon_dates = _optional_float_list(c.get("coupon_dates"))
    coupon_amounts = _optional_float_list(c.get("coupon_amounts"))
    put_dates = _optional_float_list(c.get("put_dates"))
    call_dates = _optional_float_list(c.get("call_dates"))
    return CBParams(
        face=float(c["face"]),
        conversion_ratio=float(c["conversion_ratio"]),
        maturity=float(c["maturity"]),
        conversion_start_time=float(c.get("conversion_start_time", 0.0)),
        conversion_end_time=(None if c.get("conversion_end_time") is None else float(c["conversion_end_time"])),
        ticker=c.get("ticker"),
        denomination=(None if c.get("denomination") is None else float(c["denomination"])),
        issue_price=(None if c.get("issue_price") is None else float(c["issue_price"])),
        market_price=(None if c.get("market_price") is None else float(c["market_price"])),
        conversion_price=(None if c.get("conversion_price") is None else float(c["conversion_price"])),
        valuation_date=c.get("valuation_date"),
        settlement_date=c.get("settlement_date"),
        coupon=float(c["coupon"]),
        coupon_frequency_per_year=int(c["coupon_frequency_per_year"]),
        call_price=float(c["call_price"]),
        call_start_time=float(c["call_start_time"]),
        put_price=float(c["put_price"]),
        put_frequency_per_year=int(c["put_frequency_per_year"]),
        put_start_time=float(c["put_start_time"]),
        coupon_pattern=c.get("coupon_pattern"),
        first_coupon_type=c.get("first_coupon_type"),
        coupon_dates=coupon_dates,
        coupon_amounts=coupon_amounts,
        call_dates=call_dates,
        put_dates=put_dates,
    )


def _build_ascot_params(a):
    return ASCOTParams(
        recall_price_start=float(a["recall_price_start"]),
        recall_price_end=float(a["recall_price_end"]),
        recall_expiry=float(a["recall_expiry"]),
        recall_price_model=str(a.get("recall_price_model", "linear")),
        swap_fixed_rate=float(a.get("swap_fixed_rate", 0.0)),
        swap_recall_spread=float(a.get("swap_recall_spread", 0.0)),
        swap_discount_rate=None if a.get("swap_discount_rate") is None else float(a["swap_discount_rate"]),
    )


def _build_numerics_params(n):
    return NumericsParams(
        S_max_multiple=float(n["S_max_multiple"]),
        num_space_steps=int(n["num_space_steps"]),
        num_time_steps=int(n["num_time_steps"]),
        psor_omega=float(n["psor_omega"]),
        psor_tol=float(n["psor_tol"]),
        psor_max_iter=int(n["psor_max_iter"]),
        theta=float(n["theta"]),
    )


def _build_plot_params(p):
    return PlotParams(
        spot_min=float(p["spot_min"]),
        spot_max=float(p["spot_max"]),
        spot_points=int(p["spot_points"]),
        bump_spot_rel=float(p["bump_spot_rel"]),
        bump_vol_abs=float(p["bump_vol_abs"]),
    )


# Load optional pricer conventions such as credit model and soft-call settings.
def load_pricer_config(path: str | None = None) -> PricerConfig:
    if path is None:
        return PricerConfig()
    try:
        with open(path) as f:
            d = json.load(f)
    except FileNotFoundError:
        return PricerConfig()

    soft = d.get("soft_call", {})
    output = d.get("output", {})
    config = PricerConfig(
        coupon_paid_on_put=bool(d.get("coupon_paid_on_put", True)),
        credit_model=str(d.get("credit_model", "credit_spread")),
        soft_call=SoftCallConfig(
            enabled=bool(soft.get("enabled", False)),
            method=str(soft.get("method", "one_touch_vol_adjusted")),
            start_time=None if soft.get("start_time") is None else float(soft["start_time"]),
            trigger_multiple=float(soft.get("trigger_multiple", 1.30)),
            reference_spot=None if soft.get("reference_spot") is None else float(soft["reference_spot"]),
            m=int(soft.get("m", 20)),
            n=int(soft.get("n", 30)),
            trading_days_per_year=int(soft.get("trading_days_per_year", 252)),
            vol_buffer_stddevs=float(soft.get("vol_buffer_stddevs", 0.5)),
        ),
        output=OutputConfig(
            basis=str(output.get("basis", "per_100")),
        ),
    )
    validate_pricer_config(config)
    return config


# Validate economic terms and numerical settings before pricing.
def validate_terms(market, cb, ascot, numerics, plot):
    assert market.sigma > 0
    assert market.lam >= 0
    assert 0 <= market.recovery_fraction <= 1
    assert cb.maturity > 0
    assert cb.conversion_ratio > 0
    if cb.conversion_end_time is not None:
        assert 0 <= cb.conversion_start_time <= cb.conversion_end_time <= cb.maturity
    if cb.coupon_dates is not None:
        assert all(0 < d <= cb.maturity for d in cb.coupon_dates)
    if cb.coupon_amounts is not None:
        assert cb.coupon_dates is not None and len(cb.coupon_dates) == len(cb.coupon_amounts)
    if cb.put_dates is not None:
        assert all(0 < d <= cb.maturity for d in cb.put_dates)
    if cb.call_dates is not None:
        assert all(0 < d <= cb.maturity for d in cb.call_dates)
    assert ascot.recall_expiry <= cb.maturity
    assert ascot.recall_price_model in {"linear", "swap_pv"}
    assert numerics.num_space_steps >= 10
    assert numerics.num_time_steps >= 10
    assert 0 < numerics.theta <= 1
    conversion_price = cb.face / cb.conversion_ratio
    s_max = numerics.S_max_multiple * max(conversion_price, plot.spot_max)
    assert s_max > plot.spot_max


# Validate switches that affect pricer behavior rather than trade economics.
def validate_pricer_config(config):
    assert config.credit_model in {"credit_spread", "hazard_recovery"}
    assert config.soft_call.method in {"one_touch_vol_adjusted"}
    assert config.soft_call.trigger_multiple > 0
    assert config.soft_call.m > 0
    assert config.soft_call.n >= config.soft_call.m
    assert config.soft_call.trading_days_per_year > 0
    assert config.soft_call.vol_buffer_stddevs >= 0
    assert config.output.basis in {"per_100", "per_denomination"}


def output_scale_factor(cb: CBParams, pricer_config: PricerConfig) -> float:
    if pricer_config.output.basis == "per_denomination" and cb.denomination is not None:
        return cb.denomination / cb.face
    return 1.0


def scale_results_for_output(results: dict, scale_factor: float) -> dict:
    if abs(scale_factor - 1.0) < 1e-15:
        return results
    return {k: v * scale_factor for k, v in results.items()}


# Generate recurring event dates such as coupons or puts.
def periodic_dates(freq_per_year: int, maturity: float, start: float = 0.0):
    period = 1.0 / freq_per_year
    dates = []
    d = start + period
    while d <= maturity + 1e-10:
        dates.append(min(d, maturity))
        d += period
    return sorted(set(round(x, 10) for x in dates))


# Map continuous event dates to nearest discrete time-grid indices.
def snap_dates(dates, t_grid) -> set:
    return {int(np.argmin(np.abs(t_grid - d))) for d in dates}


def snap_date_amounts(dates, amounts, t_grid) -> dict:
    snapped = {}
    for d, amt in zip(dates, amounts):
        idx = int(np.argmin(np.abs(t_grid - d)))
        snapped[idx] = snapped.get(idx, 0.0) + float(amt)
    return snapped


# Build the shared log-spot and time grid plus snapped event indices.
def build_grid_full(market, cb, ascot, numerics, plot) -> Grid:
    m = numerics.num_space_steps
    n = numerics.num_time_steps
    conversion_price = cb.face / cb.conversion_ratio
    s_max = numerics.S_max_multiple * max(conversion_price, plot.spot_max)
    s_min = 0.01 * conversion_price
    x = np.linspace(np.log(s_min), np.log(s_max), m + 1)
    s = np.exp(x)
    t = np.linspace(0.0, cb.maturity, n + 1)
    if cb.coupon_dates is not None:
        coupon_dates = cb.coupon_dates
    else:
        coupon_dates = periodic_dates(cb.coupon_frequency_per_year, cb.maturity)
    if cb.coupon_amounts is not None:
        coupon_amounts = cb.coupon_amounts
    else:
        coupon_amounts = [cb.coupon / cb.coupon_frequency_per_year] * len(coupon_dates)
    if cb.put_dates is not None:
        put_dates = cb.put_dates
    else:
        put_dates = periodic_dates(cb.put_frequency_per_year, cb.maturity, cb.put_start_time)
    if cb.call_dates is not None:
        call_active = np.zeros(n + 1, dtype=bool)
        for idx in snap_dates(cb.call_dates, t):
            call_active[idx] = True
    else:
        call_active = t >= cb.call_start_time
    return Grid(
        x=x,
        S=s,
        dx=x[1] - x[0],
        t=t,
        dt=t[1] - t[0],
        coupon_step_amounts=snap_date_amounts(coupon_dates, coupon_amounts, t),
        put_steps=snap_dates(put_dates, t),
        call_active=call_active,
        conversion_active=(t >= cb.conversion_start_time)
        if cb.conversion_end_time is None
        else ((t >= cb.conversion_start_time) & (t <= cb.conversion_end_time + 1e-12)),
    )


# Build constant finite-difference coefficients for the log-spot PDE operator.
def build_L_coeffs(sigma: float, mu: float, disc: float, dx: float):
    alpha = sigma**2 / (2.0 * dx**2)
    beta = (mu - 0.5 * sigma**2) / (2.0 * dx)
    return alpha - beta, -2.0 * alpha - disc, alpha + beta


# Assemble one Crank-Nicolson tridiagonal system for a backward time step.
def build_cn_system(v_next, a, b, c, dt, theta, source_vec, m):
    rhs = np.zeros(m + 1)
    rhs[1:-1] = (
        (1.0 + (1.0 - theta) * dt * b) * v_next[1:-1]
        + (1.0 - theta) * dt * a * v_next[:-2]
        + (1.0 - theta) * dt * c * v_next[2:]
        + dt * source_vec[1:-1]
    )
    diag = np.full(m + 1, 1.0 - theta * dt * b)
    lower = np.full(m + 1, -theta * dt * a)
    upper = np.full(m + 1, -theta * dt * c)
    diag[0] = diag[m] = 1.0
    lower[0] = upper[0] = lower[m] = upper[m] = 0.0
    rhs[0] = rhs[m] = 0.0
    return diag, lower, upper, rhs


# Assemble a CN system when the discount rate varies by spot node.
def build_cn_system_variable_disc(v_next, a_no_disc, b_no_disc, c_no_disc, disc_vec, dt, theta, m):
    b = b_no_disc - disc_vec
    rhs = np.zeros(m + 1)
    rhs[1:-1] = (
        (1.0 + (1.0 - theta) * dt * b[1:-1]) * v_next[1:-1]
        + (1.0 - theta) * dt * a_no_disc * v_next[:-2]
        + (1.0 - theta) * dt * c_no_disc * v_next[2:]
    )
    diag = np.ones(m + 1)
    lower = np.zeros(m + 1)
    upper = np.zeros(m + 1)
    diag[1:-1] = 1.0 - theta * dt * b[1:-1]
    lower[1:-1] = -theta * dt * a_no_disc
    upper[1:-1] = -theta * dt * c_no_disc
    return diag, lower, upper, rhs


# Enforce linear extrapolation boundary conditions after a solve.
def apply_linearity_bc(v):
    v[0] = 2.0 * v[1] - v[2]
    v[-1] = 2.0 * v[-2] - v[-3]
    return v


# Solve an unconstrained tridiagonal system for auxiliary PDE states.
def solve_tridiagonal(diag, lower, upper, rhs):
    n = len(diag)
    c_prime = np.zeros(n)
    d_prime = np.zeros(n)
    c_prime[0] = upper[0] / diag[0]
    d_prime[0] = rhs[0] / diag[0]
    for i in range(1, n):
        denom = diag[i] - lower[i] * c_prime[i - 1]
        c_prime[i] = upper[i] / denom if i < n - 1 else 0.0
        d_prime[i] = (rhs[i] - lower[i] * d_prime[i - 1]) / denom
    x = np.zeros(n)
    x[-1] = d_prime[-1]
    for i in range(n - 2, -1, -1):
        x[i] = d_prime[i] - c_prime[i] * x[i + 1]
    return x


# Solve a lower-obstacle LCP, used for American exercise floors.
def psor_single_obstacle(diag, lower, upper, rhs, g_lower, v_init, omega, tol, max_iter):
    v = v_init.copy()
    m = len(v) - 1
    for _ in range(max_iter):
        max_change = 0.0
        for i in range(1, m):
            gs = (rhs[i] - lower[i] * v[i - 1] - upper[i] * v[i + 1]) / diag[i]
            y = v[i] + omega * (gs - v[i])
            y_proj = max(y, g_lower[i])
            max_change = max(max_change, abs(y_proj - v[i]))
            v[i] = y_proj
        if max_change < tol:
            break
    return v


# Solve a lower/upper-obstacle LCP, used for callable convertible caps.
def psor_double_obstacle(diag, lower, upper, rhs, g_lower, g_upper, v_init, omega, tol, max_iter):
    v = v_init.copy()
    m = len(v) - 1
    for _ in range(max_iter):
        max_change = 0.0
        for i in range(1, m):
            gs = (rhs[i] - lower[i] * v[i - 1] - upper[i] * v[i + 1]) / diag[i]
            y = v[i] + omega * (gs - v[i])
            y_proj = min(max(y, g_lower[i]), g_upper[i])
            max_change = max(max_change, abs(y_proj - v[i]))
            v[i] = y_proj
        if max_change < tol:
            break
    return v


# Evaluate the standard normal CDF elementwise for scalar/array inputs.
def norm_cdf(z):
    erf = np.vectorize(math.erf)
    return 0.5 * (1.0 + erf(z / math.sqrt(2.0)))


class CBPricer:
    # Initialize PDE coefficients and model-specific credit treatment.
    def __init__(self, market, cb, grid, theta=0.5, omega=1.2, tol=1e-8, max_iter=10000, pricer_config=None):
        self.market = market
        self.cb = cb
        self.grid = grid
        self.pricer_config = pricer_config or PricerConfig()
        self.theta = theta
        self.omega = omega
        self.tol = tol
        self.max_iter = max_iter

        sigma, lam, r, q = market.sigma, market.lam, market.r, market.q
        if self.pricer_config.credit_model == "hazard_recovery":
            mu_cb = r - q + lam
            disc_cb = r + lam
            self.source_scalar = lam * market.recovery_fraction * cb.face
        else:
            mu_cb = r - q
            disc_cb = r
            self.source_scalar = 0.0

        self.a, self.b, self.c = build_L_coeffs(sigma, mu_cb, disc_cb, grid.dx)
        self.no_disc_a, self.no_disc_b, self.no_disc_c = build_L_coeffs(sigma, r - q, 0.0, grid.dx)

    # Resolve the soft-call start time, defaulting to the hard-call start.
    def _soft_call_start_time(self):
        soft = self.pricer_config.soft_call
        return self.cb.call_start_time if soft.start_time is None else soft.start_time

    # Approximate m-out-of-n soft-call eligibility with a one-touch proxy.
    def _soft_call_probability(self, s, t):
        soft = self.pricer_config.soft_call
        if not soft.enabled or t < self._soft_call_start_time():
            return np.zeros_like(s)
        reference = soft.reference_spot or (self.cb.face / self.cb.conversion_ratio)
        window = soft.n / soft.trading_days_per_year
        sigma = self.market.sigma
        trigger = soft.trigger_multiple * reference
        if sigma <= 0:
            return (s >= trigger).astype(float)
        effective_trigger = trigger * math.exp(soft.vol_buffer_stddevs * sigma * math.sqrt(window))
        p = np.ones_like(s)
        below = s < effective_trigger
        if np.any(below):
            x = np.log(np.maximum(s[below], 1e-300))
            b = math.log(effective_trigger)
            mu = self.market.r - self.market.q - 0.5 * sigma * sigma
            vol_sqrt_t = sigma * math.sqrt(window)
            z1 = (x + mu * window - b) / vol_sqrt_t
            z2 = (x - mu * window - b) / vol_sqrt_t
            mirror = np.exp(2.0 * mu * (b - x) / (sigma * sigma))
            p[below] = norm_cdf(z1) + mirror * norm_cdf(z2)
        return np.clip(p, 0.0, 1.0)

    # Apply probability-weighted call-cap pressure when soft call is enabled.
    def _apply_soft_call_pressure(self, v, s, t):
        if not self.pricer_config.soft_call.enabled:
            return v
        p_soft = self._soft_call_probability(s, t)
        call_cap = np.maximum(self.cb.call_price, self.cb.conversion_ratio * s)
        v -= p_soft * np.maximum(v - call_cap, 0.0)
        return v

    # Build the full CB value surface under the selected credit model.
    def price_surface(self):
        if self.pricer_config.credit_model == "credit_spread":
            return self._price_surface_credit_spread()

        grid, cb = self.grid, self.cb
        m, n = len(grid.S) - 1, len(grid.t) - 1
        s, dt, theta = grid.S, grid.dt, self.theta
        kappa = cb.conversion_ratio
        coupon = cb.coupon / cb.coupon_frequency_per_year
        v_surface = np.zeros((n + 1, m + 1))
        v_surface[n] = np.maximum(kappa * s, cb.face + coupon)
        v = v_surface[n].copy()
        source_vec = np.full(m + 1, self.source_scalar)

        for step in range(n - 1, -1, -1):
            diag, lower, upper, rhs = build_cn_system(v, self.a, self.b, self.c, dt, theta, source_vec, m)
            g_lower = kappa * s
            if grid.call_active[step] and not self.pricer_config.soft_call.enabled:
                g_upper = np.maximum(cb.call_price, kappa * s)
                v_new = psor_double_obstacle(diag, lower, upper, rhs, g_lower, g_upper, v, self.omega, self.tol, self.max_iter)
            else:
                v_new = psor_single_obstacle(diag, lower, upper, rhs, g_lower, v, self.omega, self.tol, self.max_iter)
            apply_linearity_bc(v_new)
            self._apply_soft_call_pressure(v_new, s, grid.t[step])
            self._apply_put_coupon_events(v_new, step, coupon)
            v_surface[step] = v_new
            v = v_new
        return v_surface

    # Build the CB value surface using QuantLib-style TF spread discounting.
    def _price_surface_credit_spread(self):
        grid, cb, market = self.grid, self.cb, self.market
        m, n = len(grid.S) - 1, len(grid.t) - 1
        s, dt, theta = grid.S, grid.dt, self.theta
        kappa = cb.conversion_ratio
        coupon = cb.coupon / cb.coupon_frequency_per_year
        redemption = cb.face + coupon
        v_surface = np.zeros((n + 1, m + 1))
        v_surface[n] = np.maximum(kappa * s, redemption)
        v = v_surface[n].copy()
        p_conv = np.where(kappa * s >= redemption, 1.0, 0.0)

        for step in range(n - 1, -1, -1):
            p_diag, p_low, p_up, p_rhs = build_cn_system(
                p_conv, self.no_disc_a, self.no_disc_b, self.no_disc_c, dt, theta, np.zeros(m + 1), m
            )
            p_new = solve_tridiagonal(p_diag, p_low, p_up, p_rhs)
            apply_linearity_bc(p_new)
            np.clip(p_new, 0.0, 1.0, out=p_new)
            disc_vec = market.r + market.lam * (1.0 - p_new)
            diag, lower, upper, rhs = build_cn_system_variable_disc(
                v, self.no_disc_a, self.no_disc_b, self.no_disc_c, disc_vec, dt, theta, m
            )
            g_lower = kappa * s
            if grid.call_active[step] and not self.pricer_config.soft_call.enabled:
                g_upper = np.maximum(cb.call_price, kappa * s)
                v_new = psor_double_obstacle(diag, lower, upper, rhs, g_lower, g_upper, v, self.omega, self.tol, self.max_iter)
            else:
                g_upper = None
                v_new = psor_single_obstacle(diag, lower, upper, rhs, g_lower, v, self.omega, self.tol, self.max_iter)
            apply_linearity_bc(v_new)
            self._apply_soft_call_pressure(v_new, s, grid.t[step])
            p_new[v_new <= kappa * s + 1e-8] = 1.0
            if g_upper is not None:
                called = np.abs(v_new - g_upper) <= 1e-7
                p_new[called & (kappa * s >= cb.call_price)] = 1.0
            self._apply_put_coupon_events(v_new, step, coupon)
            v_surface[step] = v_new
            v, p_conv = v_new, p_new
        return v_surface

    # Apply put and coupon jumps in the configured event order.
    def _apply_put_coupon_events(self, v, step, coupon):
        coupon_amount = self.grid.coupon_step_amounts.get(step)
        if self.pricer_config.coupon_paid_on_put:
            if step in self.grid.put_steps:
                np.maximum(v, self.cb.put_price, out=v)
            if coupon_amount is not None:
                v += coupon_amount
        else:
            if coupon_amount is not None:
                v += coupon_amount
            if step in self.grid.put_steps:
                np.maximum(v, self.cb.put_price, out=v)

    # Interpolate the t=0 CB price at a requested spot.
    def price_at_spot(self, s0, surface):
        return float(np.interp(s0, self.grid.S, surface[0]))


class ASCOTPricer:
    # Initialize ASCOT PDE coefficients and precompute the recall schedule.
    def __init__(self, market, ascot, grid, cb_surface, cb=None, theta=0.5, omega=1.2, tol=1e-8, max_iter=10000):
        self.market = market
        self.ascot = ascot
        self.cb = cb
        self.grid = grid
        self.cb_surface = cb_surface
        self.R0 = ascot.recall_price_start
        self.RT = ascot.recall_price_end
        self.T_rec = ascot.recall_expiry
        self.theta = theta
        self.omega = omega
        self.tol = tol
        self.max_iter = max_iter
        self.a, self.b, self.c = build_L_coeffs(market.sigma, market.r - market.q, market.r, grid.dx)
        self.source_vec = np.zeros(len(grid.S))
        self.recall_prices = self._build_recall_price_grid()

    # Generate CB coupon dates needed by the swap-PV recall model.
    def _coupon_dates(self):
        if self.cb is None:
            return []
        if self.cb.coupon_dates is not None:
            return sorted(set(round(float(x), 10) for x in self.cb.coupon_dates))
        return periodic_dates(self.cb.coupon_frequency_per_year, self.cb.maturity)

    # Compute swap-based recall price from future net asset-swap cashflows.
    def _swap_recall_price(self, t):
        if self.cb is None:
            raise ValueError("swap_pv recall_price_model requires cb terms")
        discount = self.market.r if self.ascot.swap_discount_rate is None else self.ascot.swap_discount_rate
        pay_rate = self.ascot.swap_fixed_rate + self.ascot.swap_recall_spread
        net_amount_per_year = self.cb.coupon - self.cb.face * pay_rate
        pv_net = 0.0
        prev = t
        for pay_date in self._coupon_dates():
            if pay_date <= t + 1e-12:
                continue
            accrual = pay_date - prev
            pv_net += net_amount_per_year * accrual * np.exp(-discount * (pay_date - t))
            prev = pay_date
        return self.cb.face + pv_net

    # Compute recall price directly before time-grid interpolation.
    def _raw_recall_price(self, t):
        if self.ascot.recall_price_model == "swap_pv":
            return self._swap_recall_price(t)
        if self.T_rec <= 0:
            return self.RT
        return self.R0 + (self.RT - self.R0) * t / self.T_rec

    # Precompute recall prices at every pricing time node.
    def _build_recall_price_grid(self):
        return np.array([self._raw_recall_price(float(t)) for t in self.grid.t])

    # Read or interpolate recall price for an arbitrary time.
    def recall_price(self, t):
        return float(np.interp(t, self.grid.t, self.recall_prices))

    # Build the ASCOT American option value surface backward from recall expiry.
    def price_surface(self):
        grid, t_arr = self.grid, self.grid.t
        m = len(grid.S) - 1
        n_rec = int(np.argmin(np.abs(t_arr - self.T_rec)))
        r_t = self.recall_prices[n_rec]
        a_init = np.maximum(self.cb_surface[n_rec] - r_t, 0.0)
        a_surface = np.zeros((n_rec + 1, m + 1))
        a_surface[n_rec] = a_init
        a = a_init.copy()
        for step in range(n_rec - 1, -1, -1):
            diag, lower, upper, rhs = build_cn_system(a, self.a, self.b, self.c, grid.dt, self.theta, self.source_vec, m)
            g_lower = self.cb_surface[step] - self.recall_prices[step]
            a_new = psor_single_obstacle(diag, lower, upper, rhs, g_lower, a, self.omega, self.tol, self.max_iter)
            apply_linearity_bc(a_new)
            a_surface[step] = a_new
            a = a_new
        return a_surface

    # Interpolate full ASCOT value at t=0 for a requested spot.
    def price_full(self, s0, a_surface):
        return float(np.interp(s0, self.grid.S, a_surface[0]))

    # Compute immediate exercise value at t=0 using the active recall model.
    def price_intrinsic(self, s0, cb_at_s0):
        return max(cb_at_s0 - self.recall_price(0.0), 0.0)


# Build coupled CB and ASCOT surfaces for a given market state.
def build_surfaces(market, cb, ascot, numerics, plot, pricer_config=None):
    grid = build_grid_full(market, cb, ascot, numerics, plot)
    cb_pricer = CBPricer(
        market, cb, grid, theta=numerics.theta, omega=numerics.psor_omega,
        tol=numerics.psor_tol, max_iter=numerics.psor_max_iter, pricer_config=pricer_config
    )
    cb_surf = cb_pricer.price_surface()
    asc_pricer = ASCOTPricer(
        market, ascot, grid, cb_surf, cb=cb, theta=numerics.theta,
        omega=numerics.psor_omega, tol=numerics.psor_tol, max_iter=numerics.psor_max_iter
    )
    a_surf = asc_pricer.price_surface()
    return grid, cb_surf, a_surf, asc_pricer


# Read CB, full ASCOT, and intrinsic ASCOT values from prebuilt surfaces.
def read_pv(s0, grid, cb_surf, a_surf, asc_pricer):
    cb_pv = float(np.interp(s0, grid.S, cb_surf[0]))
    return cb_pv, asc_pricer.price_full(s0, a_surf), asc_pricer.price_intrinsic(s0, cb_pv)


# Convert log-space finite differences into spot delta and gamma arrays.
def grid_delta_gamma(v0, s, dx):
    v_x = np.gradient(v0, dx)
    v_xx = np.gradient(v_x, dx)
    return v_x / s, (v_xx - v_x) / s**2


# Compute PV, delta, gamma, and vega across a spot sweep.
def compute_all_greeks_sweep(spots, market, cb, ascot, numerics, plot, pricer_config=None):
    print("Building base surfaces...")
    grid, cb_surf, a_surf, asc_pricer = build_surfaces(market, cb, ascot, numerics, plot, pricer_config)
    s, dx = grid.S, grid.dx
    r0 = asc_pricer.recall_price(0.0)
    intr_v0 = np.maximum(cb_surf[0] - r0, 0.0)
    delta_cb_grid, gamma_cb_grid = grid_delta_gamma(cb_surf[0], s, dx)
    delta_full_grid, gamma_full_grid = grid_delta_gamma(a_surf[0], s, dx)
    delta_intr_grid, gamma_intr_grid = grid_delta_gamma(intr_v0, s, dx)

    dv = plot.bump_vol_abs
    print("Building vol-up surfaces for vega...")
    mkt_up = replace(market, sigma=market.sigma + dv)
    grid_u, cb_surf_u, a_surf_u, _ = build_surfaces(mkt_up, cb, ascot, numerics, plot, pricer_config)
    print("Building vol-down surfaces for vega...")
    mkt_dn = replace(market, sigma=market.sigma - dv)
    grid_d, cb_surf_d, a_surf_d, _ = build_surfaces(mkt_dn, cb, ascot, numerics, plot, pricer_config)
    cb_vega_grid = (cb_surf_u[0] - cb_surf_d[0]) / (2.0 * dv)
    full_vega_grid = (a_surf_u[0] - a_surf_d[0]) / (2.0 * dv)
    intr_vega_grid = (np.maximum(cb_surf_u[0] - r0, 0.0) - np.maximum(cb_surf_d[0] - r0, 0.0)) / (2.0 * dv)

    # IR01: bump r for both CB and recall-value discounting
    dr = 1e-4
    print("Building rate-up surfaces for IR01...")
    asc_up = replace(
        ascot,
        swap_discount_rate=(None if ascot.swap_discount_rate is None else ascot.swap_discount_rate + dr),
    )
    _, cb_surf_r_u, a_surf_r_u, asc_r_u = build_surfaces(
        replace(market, r=market.r + dr), cb, asc_up, numerics, plot, pricer_config
    )
    print("Building rate-down surfaces for IR01...")
    asc_dn = replace(
        ascot,
        swap_discount_rate=(None if ascot.swap_discount_rate is None else ascot.swap_discount_rate - dr),
    )
    _, cb_surf_r_d, a_surf_r_d, asc_r_d = build_surfaces(
        replace(market, r=market.r - dr), cb, asc_dn, numerics, plot, pricer_config
    )
    cb_ir01_grid = (cb_surf_r_u[0] - cb_surf_r_d[0]) / (2.0 * dr)
    full_ir01_grid = (a_surf_r_u[0] - a_surf_r_d[0]) / (2.0 * dr)
    r0_u = asc_r_u.recall_price(0.0)
    r0_d = asc_r_d.recall_price(0.0)
    intr_ir01_grid = (np.maximum(cb_surf_r_u[0] - r0_u, 0.0) - np.maximum(cb_surf_r_d[0] - r0_d, 0.0)) / (2.0 * dr)

    # CS01: bump lambda as credit spread proxy
    dcs = 1e-4
    print("Building spread-up surfaces for CS01...")
    _, cb_surf_cs_u, a_surf_cs_u, asc_cs_u = build_surfaces(
        replace(market, lam=market.lam + dcs), cb, ascot, numerics, plot, pricer_config
    )
    print("Building spread-down surfaces for CS01...")
    _, cb_surf_cs_d, a_surf_cs_d, asc_cs_d = build_surfaces(
        replace(market, lam=market.lam - dcs), cb, ascot, numerics, plot, pricer_config
    )
    cb_cs01_grid = (cb_surf_cs_u[0] - cb_surf_cs_d[0]) / (2.0 * dcs)
    full_cs01_grid = (a_surf_cs_u[0] - a_surf_cs_d[0]) / (2.0 * dcs)
    r0_cs_u = asc_cs_u.recall_price(0.0)
    r0_cs_d = asc_cs_d.recall_price(0.0)
    intr_cs01_grid = (np.maximum(cb_surf_cs_u[0] - r0_cs_u, 0.0) - np.maximum(cb_surf_cs_d[0] - r0_cs_d, 0.0)) / (2.0 * dcs)

    results = {k: np.zeros(len(spots)) for k in [
        "cb_pv", "ascot_full", "ascot_intr", "delta_cb", "delta_full", "delta_intr",
        "gamma_cb", "gamma_full", "gamma_intr", "vega_cb", "vega_full", "vega_intr",
        "ir01_cb", "ir01_full", "ir01_intr", "cs01_cb", "cs01_full", "cs01_intr"
    ]}
    print(f"Reading off Greeks at {len(spots)} spots...")
    for i, s0 in enumerate(spots):
        cb0, af0, ai0 = read_pv(s0, grid, cb_surf, a_surf, asc_pricer)
        results["cb_pv"][i], results["ascot_full"][i], results["ascot_intr"][i] = cb0, af0, ai0
        results["delta_cb"][i] = np.interp(s0, s, delta_cb_grid)
        results["delta_full"][i] = np.interp(s0, s, delta_full_grid)
        results["delta_intr"][i] = np.interp(s0, s, delta_intr_grid)
        results["gamma_cb"][i] = np.interp(s0, s, gamma_cb_grid)
        results["gamma_full"][i] = np.interp(s0, s, gamma_full_grid)
        results["gamma_intr"][i] = np.interp(s0, s, gamma_intr_grid)
        results["vega_cb"][i] = np.interp(s0, s, cb_vega_grid)
        results["vega_full"][i] = np.interp(s0, s, full_vega_grid)
        results["vega_intr"][i] = np.interp(s0, s, intr_vega_grid)
        results["ir01_cb"][i] = np.interp(s0, s, cb_ir01_grid)
        results["ir01_full"][i] = np.interp(s0, s, full_ir01_grid)
        results["ir01_intr"][i] = np.interp(s0, s, intr_ir01_grid)
        results["cs01_cb"][i] = np.interp(s0, s, cb_cs01_grid)
        results["cs01_full"][i] = np.interp(s0, s, full_cs01_grid)
        results["cs01_intr"][i] = np.interp(s0, s, intr_cs01_grid)
    return results
