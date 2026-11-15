"""Diagramok. Minden függvény PNG-be ment és visszaadja a Figure-t (notebookban megjelenik)."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")


def _save(fig: plt.Figure, output_dir: Path, filename: str) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / filename
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"Mentve: {path}")
    return path


def plot_population_by_age(df: pd.DataFrame, output_dir: Path) -> plt.Figure:
    """Korcsoportos népesség idősora (millió fő)."""
    labels = {
        "population_0_14": "0–14 évesek",
        "population_15_64": "15–64 évesek",
        "population_65_plus": "65+ évesek",
    }
    fig, ax = plt.subplots(figsize=(10, 5))
    for col, label in labels.items():
        ax.plot(df["year"], df[col] / 1e6, marker="o", label=label)
    ax.set_title("Magyarország népessége korcsoportok szerint (január 1.)")
    ax.set_xlabel("Év")
    ax.set_ylabel("Népesség (millió fő)")
    ax.legend()
    _save(fig, output_dir, "population_by_age.png")
    return fig


def plot_ageing_index(df: pd.DataFrame, output_dir: Path) -> plt.Figure:
    """Öregedési index idősora, 100-as referencia-vonallal."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["year"], df["ageing_index"], marker="o", color="tab:red", label="Öregedési index")
    ax.axhline(100, color="grey", linestyle="--", label="100 = annyi idős, ahány gyermek")
    ax.set_title("Öregedési index (65+ évesek 100 fő 0–14 évesre)")
    ax.set_xlabel("Év")
    ax.set_ylabel("65+ / 0–14 × 100")
    ax.legend()
    _save(fig, output_dir, "ageing_index.png")
    return fig


def plot_economy_and_employment(df: pd.DataFrame, output_dir: Path) -> plt.Figure:
    """Foglalkoztatási ráta és reál GDP két külön panelen.

    Eltérő mértékegységek miatt nem scatter és nem közös tengely: a két idősor
    együttmozgása önmagában nem bizonyít ok-okozati kapcsolatot.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    ax1.plot(df["year"], df["employment_rate"], marker="o", color="tab:green")
    ax1.set_title("Foglalkoztatási ráta, 15–64 évesek (%)")
    ax1.set_ylabel("%")

    ax2.plot(df["year"], df["gdp"] / 1000, marker="o", color="tab:blue")
    ax2.set_title("Reál GDP (láncolt volumen, 2021-es referenciaév)")
    ax2.set_ylabel("Milliárd Ft")
    ax2.set_xlabel("Év")

    fig.suptitle("Foglalkoztatás és gazdasági teljesítmény – együttmozgás, nem ok-okozat", y=1.0)
    fig.tight_layout()
    _save(fig, output_dir, "economy_and_employment.png")
    return fig
