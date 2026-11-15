"""Adattisztítás. Minden függvény másolaton dolgozik, a bemenetet nem módosítja.

Fontos: hiányzó statisztikai adatot NEM töltünk ki nullával – a hiány nem nulla.
"""

from __future__ import annotations

import pandas as pd


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Oszlopnevek egységesítése: kisbetű, szóköz/kötőjel -> aláhúzás."""
    result = df.copy()
    result.columns = (
        result.columns.str.strip().str.lower().str.replace(r"[\s\-]+", "_", regex=True)
    )
    return result


def report_quality(df: pd.DataFrame, name: str = "") -> None:
    """Rövid adatminőségi jelentés kiírása: sorok, hiányzó értékek, duplikált évek."""
    print(f"--- {name} ---")
    print(f"Sorok: {len(df)}, évek: {df['year'].min()}–{df['year'].max()}")
    missing = df.isna().sum()
    print("Hiányzó értékek:", missing[missing > 0].to_dict() or "nincs")
    print("Duplikált évek:", int(df["year"].duplicated().sum()))


def _to_numeric(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Év és numerikus oszlopok konvertálása; ami nem szám, NaN lesz (és jelezzük)."""
    result = df.copy()
    result["year"] = pd.to_numeric(result["year"], errors="coerce").astype("Int64")
    for col in columns:
        converted = pd.to_numeric(result[col], errors="coerce")
        bad = converted.isna() & result[col].notna()
        if bad.any():
            print(f"FIGYELEM: {col}: {int(bad.sum())} nem numerikus érték NaN-ra cserélve.")
        result[col] = converted
    return result


def _drop_empty_and_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Teljesen üres sorok és teljes sor-duplikátumok eltávolítása (jelezve)."""
    before = len(df)
    result = df.dropna(how="all").drop_duplicates()
    result = result[result["year"].notna()]
    if len(result) != before:
        print(f"Eltávolítva {before - len(result)} üres / duplikált / év nélküli sor.")
    if result["year"].duplicated().any():
        raise ValueError("Ugyanaz az év többször szerepel eltérő értékekkel – ellenőrizd a forrást!")
    return result.sort_values("year").reset_index(drop=True)


def clean_population_data(df: pd.DataFrame) -> pd.DataFrame:
    """Demográfiai adatok tisztítása és ellenőrzése.

    Ellenőrzi, hogy nincs negatív érték, és hogy a három korcsoport összege
    egyezik-e a teljes népességgel (eltérés esetén figyelmeztet, nem javít).
    """
    value_cols = ["total_population", "population_0_14", "population_15_64", "population_65_plus"]
    result = _drop_empty_and_duplicates(_to_numeric(normalize_columns(df), value_cols))

    if (result[value_cols] < 0).any().any():
        print("FIGYELEM: negatív népességérték található!")

    age_sum = result[["population_0_14", "population_15_64", "population_65_plus"]].sum(axis=1, min_count=3)
    diff = (age_sum - result["total_population"]).abs()
    if (diff > 0).any():
        print("FIGYELEM: a korcsoportok összege eltér a teljes népességtől ezekben az években:",
              result.loc[diff > 0, "year"].tolist())
    return result


def clean_economic_data(df: pd.DataFrame) -> pd.DataFrame:
    """Gazdasági és foglalkoztatási adatok tisztítása.

    Minden ``year``-en kívüli numerikusra alakítható oszlopot számmá konvertál;
    a ``obs_status``-hoz hasonló szöveges oszlopokat érintetlenül hagyja.
    Százalékos oszlopnál (``*_rate``) jelzi a 0–100 tartományon kívüli értéket.
    """
    result = normalize_columns(df)
    value_cols = [c for c in result.columns if c != "year" and c != "obs_status"]
    result = _drop_empty_and_duplicates(_to_numeric(result, value_cols))

    for col in value_cols:
        if col.endswith("_rate") and not result[col].dropna().between(0, 100).all():
            print(f"FIGYELEM: {col} oszlopban 0–100 tartományon kívüli érték van!")
        elif (result[col] < 0).any():
            print(f"FIGYELEM: {col} oszlopban negatív érték van!")
    return result
