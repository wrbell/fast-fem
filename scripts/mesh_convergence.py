#!/usr/bin/env python3
"""
Mesh Convergence Plotter

Reads a CSV of (element_count, result_value) pairs and produces a
publication-quality convergence plot.

Usage:
    python mesh_convergence.py data.csv --ylabel "Max Stress (MPa)" --title "Cantilever Beam"
    python mesh_convergence.py data.csv -o convergence.png

CSV format (with or without header):
    elements,stress
    500,98.2
    2000,112.5
    8000,118.3
    32000,119.1
"""

import argparse
import csv
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def read_csv(filepath: str) -> tuple[list[int], list[float]]:
    """Read element counts and result values from CSV."""
    elements = []
    values = []
    with open(filepath, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or row[0].strip().startswith("#"):
                continue
            try:
                elements.append(int(float(row[0].strip())))
                values.append(float(row[1].strip()))
            except (ValueError, IndexError):
                continue  # Skip header or malformed rows
    return elements, values


def plot_convergence(
    elements: list[int],
    values: list[float],
    ylabel: str = "Result Value",
    title: str = "Mesh Convergence Study",
    output: str | None = None,
    threshold: float = 2.0,
) -> None:
    """Generate mesh convergence plot."""
    elements = np.array(elements)
    values = np.array(values)

    # Sort by element count
    idx = np.argsort(elements)
    elements = elements[idx]
    values = values[idx]

    # Compute % change between successive refinements
    pct_changes = []
    for i in range(1, len(values)):
        pct = abs(values[i] - values[i - 1]) / abs(values[i - 1]) * 100
        pct_changes.append(pct)

    # Determine converged value (last value)
    converged = values[-1]

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.semilogx(elements, values, "bo-", markersize=8, linewidth=2, label="FEA Result")

    # Converged value line
    ax.axhline(
        y=converged,
        color="green",
        linestyle="--",
        alpha=0.7,
        label=f"Converged: {converged:.4g}",
    )

    # Annotate % changes
    for i, pct in enumerate(pct_changes):
        mid_x = np.sqrt(elements[i] * elements[i + 1])  # Geometric mean for log scale
        mid_y = (values[i] + values[i + 1]) / 2
        color = "green" if pct < threshold else "red"
        ax.annotate(
            f"{pct:.1f}%",
            xy=(mid_x, mid_y),
            fontsize=10,
            fontweight="bold",
            color=color,
            ha="center",
            va="bottom",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor=color, alpha=0.8),
        )

    # Mark converged points
    for i, pct in enumerate(pct_changes):
        if pct < threshold:
            ax.plot(
                elements[i + 1],
                values[i + 1],
                "gs",
                markersize=12,
                zorder=5,
                label=f"Converged (< {threshold}% change)" if i == next(j for j, p in enumerate(pct_changes) if p < threshold) else "",
            )

    ax.set_xlabel("Element Count", fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, which="both", alpha=0.3)
    ax.tick_params(labelsize=11)

    plt.tight_layout()

    if output:
        plt.savefig(output, dpi=150, bbox_inches="tight")
        print(f"Saved: {output}")
    else:
        plt.show()

    # Print summary table
    print(f"\n{'Elements':>10}  {'Result':>12}  {'% Change':>10}  {'Converged?':>10}")
    print("-" * 48)
    print(f"{elements[0]:>10d}  {values[0]:>12.4f}  {'—':>10}  {'—':>10}")
    for i, pct in enumerate(pct_changes):
        conv = "Yes" if pct < threshold else "No"
        print(f"{elements[i+1]:>10d}  {values[i+1]:>12.4f}  {pct:>9.1f}%  {conv:>10}")


def main():
    parser = argparse.ArgumentParser(description="Mesh convergence plotter")
    parser.add_argument("csv_file", help="CSV file with (element_count, result_value) pairs")
    parser.add_argument("--ylabel", "-y", default="Result Value", help="Y-axis label")
    parser.add_argument("--title", "-t", default="Mesh Convergence Study", help="Plot title")
    parser.add_argument("--output", "-o", default=None, help="Output PNG file (omit to show interactively)")
    parser.add_argument("--threshold", default=2.0, type=float, help="Convergence threshold in %% (default: 2.0)")
    args = parser.parse_args()

    if not Path(args.csv_file).exists():
        print(f"Error: {args.csv_file} not found", file=sys.stderr)
        sys.exit(1)

    elements, values = read_csv(args.csv_file)

    if len(elements) < 2:
        print("Error: Need at least 2 data points", file=sys.stderr)
        sys.exit(1)

    plot_convergence(elements, values, args.ylabel, args.title, args.output, args.threshold)


if __name__ == "__main__":
    main()
