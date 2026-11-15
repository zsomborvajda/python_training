"""Központi projektbeállítások: útvonalak, API-címek, fájlnevek."""

from pathlib import Path

# A projekt gyökere: a config/ mappa szülőkönyvtára (nem függ a munkakönyvtártól)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Könyvtárak
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
SAMPLE_DIR = DATA_DIR / "sample_data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
CHART_DIR = OUTPUT_DIR / "charts"

# --- KSH "Nagy értékű adatkészletek" API (dokumentáció: https://data.ksh.hu/dokumentacio)
KSH_API_BASE_URL = "https://data.ksh.hu"
REQUEST_TIMEOUT = 60  # másodperc; a népesség-CSV ~12 MB

# Népesség – HVD dataset és disztribúció (ellenőrizve: 2026-11-15, datasets.json + metadata.rdf)
POPULATION_DATASET_ID = "f44d314b-bc27-40a7-b34e-af01b3c4ab05"  # "HVD - Népesség"
# "Population on 1 January by sex, age and citizenship" (CSV)
POPULATION_DISTRIBUTION_ID = "5c5c1828-8599-4b96-8b9f-ef6c27ab7c82"

# GDP – HVD dataset és disztribúció
GDP_DATASET_ID = "93a05949-b058-477f-a02d-0fdb024b503f"  # "HVD - Nemzeti számlák – a GDP főbb éves aggregátumai"
# "GDP and main components ... – annual (NAMAIN_T01GDP_A)" (SDMX XML)
GDP_DISTRIBUTION_ID = "bd19297c-4446-4f1e-85de-577a17389793"

# --- Foglalkoztatás: KSH STADAT 20.1.1.3 (nem az API része, letölthető CSV)
EMPLOYMENT_STADAT_URL = "https://www.ksh.hu/stadat_files/mun/hu/mun0003.csv"
STADAT_ENCODING = "cp1250"  # a STADAT CSV-k Windows-1250 kódolásúak

# Vizsgált időszak kezdete (szűrés a letöltött adatokon; az API nem kezel év-paramétert)
START_YEAR = 2000

# Fájlnevek
RAW_POPULATION_FILE = RAW_DIR / "ksh_population_by_age_citizenship.csv"
RAW_GDP_FILE = RAW_DIR / "ksh_gdp_namain_t01gdp_a.xml"
RAW_EMPLOYMENT_FILE = RAW_DIR / "ksh_stadat_mun0003.csv"
RAW_DATASETS_FILE = RAW_DIR / "ksh_datasets.json"
SOURCE_METADATA_FILE = RAW_DIR / "source_metadata.json"

SAMPLE_POPULATION_FILE = SAMPLE_DIR / "population_sample.csv"
SAMPLE_EMPLOYMENT_FILE = SAMPLE_DIR / "employment_sample.csv"
SAMPLE_GDP_FILE = SAMPLE_DIR / "gdp_sample.csv"

PROCESSED_FILE = PROCESSED_DIR / "hungary_indicators.csv"
