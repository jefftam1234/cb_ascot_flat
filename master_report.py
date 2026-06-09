"""Build report-ready validation tables and plot snippets for the flat package."""

from __future__ import annotations

import argparse
import os
from dataclasses import replace

import numpy as np

from core_pricing import load_pricer_config, load_terms, output_scale_factor
from output_plotting import run as run_plots, run_plots_only
from testing import QuantLibCBPricer, local_cb_prices


BASE_DIR = os.path.dirname(__file__)
INPUT_DIR = os.path.join(BASE_DIR, "json")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
REPORT_DIR = os.path.join(BASE_DIR, "report_material")

PLOT_FILES = [
    "plot_pv.png",
    "plot_delta.png",
    "plot_gamma.png",
    "plot_vega.png",
    "plot_ir01.png",
    "plot_cs01.png",
    "plot_cb.png",
]


# Return canonical input and output bundle names.
def bundle_paths():
    return {
        "default": os.path.join(INPUT_DIR, "default"),
        "kansai": os.path.join(INPUT_DIR, "kansai_paint"),
    }


# Generate all plot PNGs into output/<bundle>/. Pass replot_only=True to skip pricing.
def generate_bundle_plots(replot_only=False):
    fn = run_plots_only if replot_only else run_plots
    for bundle, input_path in bundle_paths().items():
        config_path = os.path.join(input_path, "pricer_config.json")
        fn(input_path, config_path, OUTPUT_DIR, bundle)


# Compute local and QuantLib CB PVs for the default validation bundle.
def quantlib_comparison_data():
    terms_path = os.path.join(INPUT_DIR, "default")
    config_path = os.path.join(terms_path, "pricer_config.json")
    market, cb, ascot, numerics, plot = load_terms(terms_path)
    pricer_config = load_pricer_config(config_path)
    pricer_config.output.basis = "per_100"
    pricer_config = replace(pricer_config, credit_model="credit_spread")

    spots = np.linspace(plot.spot_min, plot.spot_max, plot.spot_points)
    local = local_cb_prices(spots, market, cb, ascot, numerics, plot, pricer_config)
    quantlib = QuantLibCBPricer(market, cb, numerics).price_many(spots)
    scale = output_scale_factor(cb, pricer_config)
    return spots, local * scale, quantlib * scale


# Build summary error statistics for report text.
def error_stats(local, quantlib):
    error = local - quantlib
    abs_error = np.abs(error)
    rel_error = abs_error / np.maximum(np.abs(quantlib), 1e-12)
    return {
        "mean_error": float(error.mean()),
        "mean_abs_error": float(abs_error.mean()),
        "rmse": float(np.sqrt(np.mean(error**2))),
        "max_abs_error": float(abs_error.max()),
        "max_rel_error_pct": float(100.0 * rel_error.max()),
    }


# Select a readable subset of spot rows for the LaTeX comparison table.
def sampled_rows(spots, local, quantlib, n_rows=10):
    indices = np.linspace(0, len(spots) - 1, min(n_rows, len(spots)), dtype=int)
    rows = []
    for idx in indices:
        rows.append((spots[idx], local[idx], quantlib[idx], local[idx] - quantlib[idx]))
    return rows


# Write a LaTeX table comparing local CB PV with QuantLib CB PV.
def write_quantlib_table(path, spots, local, quantlib):
    rows = sampled_rows(spots, local, quantlib)
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{Convertible bond PV validation against QuantLib}",
        r"\begin{tabular}{rrrr}",
        r"\hline",
        r"Spot & Local PV & QuantLib PV & Difference \\",
        r"\hline",
    ]
    for spot, local_pv, ql_pv, diff in rows:
        lines.append(f"{spot:.2f} & {local_pv:.6f} & {ql_pv:.6f} & {diff:+.6f} \\\\")
    lines.extend([
        r"\hline",
        r"\end{tabular}",
        r"\end{table}",
        "",
    ])
    with open(path, "w") as f:
        f.write("\n".join(lines))


# Write a short LaTeX-ready validation paragraph with aggregate error metrics.
def write_quantlib_summary(path, stats):
    text = (
        "The finite-difference CB implementation was benchmarked against "
        "QuantLib's binomial convertible-bond engine under the TF credit-spread "
        "configuration. Across the spot grid, the average signed error was "
        f"{stats['mean_error']:+.6f}, the mean absolute error was "
        f"{stats['mean_abs_error']:.6f}, the RMSE was {stats['rmse']:.6f}, "
        f"and the maximum absolute error was {stats['max_abs_error']:.6f}. "
        f"The maximum relative error was {stats['max_rel_error_pct']:.4f}\\%."
    )
    with open(path, "w") as f:
        f.write(text + "\n")


# Write LaTeX includegraphics snippets using default/ and kansai/ subfolders.
def write_includegraphics_snippets(path):
    lines = []
    for bundle in ["default", "kansai"]:
        lines.append(f"% {bundle} plots")
        for plot_file in PLOT_FILES:
            stem = os.path.splitext(plot_file)[0].replace("plot_", "")
            lines.extend([
                r"\begin{figure}[htbp]",
                r"\centering",
                f"\\includegraphics[width=0.90\\textwidth]{{18_modelassum/{bundle}/{plot_file}}}",
                f"\\caption{{{bundle.capitalize()} {stem.upper()} plot}}",
                f"\\label{{fig:{bundle}-{stem}}}",
                r"\end{figure}",
                "",
            ])
    with open(path, "w") as f:
        f.write("\n".join(lines))


# Run plot generation and write all report material files.
def run(replot_only=False):
    os.makedirs(REPORT_DIR, exist_ok=True)
    generate_bundle_plots(replot_only=replot_only)
    spots, local, quantlib = quantlib_comparison_data()
    stats = error_stats(local, quantlib)
    write_quantlib_table(os.path.join(REPORT_DIR, "quantlib_regression_table.tex"), spots, local, quantlib)
    write_quantlib_summary(os.path.join(REPORT_DIR, "quantlib_regression_summary.tex"), stats)
    write_includegraphics_snippets(os.path.join(REPORT_DIR, "includegraphics_snippets.tex"))
    print(f"Report material saved in: {REPORT_DIR}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build ASCOT report material.")
    parser.add_argument(
        "--replot-only",
        action="store_true",
        help="Skip pricing; load cached results.npz from each output bundle and regenerate plots only.",
    )
    args = parser.parse_args()
    run(replot_only=args.replot_only)
