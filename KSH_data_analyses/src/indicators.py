"""Demográfiai és gazdasági mutatók (KPI-k) számítása."""

from __future__ import annotations

import numpy as np
import pandas as pd


def safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    """Osztás, ahol a 0 vagy hiányzó nevező eredménye NaN (nem hiba, nem végtelen)."""
    denominator = denominator.astype("float64").replace(0, np.nan)
    return numerator.astype("float64") / denominator


def yoy_pct(df: pd.DataFrame, column: str) -> pd.Series:
    """Éves változás %-ban. Csak egymást követő évek között számol, egyébként NaN."""
    ordered = df.sort_values("year")
    change = ordered[column].astype("float64").pct_change(fill_method=None) * 100
    consecutive = ordered["year"].diff() == 1
    return change.where(consecutive).reindex(df.index)


def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Kiszámítja a demográfiai és gazdasági mutatókat; új DataFrame-et ad vissza.

    Új oszlopok:
        working_age_ratio   – 15–64 évesek aránya a teljes népességben (%)
        elderly_ratio       – 65+ évesek aránya a teljes népességben (%)
        ageing_index        – 65+ évesek száma 100 fő 0–14 évesre
        population_15_64_yoy_pct – munkaképes korúak éves változása (%)
        gdp_yoy_pct         – reál GDP éves változása (%), ha van ``gdp`` oszlop
        gdp_per_capita      – reál GDP/fő (Ft, 2021-es láncolt áron), ha van ``gdp`` oszlop.
                              Közelítés: nevező a január 1-jei népesség (nem évközi átlag).
    A foglalkoztatási rátát nem számoljuk újra: a KSH hivatalos értékét használjuk.
    """
    result = df.copy()

    result["working_age_ratio"] = safe_divide(result["population_15_64"], result["total_population"]) * 100
    result["elderly_ratio"] = safe_divide(result["population_65_plus"], result["total_population"]) * 100
    result["ageing_index"] = safe_divide(result["population_65_plus"], result["population_0_14"]) * 100
    result["population_15_64_yoy_pct"] = yoy_pct(result, "population_15_64")

    if "gdp" in result.columns:
        result["gdp_yoy_pct"] = yoy_pct(result, "gdp")
        # gdp: millió Ft -> Ft/fő
        result["gdp_per_capita"] = safe_divide(result["gdp"] * 1_000_000, result["total_population"])

    return result
