"""Output tables and plots for the flat ASCOT toy."""

from __future__ import annotations

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from core_pricing import (
    compute_all_greeks_sweep,
    load_pricer_config,
    load_terms,
    output_scale_factor,
    scale_results_for_output,
)


BASE_DIR = os.path.dirname(__file__)
DEFAULT_TERMS = os.path.join(BASE_DIR, "json", "default")
DEFAULT_CONFIG = os.path.join(BASE_DIR, "json", "default", "pricer_config.json")
DEFAULT_OUTPUT = os.path.join(BASE_DIR, "output")


# Infer the output bundle name from an input bundle path.
def bundle_name_from_terms_path(terms_path):
    bundle = os.path.basename(os.path.normpath(terms_path))
    if bundle == "kansai_paint":
        return "kansai"
    if bundle in {"default", "kansai"}:
        return bundle
    return bundle or "default"


# Build the final bundle-specific output directory.
def bundle_output_dir(output_base_dir, bundle_name):
    return os.path.join(output_base_dir, bundle_name)


def swap_recall_price_0(cb, ascot, market):
    discount = market.r if ascot.swap_discount_rate is None else ascot.swap_discount_rate
    pay_rate = ascot.swap_fixed_rate + ascot.swap_recall_spread
    net_amount_per_year = cb.coupon - cb.face * pay_rate
    pv_net = 0.0
    period = 1.0 / cb.coupon_frequency_per_year
    t = period
    prev = 0.0
    while t <= cb.maturity + 1e-10:
        pay_date = min(t, cb.maturity)
        accrual = pay_date - prev
        pv_net += net_amount_per_year * accrual * np.exp(-discount * pay_date)
        prev = pay_date
        t += period
    return cb.face + pv_net


def setup_ax(ax, title, xlabel, ylabel):
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend()


def spot_for_cb_level(spots, cb_values, target_level):
    """Return interpolated spot where CB value crosses target_level."""
    diffs = cb_values - target_level
    if np.all(diffs < 0) or np.all(diffs > 0):
        return None

    exact_idx = np.where(np.isclose(diffs, 0.0, atol=1e-12))[0]
    if exact_idx.size > 0:
        return float(spots[exact_idx[0]])

    sign_change_idx = np.where(diffs[:-1] * diffs[1:] < 0)[0]
    if sign_change_idx.size == 0:
        return None

    i = int(sign_change_idx[0])
    x0, x1 = float(spots[i]), float(spots[i + 1])
    y0, y1 = float(cb_values[i]), float(cb_values[i + 1])
    if np.isclose(y1, y0):
        return x0
    return x0 + (target_level - y0) * (x1 - x0) / (y1 - y0)


