"""Adatbetöltés: egyszerű CSV/JSON olvasás és a nyers KSH-formátumok átalakítása
egyszerű, év szerinti táblákká (ugyanaz a séma, mint a mintaadatoké)."""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd

from config import settings


def _check_exists(filepath: Path) -> Path:
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(
            f"A fájl nem található: {filepath}\n"
            "Tipp: futtasd a letöltő cellát (USE_SAMPLE_DATA = False), "
            "vagy használd a mintaadatokat (USE_SAMPLE_DATA = True)."
        )
    return filepath


def load_csv(filepath: Path, **kwargs) -> pd.DataFrame:
    """CSV fájl betöltése DataFrame-be (alapértelmezés: UTF-8)."""
    kwargs.setdefault("encoding", "utf-8")
    return pd.read_csv(_check_exists(filepath), **kwargs)


def load_json(filepath: Path):
    """JSON fájl betöltése UTF-8 kódolással."""
    with open(_check_exists(filepath), encoding="utf-8") as f:
        return json.load(f)


# --- Nyers KSH-fájlok -> egyszerű táblák -------------------------------------

# Az SDMX AGE kódok és a projekt oszlopnevei közötti megfeleltetés
POPULATION_AGE_CODES = {
    "TOTAL": "total_population",
    "Y_LT15": "population_0_14",
    "Y15-64": "population_15_64",
    "Y_GE65": "population_65_plus",
}


def load_ksh_population(filepath: Path) -> pd.DataFrame:
    """A KSH HVD népesség-CSV (január 1., nem/kor/állampolgárság) átalakítása.

    Szűrés: mindkét nem (SEX=T), összes állampolgárság (CITIZEN=TOTAL), Magyarország.
    A forrás ':' jele a hiányzó értéket jelöli -> NaN.
    """
    raw = load_csv(filepath, sep=";", na_values=[":"], dtype={"VALUES": "float64"})
    subset = raw[
        (raw["SEX"] == "T")
        & (raw["CITIZEN"] == "TOTAL")
        & (raw["GEO"] == "HU")
        & (raw["AGE"].isin(POPULATION_AGE_CODES))
    ]
    table = subset.pivot(index="TIME", columns="AGE", values="VALUES").rename(columns=POPULATION_AGE_CODES)
    table = table.reset_index().rename(columns={"TIME": "year"})
    table.columns.name = None
    return table[["year", *POPULATION_AGE_CODES.values()]]


def load_ksh_gdp_sdmx(filepath: Path) -> pd.DataFrame:
    """Reál GDP kinyerése a NAMAIN_T01GDP_A SDMX (compact XML) állományból.

    Kiválasztott idősor: STO=B1GQ (GDP), PRICES=L (láncolt volumen, 2021-es referenciaév),
    UNIT_MEASURE=XDC (forint), UNIT_MULT=6 (millió) -> ``gdp`` oszlop millió Ft-ban.
    """
    root = ET.parse(_check_exists(filepath)).getroot()
    rows = []
    for series in root.iter():
        if (
            series.tag.endswith("Series")
            and series.get("STO") == "B1GQ"
            and series.get("PRICES") == "L"
            and series.get("UNIT_MEASURE") == "XDC"
            and series.get("REF_AREA") == "HU"
        ):
            for obs in series:
                rows.append(
                    {
                        "year": int(obs.get("TIME_PERIOD")),
                        "gdp": float(obs.get("OBS_VALUE")),
                        "obs_status": obs.get("OBS_STATUS"),  # A = végleges, P = előzetes
                    }
                )
    return pd.DataFrame(rows).sort_values("year").reset_index(drop=True)


def load_ksh_employment_stadat(filepath: Path) -> pd.DataFrame:
    """Foglalkoztatási ráta (15–64 évesek, %) a STADAT 20.1.1.3 táblából.

    A tábla blokkokban tartalmazza az "Együtt", "Férfi", "Nő" adatokat;
    csak az "Együtt" blokkot vesszük. Tizedesjel: vessző.
    """
    raw = load_csv(filepath, sep=";", skiprows=1, encoding=settings.STADAT_ENCODING, dtype=str)
    first_col = raw.columns[0]  # "Év"
    labels = raw[first_col].str.strip()

    start = labels.index[labels == "Együtt"][0] + 1
    block = raw.loc[start:]
    # a blokk az első nem-évszám soráig tart (pl. "Férfi")
    is_year = block[first_col].str.strip().str.fullmatch(r"\d{4}")
    end = is_year.idxmin() if not is_year.all() else block.index[-1] + 1
    block = raw.loc[start : end - 1]

    rate_col = [c for c in raw.columns if c.startswith("Foglalkoztatási ráta")][0]
    return pd.DataFrame(
        {
            "year": block[first_col].astype(int).to_numpy(),
            "employment_rate": block[rate_col].str.replace(",", ".").astype(float).to_numpy(),
        }
    )
