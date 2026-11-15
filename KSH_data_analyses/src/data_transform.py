"""Az adatforrások év szerinti összekapcsolása egy elemzési táblába."""

from __future__ import annotations

import pandas as pd


def _year_range(df: pd.DataFrame) -> str:
    return f"{df['year'].min()}–{df['year'].max()} ({df['year'].nunique()} év)"


def merge_datasets(
    population: pd.DataFrame, employment: pd.DataFrame, gdp: pd.DataFrame
) -> pd.DataFrame:
    """Összekapcsolja az adatforrásokat év szerint.

    Join-választás: **left join a népességi táblára**. A demográfia az elsődleges
    adatkör, ezért minden demográfiai év megmarad; ahol a foglalkoztatási vagy
    GDP-adat hiányzik, ott NaN szerepel (nem dobunk el csendben éveket).
    A népességi időszakon kívül eső gazdasági évek kimaradnak – ezt kiírjuk.
    """
    sources = {"population": population, "employment": employment, "gdp": gdp}

    # 1) Ellenőrzések: egyedi év-kulcs, éves granularitás (egész évszámok)
    for name, df in sources.items():
        if df["year"].duplicated().any():
            raise ValueError(f"A(z) {name} táblában ismétlődő év van – éves granularitás szükséges.")
        print(f"{name:<11} {_year_range(df)}")

    # 2) Összekapcsolás
    merged = (
        population.merge(employment, on="year", how="left")
        .merge(gdp, on="year", how="left")
        .sort_values("year")
        .reset_index(drop=True)
    )

    # 3) Átláthatóság: mi maradt ki / hol hiányzik adat
    pop_years = set(population["year"])
    for name in ("employment", "gdp"):
        df = sources[name]
        dropped = sorted(set(df["year"]) - pop_years)
        missing = sorted(pop_years - set(df["year"]))
        if dropped:
            print(f"  {name}: a népességi időszakon kívül, nem kerül be ({len(dropped)} év): {dropped}")
        if missing:
            print(f"  {name}: hiányzik ezekre a népességi évekre (NaN): {missing}")

    print(f"Elemzési tábla: {_year_range(merged)}")
    return merged