def plot_all(spots, results, cb, ascot, market, output_dir=DEFAULT_OUTPUT, value_scale=1.0):
    os.makedirs(output_dir, exist_ok=True)
    kappa = cb.conversion_ratio
    conv_line = value_scale * kappa * spots
    r0 = (
        ascot.recall_price_start
        if ascot.recall_price_model == "linear"
        else swap_recall_price_0(cb, ascot, market)
    )
    recall_level = value_scale * r0
    recall_spot = spot_for_cb_level(spots, results["cb_pv"], recall_level)
    recall_label = "linear R0" if ascot.recall_price_model == "linear" else "swap R(0)"

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(spots, results["ascot_full"], label="ASCOT full (American)", color="steelblue", lw=2)
    ax.plot(spots, results["ascot_intr"], label=f"ASCOT intrinsic (CB - {recall_label}={r0:.2f})", color="darkorange", lw=2, ls="--")
    gap = results["ascot_full"] - results["ascot_intr"]
    ax.fill_between(spots, results["ascot_intr"], results["ascot_full"], where=gap > 0.01, alpha=0.15, color="steelblue", label="Time value")
    ax.axhline(0, color="black", lw=0.5)
    if recall_spot is not None:
        ax.axvline(recall_spot, color="black", lw=1, ls=":", label=f"S* where CB = R0 ({recall_spot:.1f})")
    setup_ax(ax, "ASCOT PV vs Initial Spot", "Spot S0", "PV")
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "plot_pv.png"), dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(spots, results["delta_full"], label="ASCOT full Delta", color="steelblue", lw=2)
    ax.plot(spots, results["delta_intr"], label="ASCOT intrinsic Delta", color="darkorange", lw=2, ls="--")
    ax.plot(spots, results["delta_cb"], label="ASCOT CB Proxy [Delta]", color="seagreen", lw=2, ls="-.")
    ax.axhline(0, color="black", lw=0.5)
    if recall_spot is not None:
        ax.axvline(recall_spot, color="black", lw=1, ls=":", label=f"S* where CB = R0 ({recall_spot:.1f})")
    setup_ax(ax, "ASCOT Delta vs Initial Spot", "Spot S0", "Delta")
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "plot_delta.png"), dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(spots, results["gamma_full"], label="ASCOT full Gamma", color="steelblue", lw=2)
    ax.plot(spots, results["gamma_intr"], label="ASCOT intrinsic Gamma", color="darkorange", lw=2, ls="--")
    ax.plot(spots, results["gamma_cb"], label="ASCOT CB Proxy [Gamma]", color="seagreen", lw=2, ls="-.")
    ax.axhline(0, color="black", lw=0.5)
    if recall_spot is not None:
        ax.axvline(recall_spot, color="black", lw=1, ls=":", label=f"S* where CB = R0 ({recall_spot:.1f})")
    setup_ax(ax, "ASCOT Gamma vs Initial Spot", "Spot S0", "Gamma")
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "plot_gamma.png"), dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(spots, results["vega_full"], label="ASCOT full Vega", color="steelblue", lw=2)
    ax.plot(spots, results["vega_intr"], label="ASCOT intrinsic Vega", color="darkorange", lw=2, ls="--")
    ax.plot(spots, results["vega_cb"], label="ASCOT CB Proxy [Vega]", color="seagreen", lw=2, ls="-.")
    ax.axhline(0, color="black", lw=0.5)
    if recall_spot is not None:
        ax.axvline(recall_spot, color="black", lw=1, ls=":", label=f"S* where CB = R0 ({recall_spot:.1f})")
    setup_ax(ax, "ASCOT Vega vs Initial Spot", "Spot S0", "Vega")
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "plot_vega.png"), dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(spots, results["ir01_full"], label="ASCOT full IR01", color="steelblue", lw=2)
    ax.plot(spots, results["ir01_intr"], label="ASCOT intrinsic IR01", color="darkorange", lw=2, ls="--")
    ax.plot(spots, results["ir01_cb"], label="ASCOT CB Proxy [IR01]", color="seagreen", lw=2, ls="-.")
    ax.axhline(0, color="black", lw=0.5)
    if recall_spot is not None:
        ax.axvline(recall_spot, color="black", lw=1, ls=":", label=f"S* where CB = R0 ({recall_spot:.1f})")
    setup_ax(ax, "ASCOT IR01 vs Initial Spot", "Spot S0", "IR01 (dPV/dr)")
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "plot_ir01.png"), dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(spots, results["cs01_full"], label="ASCOT full CS01", color="steelblue", lw=2)
    ax.plot(spots, results["cs01_intr"], label="ASCOT intrinsic CS01", color="darkorange", lw=2, ls="--")
    ax.plot(spots, results["cs01_cb"], label="ASCOT CB Proxy [CS01]", color="seagreen", lw=2, ls="-.")
    ax.axhline(0, color="black", lw=0.5)
    if recall_spot is not None:
        ax.axvline(recall_spot, color="black", lw=1, ls=":", label=f"S* where CB = R0 ({recall_spot:.1f})")
    setup_ax(ax, "ASCOT CS01 vs Initial Spot", "Spot S0", "CS01 (dPV/dlambda)")
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "plot_cs01.png"), dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(spots, results["cb_pv"], label="CB price", color="green", lw=2)
    ax.plot(spots, conv_line, label=f"Conversion value", color="gray", lw=1.5, ls=":")
    bond_floor = value_scale * cb.face * np.exp(-(market.r + market.lam) * cb.maturity)
    ax.axhline(bond_floor, color="brown", lw=1, ls="--", label=f"Bond floor ref ({bond_floor:.1f})")
    ax.axhline(value_scale * cb.call_price, color="red", lw=1, ls="-.", label=f"Call price ({value_scale * cb.call_price:.0f})")
    ax.axhline(value_scale * cb.put_price, color="purple", lw=1, ls="-.", label=f"Put price ({value_scale * cb.put_price:.0f})")
    ax.axhline(recall_level, color="navy", lw=1, ls="--", label=f"Initial recall R0 ({recall_level:.0f})")
    if recall_spot is not None:
        ax.axvline(recall_spot, color="black", lw=1, ls=":", label=f"S* where CB = R0 ({recall_spot:.1f})")
    setup_ax(ax, "CB Price vs Spot", "Spot S0", "CB Price")
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "plot_cb.png"), dpi=150)
    plt.close(fig)

    for name in [
        "plot_pv.png", "plot_delta.png", "plot_gamma.png", "plot_vega.png",
        "plot_ir01.png", "plot_cs01.png", "plot_cb.png"
    ]:
        print(f"Saved {os.path.join(output_dir, name)}")


