# Hungary Demographic & Economic Insights

Oktatási célú (kb. 150 perces) Python-projekt: KSH-adatok letöltése → tisztítás → összekapcsolás → KPI-k → ábrák Jupyter Notebookban.

**Központi kérdés:** Hogyan változik Magyarország demográfiai szerkezete, és milyen párhuzamok figyelhetők meg a munkaképes korú népesség, a foglalkoztatás és a gazdasági teljesítmény alakulásában?

## Projektstruktúra

```text
KSH_data_analyses/
├── README.md
├── requirements.txt
├── .gitignore
├── config/settings.py          # útvonalak, API URL, dataset-azonosítók, fájlnevek
├── data/
│   ├── raw/                    # nyers letöltések (gitignored) + source_metadata.json
│   ├── processed/              # hungary_indicators.csv (a notebook írja)
│   └── sample_data/            # kis, verziókezelt KSH-kivonatok (offline futtatáshoz)
├── src/
│   ├── ksh_client.py           # HTTP-kérések a KSH API-hoz, nyers mentés
│   ├── data_loader.py          # CSV/JSON betöltés, nyers KSH-formátumok átalakítása
│   ├── data_cleaning.py        # oszlopnevek, típusok, hiányzó értékek, ellenőrzések
│   ├── data_transform.py       # év szerinti összekapcsolás
│   ├── indicators.py           # KPI-k
│   └── visualization.py        # 3 ábra, PNG-mentéssel
├── notebooks/demographic_analysis.ipynb
├── outputs/charts/             # elmentett ábrák
└── tests/test_indicators.py
```

## Telepítés és futtatás

```bash
# Virtuális környezet létrehozása
python -m venv .venv

# Aktiválás macOS/Linux rendszeren
source .venv/bin/activate

# Aktiválás Windows PowerShellben
.venv\Scripts\Activate.ps1

# Függőségek telepítése
pip install -r requirements.txt

# Notebook indítása a projekt gyökérkönyvtárából
jupyter notebook
```

Ezután nyisd meg a `notebooks/demographic_analysis.ipynb`-t, és futtasd: **Kernel → Restart & Run All**.
A notebook maga keresi meg a projektgyökeret (a `config/settings.py` alapján), így az importok a `notebooks/` mappából indított kernelből is működnek.

Tesztek (hálózat nélkül):

```bash
python -m unittest discover -s tests -t .
```

## Mintaadat-mód és API-mód

A notebook 3. szakaszában:

```python
USE_SAMPLE_DATA = True   # alapértelmezés: helyi mintaadat, internet nélkül is fut
USE_SAMPLE_DATA = False  # letöltés a KSH-ból a data/raw/ mappába, majd feldolgozás
```

API-módban a letöltés kb. 17 MB (a népesség-CSV ~12 MB, a GDP XML ~4,5 MB).

## Adatforrások

A KSH API-t 2026-11-15-én ellenőriztük. Dokumentáció: https://data.ksh.hu/dokumentacio (OpenAPI: https://data.ksh.hu/openapi/).
Csak a dokumentált végpontokat használjuk: `GET /datasets.json`, `GET /datasets/{id}/metadata.rdf`, és az RDF-ben megadott `downloadURL`.

| Adatkör | Forrás | Elérés | Definíció, mértékegység | Időszak |
|---|---|---|---|---|
| Demográfia | KSH API – *HVD - Népesség* (`f44d314b-…`), állomány: *Population on 1 January by sex, age and citizenship* (`5c5c1828-…`, CSV) | programozott (API) | **január 1-jei** népesség, fő; AGE = TOTAL, Y_LT15, Y15-64, Y_GE65; SEX = T; CITIZEN = TOTAL | 2013–2024 |
| Foglalkoztatás | KSH STADAT 20.1.1.3 – https://www.ksh.hu/stadat_files/mun/hu/mun0003.csv | CSV letöltés (nem része az API-nak) | foglalkoztatási ráta, **15–64 évesek**, %, éves átlag (munkaerő-felmérés) | 2009–2025 |
| GDP | KSH API – *Nemzeti számlák – a GDP főbb éves aggregátumai* (`93a05949-…`), állomány: NAMAIN_T01GDP_A (`bd19297c-…`, SDMX XML) | programozott (API) | **reál GDP**: B1GQ, láncolt volumen (PRICES=L), 2021-es referenciaév, millió Ft | 1995–2024 (2024 előzetes) |

Részletes forrás-metaadatok: `data/raw/source_metadata.json`.

### Adatok státusza

- **Hivatalos KSH-adat:** a data.ksh.hu és a STADAT forrásai.
- **Lokálisan tárolt, KSH-ból letöltött nyers adat:** `data/raw/` (API-módban jön létre, nem verziókezelt).
- **Mintaadat (`data/sample_data/`):** a fenti hivatalos KSH-forrásokból 2026-11-15-én kivonatolt értékek, a projekt sémájára átalakítva. **Nem szintetikus adat**, ezért szintetikus tesztadatra nem volt szükség.

## KPI-k

| Mutató | Képlet | Egység |
|---|---|---|
| `working_age_ratio` | 15–64 évesek / teljes népesség × 100 | % |
| `elderly_ratio` | 65+ évesek / teljes népesség × 100 | % |
| `ageing_index` | 65+ évesek / 0–14 évesek × 100 | 65+ fő 100 gyermekre |
| `employment_rate` | KSH hivatalos érték, nem számoljuk újra | % |
| `gdp_per_capita` | reál GDP / jan. 1-jei népesség | Ft/fő, 2021-es láncolt áron (**közelítés**) |
| `population_15_64_yoy_pct`, `gdp_yoy_pct` | éves %-os változás, csak egymást követő évek között | % |

Nullával osztás vagy hiányzó bemenet esetén az eredmény `NaN`.

## Összekapcsolás

Left join a népességi táblára (év kulcs): minden demográfiai év (2013–2024) megmarad; ahol gazdasági adat hiányzik, ott `NaN`. A népességi időszakon kívüli évek (foglalkoztatás 2009–2012, 2025; GDP 2000–2012) nem kerülnek az elemzési táblába – a `merge_datasets` ezt ki is írja.

## Ismert korlátok

- A KSH API-n elérhető népesség-állomány csak **2013-tól** tartalmaz adatot; a specifikációban kért 2000-es kezdés így nem teljesül. Hosszabb idősorhoz STADAT népességi tábla használható (nem része a projektnek).
- A népesség év eleji (jan. 1.), a foglalkoztatási ráta éves átlag – eltérő referencia-időpont.
- A GDP/fő a jan. 1-jei népességgel számolt közelítés (nem évközi átlagnépesség).
- A 2024-es GDP előzetes adat; a KSH revideálhatja.
- A STADAT CSV formátuma (blokkok, kódolás, oszlopnevek) a KSH által változhat; ekkor a `load_ksh_employment_stadat` igazítást igényelhet.
- Az API dataset- és állomány-azonosítói (`config/settings.py`) a KSH oldalán változhatnak – ha a letöltés hibát ad, ellenőrizd őket a `get_datasets()` és `get_distribution_urls()` függvényekkel.
- Az ábrák együttmozgást mutatnak, **nem ok-okozati kapcsolatot**.