def print_table(spots, results, n_points=8):
    idx = np.round(np.linspace(0, len(spots) - 1, n_points)).astype(int)
    print(f"\n{'S0':>8}  {'CB PV':>8}  {'ASCOT full':>11}  {'ASCOT intr':>11}  {'Delta full':>11}  {'Vega full':>10}")
    print("-" * 78)
    for i in idx:
        print(
            f"{spots[i]:8.1f}  {results['cb_pv'][i]:8.3f}  "
            f"{results['ascot_full'][i]:11.3f}  {results['ascot_intr'][i]:11.3f}  "
            f"{results['delta_full'][i]:11.4f}  {results['vega_full'][i]:10.3f}"
        )


RESULTS_FILENAME = "results.npz"


def save_results(output_dir, spots, results, scale_factor):
    """Persist Greeks sweep results so plots can be regenerated without repricing."""
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, RESULTS_FILENAME)
    np.savez(path, spots=spots, scale_factor=np.float64(scale_factor), **results)
    print(f"Saved numerical results to: {path}")


def load_results(output_dir):
    """Load previously saved Greeks sweep results. Returns (spots, results, scale_factor)."""
    path = os.path.join(output_dir, RESULTS_FILENAME)
    data = np.load(path)
    spots = data["spots"]
    scale_factor = float(data["scale_factor"])
    result_keys = [k for k in data.files if k not in ("spots", "scale_factor")]
    results = {k: data[k] for k in result_keys}
    print(f"Loaded numerical results from: {path}")
    return spots, results, scale_factor


def run(terms_path=DEFAULT_TERMS, pricer_config_path=DEFAULT_CONFIG, output_dir=DEFAULT_OUTPUT, bundle_name=None):
    bundle_name = bundle_name or bundle_name_from_terms_path(terms_path)
    final_output_dir = bundle_output_dir(output_dir, bundle_name)
    print(f"Loading terms from: {terms_path}")
    market, cb, ascot, numerics, plot = load_terms(terms_path)
    print(f"Loading pricer config from: {pricer_config_path}")
    print(f"Output bundle: {bundle_name}")
    print(f"Output directory: {final_output_dir}")
    pricer_config = load_pricer_config(pricer_config_path)
    spots = np.linspace(plot.spot_min, plot.spot_max, plot.spot_points)

    print("\n=== Computing Greeks sweep ===")
    results_raw = compute_all_greeks_sweep(spots, market, cb, ascot, numerics, plot, pricer_config)
    scale_factor = output_scale_factor(cb, pricer_config)
    results = scale_results_for_output(results_raw, scale_factor)

    print("\n=== Correctness checks ===")
    print("PASS: ASCOT full >= intrinsic everywhere" if np.all(results_raw["ascot_full"] >= results_raw["ascot_intr"] - 1e-6) else "FAIL: ASCOT full < intrinsic")
    print("PASS: ASCOT PV >= 0 everywhere" if np.all(results_raw["ascot_full"] >= -1e-6) else "FAIL: negative ASCOT PV")
    print("PASS: CB PV >= conversion value (kappa S) everywhere" if np.all(results_raw["cb_pv"] >= cb.conversion_ratio * spots - 0.05) else "FAIL: CB below conversion value")

    print_table(spots, results)
    save_results(final_output_dir, spots, results, scale_factor)
    print("\n=== Generating plots ===")
    plot_all(spots, results, cb, ascot, market, final_output_dir, value_scale=scale_factor)
    print(f"\nDone. Plots saved in: {final_output_dir}")


def run_plots_only(terms_path=DEFAULT_TERMS, pricer_config_path=DEFAULT_CONFIG, output_dir=DEFAULT_OUTPUT, bundle_name=None):
    """Regenerate plots from cached results.npz without repricing."""
    bundle_name = bundle_name or bundle_name_from_terms_path(terms_path)
    final_output_dir = bundle_output_dir(output_dir, bundle_name)
    print(f"Loading terms from: {terms_path}")
    print(f"Pricer config: {pricer_config_path} (not used in replot mode)")
    market, cb, ascot, _, _ = load_terms(terms_path)
    spots, results, scale_factor = load_results(final_output_dir)
    print("\n=== Regenerating plots from cached results ===")
    plot_all(spots, results, cb, ascot, market, final_output_dir, value_scale=scale_factor)
    print(f"\nDone. Plots saved in: {final_output_dir}")


if __name__ == "__main__":
    terms_file = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_TERMS
    config_file = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_CONFIG
    out_dir = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_OUTPUT
    bundle = sys.argv[4] if len(sys.argv) > 4 else None
    run(terms_file, config_file, out_dir, bundle)
