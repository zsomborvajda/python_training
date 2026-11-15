# Hungary Demographic & Economic Insights

## Projektépítési specifikáció Claude számára

> **Cél:** építs fel egy oktatási célú, kezdő--középhaladó
> Python-projektet, amely 2--3 óra alatt végigvezet a KSH-adatok
> megszerzésétől az adatfeldolgozáson át a Jupyter Notebookban történő
> elemzésig és vizualizációig.
>
> **Projekt nyelve:** a dokumentáció és a notebook magyarázó szövegei
> magyarul legyenek. A Python változó- és függvénynevek legyenek
> angolul.
>
> **Fontos:** ne csak tervet vagy kódrészleteket adj. Hozd létre a
> teljes, futtatható projektstruktúrát, a forrásfájlokat, a notebookot,
> a README-t és a függőségi listát.

------------------------------------------------------------------------

# 1. Projektcél és elemzési kérdés

A projekt címe: **Hungary Demographic & Economic Insights**

A résztvevő azt vizsgálja, hogyan változik Magyarország népessége és
korösszetétele, hogyan alakul a munkaképes korú népesség, az elöregedés,
a foglalkoztatás és a gazdasági teljesítmény.

Központi kérdés:

**Hogyan változik Magyarország demográfiai szerkezete, és milyen
párhuzamok figyelhetők meg a munkaképes korú népesség, a foglalkoztatás
és a gazdasági teljesítmény alakulásában?**

A projekt oktatási célú, ezért a kód legyen egyszerűen olvasható, jól
tagolt, kommentált, de ne legyen túlbonyolítva.

## Tanulási célok

A résztvevő gyakorolja:

1.  külső statisztikai adatforrás API-n keresztüli elérését;
2.  HTTP-kérések és JSON/CSV válaszok kezelését;
3.  nyers adatok mentését;
4.  Python modulok és függvények létrehozását;
5.  Pandas-alapú tisztítást, transzformációt és adat-összekapcsolást;
6.  mutatók (KPI-k) számítását;
7.  saját modulok importálását Jupyter Notebookból;
8.  diagramok készítését Matplotlib és Seaborn segítségével;
9.  az eredmények értelmezését és korlátainak felismerését.

------------------------------------------------------------------------

# 2. Időkeret és tervezési korlátok

A teljes gyakorlat célideje **150 perc**, a megengedett tartomány
120--180 perc.

  Részfeladat                              Célidő
  ------------------------------------- ---------
  Projekt és adatforrások megismerése     15 perc
  KSH API és adatletöltés                 30 perc
  Adattisztítás és transzformáció         30 perc
  KPI-k és Python modulok                 25 perc
  Jupyter Notebook összeállítása          20 perc
  Vizualizáció és értelmezés              25 perc
  Összefoglalás                            5 perc

**Ne építs be** adatbázist, Docker-környezetet, webalkalmazást, felhős
infrastruktúrát, komplex orchestrationt vagy gépi tanulást. Ezek kívül
esnek a feladat célján és időkeretén.

A projekt legyen lokálisan futtatható, egyszerű Python-környezettel.

------------------------------------------------------------------------

# 3. Adatforrások és adatválasztás

## Elsődleges forrás

A projekt elsődleges adatforrása a Központi Statisztikai Hivatal (KSH).

Kiindulópontok:

-   KSH weboldal: https://www.ksh.hu/
-   KSH STADAT: https://www.ksh.hu/stadat
-   KSH adatportál / API dokumentáció: https://data.ksh.hu/

**Kritikus követelmény:** a projektben ne találj ki API-végpontot,
paramétert, dataset-azonosítót vagy válaszformátumot. Először vizsgáld
meg az aktuális KSH API dokumentációját, és csak dokumentált végpontot
használj. Ha a dokumentáció vagy egy dataset nem érhető el, ezt a
README-ben egyértelműen jelezd, és használd az alább leírt CSV fallback
megoldást.

A KSH API és a STADAT táblák elérhetősége nem feltétlenül azonos. Ne
feltételezd, hogy minden STADAT-tábla közvetlenül elérhető ugyanazon
API-n keresztül.

## Szükséges adatkörök

A projekt három adatkört használjon:

### A. Demográfia -- kötelező, elsődleges adatforrás

Éves vagy adott referencia-időpontra vonatkozó magyarországi
népességadatok korcsoport szerint:

-   teljes népesség;
-   0--14 éves népesség;
-   15--64 éves népesség;
-   65 éves és idősebb népesség.

Lehetőleg legalább 2000-től a legutolsó elérhető évig terjedő idősor
legyen.

A korcsoportos bontás és a referencia-időpont pontos definícióját őrizd
meg a metaadatokban. Ha a forrás csak ötéves korcsoportokat ad, azokat
helyesen kell összegezni. Ne keverd össze az év eleji és évközi
népességet.

### B. Munkaerőpiac -- másodlagos adatforrás

Éves foglalkoztatási ráta, lehetőleg a 15--64 éves korosztályra,
százalékban.

Ha ez a pontos mutató nem érhető el, válassz egy világosan dokumentált,
összehasonlítható foglalkoztatási mutatót. A korcsoportot és a
definíciót tüntesd fel.

### C. Gazdaság -- másodlagos adatforrás

Éves GDP vagy GDP volumenindex, lehetőleg reálértéken, valamint -- ha
megbízhatóan elérhető -- egy főre jutó GDP.

Ne hasonlíts össze nominális GDP-t és reál GDP-t úgy, mintha azonos
mutatók lennének. A mértékegységet, árszintet, bázisévet és pénznemet
dokumentáld.

## Javasolt megvalósítási stratégia

A 2--3 órás oktatási időkeret miatt alkalmazz hibrid adatbetöltést:

1.  **A demográfiai adatkört** töltsd le programozottan a KSH API
    dokumentált végpontján keresztül, amennyiben az adott adatkészlet
    API-n elérhető.
2.  **A foglalkoztatási és GDP-adatkörökhöz** használj KSH által
    publikált, letölthető CSV/XLSX fájlokat, ha ezek API-s elérése nem
    egyértelmű vagy túl sok időt igényel.
3.  A másodlagos forrásokhoz mellékelj előre letöltött,
    forrásmegjelöléssel ellátott mintaadatokat, hogy a projekt internet
    vagy API-változás esetén is végigfuttatható legyen.
4.  Ha fájlokat nem tudsz megbízhatóan letölteni, hozz létre egy
    kisméretű, szintetikus tesztadatot külön `sample_data/` könyvtárban,
    és **egyértelműen jelöld, hogy nem hivatalos KSH-adat**. A
    szintetikus adat soha ne legyen a valódi eredményként bemutatva.

A README különböztesse meg: - a hivatalos KSH-adatot; - a lokálisan
tárolt, KSH-ból letöltött nyers adatot; - a szintetikus tesztadatot.

## Forrásmetaadatok

Minden nyers adat mellé készíts rövid metaadat-leírást, lehetőleg
`data/raw/source_metadata.json` fájlban, amely tartalmazza:

-   forrás neve;
-   forrás URL-je;
-   dataset vagy STADAT tábla címe/azonosítója;
-   letöltés dátuma;
-   referencia-időszak;
-   mértékegység;
-   korcsoport / populáció definíció;
-   adatállapot (official / sample / synthetic);
-   esetleges módszertani megjegyzések.

Ne állítsd be automatikusan a letöltés dátumát az adat referenciaévének.

------------------------------------------------------------------------

# 4. Elemzési mutatók (KPI-k)

A projekt legalább az alábbi mutatókat számítsa ki, ha a forrásadatok
lehetővé teszik:

## 4.1. Munkaképes korú népesség aránya

**Képlet:**

`working_age_ratio = population_15_64 / total_population * 100`

Mértékegység: százalék.

## 4.2. Idős népesség aránya

**Képlet:**

`elderly_ratio = population_65_plus / total_population * 100`

Mértékegység: százalék.

## 4.3. Öregedési index

**Képlet:**

`ageing_index = population_65_plus / population_0_14 * 100`

Értelmezés: a 65 éves és idősebb népesség száma 100 gyermekkorúra (0--14
évesre) vetítve.

Ha az érték 100 felett van, az idős népesség létszáma meghaladja a 0--14
éves népességét.

## 4.4. Foglalkoztatási ráta

A KSH-forrás definícióját használd. Ne számítsd újra, ha a forrásban
kész, hivatalos ráta áll rendelkezésre, kivéve ha a számláló és nevező
is egyértelműen adott.

## 4.5. GDP/fő

Csak akkor számítsd ki, ha a GDP és a népesség: - azonos területi
lefedettségű; - megfelelően összehangolt időszakú; - mértékegysége
ismert és egységesíthető.

Dokumentáld, hogy nominális vagy reál GDP/fő szerepel-e.

## 4.6. Éves változás

Legalább a munkaképes korú népességre és a GDP-re számíts éves
változást, amennyiben az idősor alkalmas rá.

Például:

`population_yoy_pct = population.pct_change() * 100`

Ne számíts éves változást olyan adatsorra, ahol az egymást követő
megfigyelések nem egymást követő éveket jelentenek.

------------------------------------------------------------------------

# 5. Projektstruktúra

Az alábbi struktúrát hozd létre:

``` text
hungary-demographic-analysis/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   ├── processed/
│   │   └── .gitkeep
│   └── sample_data/
│       ├── population_sample.csv
│       ├── employment_sample.csv
│       └── gdp_sample.csv
│
├── src/
│   ├── __init__.py
│   ├── ksh_client.py
│   ├── data_loader.py
│   ├── data_cleaning.py
│   ├── data_transform.py
│   ├── indicators.py
│   └── visualization.py
│
├── notebooks/
│   └── demographic_analysis.ipynb
│
├── outputs/
│   └── charts/
│       └── .gitkeep
│
└── tests/
    ├── __init__.py
    └── test_indicators.py
```

A notebookból a projekt gyökérkönyvtárából indítható legyen a Jupyter,
és az importok megbízhatóan működjenek. Ne támaszkodj törékeny, aktuális
munkakönyvtártól függő relatív útvonalakra. Használj `pathlib.Path`-ot
és a projekt gyökérkönyvtárának robusztus meghatározását.

------------------------------------------------------------------------

# 6. Modulok részletes specifikációja

## 6.1. `config/settings.py`

Tartalmazza: - projekt gyökérkönyvtárát; - raw, processed, sample,
output és chart könyvtárak útvonalát; - API base URL-t; - timeout
értéket; - vizsgált kezdőévet, ha az API ezt támogatja; - a fájlneveket.

Ne legyenek szétszórva a kódban hardcode-olt útvonalak.

## 6.2. `src/ksh_client.py`

Feladata: - HTTP GET kérés küldése; - timeout beállítása; - HTTP hibák
kezelése `raise_for_status()` segítségével; - JSON-válasz visszaadása; -
adatkészlet-lista lekérése kizárólag a dokumentációban igazolt
végponttal; - a letöltött nyers válasz mentése.

Elvárt függvények (az API dokumentációjához igazíthatók):

``` python
def get_datasets():
    """Lekéri az elérhető KSH adatkészleteket."""

def fetch_dataset(dataset_id, params=None):
    """Lekér egy dokumentált KSH adatkészletet."""

def save_json(data, filepath):
    """JSON adat mentése UTF-8 kódolással."""
```

A `fetch_dataset` végpontját és paramétereit ne találd ki. Ha a
dataset-azonosító vagy az API séma nem állapítható meg, készíts jól
dokumentált adapter-felületet, és jelezd a README-ben, hogy a tényleges
dataset-konfigurációt ellenőrizni kell.

## 6.3. `src/data_loader.py`

Feladata: - CSV betöltése Pandas DataFrame-be; - JSON betöltése, ha
szükséges; - UTF-8 és magyar karakterek helyes kezelése; - fájlhiány
esetén érthető hibaüzenet.

Elvárt függvények:

``` python
def load_csv(filepath):
    """CSV fájl betöltése DataFrame-be."""

def load_json(filepath):
    """JSON fájl betöltése."""
```

## 6.4. `src/data_cleaning.py`

Feladata: - oszlopnevek normalizálása; - év mező numerikussá
alakítása; - numerikus oszlopok konvertálása; - üres sorok és
duplikátumok ellenőrzése; - hiányzó értékek jelentése; - hibás vagy
lehetetlen értékek jelzése.

Ne tölts ki automatikusan hiányzó statisztikai adatot nullával. A
hiányzó érték jelentése nem feltétlenül nulla.

Elvárt függvények:

``` python
def normalize_columns(df):
    """Oszlopnevek egységesítése."""

def clean_population_data(df):
    """Demográfiai adatok tisztítása."""

def clean_economic_data(df):
    """Gazdasági és foglalkoztatási adatok tisztítása."""
```

A függvények ne módosítsák észrevétlenül az eredeti DataFrame-et;
használjanak másolatot.

## 6.5. `src/data_transform.py`

Feladata: - eltérő források egységes év szerinti összekapcsolása; - éves
aggregálás, ha szükséges és módszertanilag indokolt; - rendezés év
szerint; - elemzési tábla előállítása.

Elvárt függvény:

``` python
def merge_datasets(population, employment, gdp):
    """Összekapcsolja az adatforrásokat év szerint."""
```

Az összekapcsolás előtt ellenőrizd: - egyedi-e az év kulcs az egyes
táblákban; - azonos-e az időbeli granularitás; - vannak-e eltérő
évkészletek; - miért választottál `inner` vagy `left` join-t.

Ne dobj el csendben éveket. A README vagy notebook magyarázza el, ha
csak közös évek kerülnek az elemzésbe. Ha a források időszaka eltér,
mutasd meg az eredményben az elérhető évek számát.

## 6.6. `src/indicators.py`

Feladata a KPI-k kiszámítása.

Elvárt függvény:

``` python
def calculate_indicators(df):
    """Kiszámítja a demográfiai és gazdasági mutatókat."""
```

Kezeld a nullával osztás és hiányzó adatok esetét. A számított érték
legyen `NaN`, ha a szükséges bemeneti adat hiányzik vagy a nevező nulla.

A függvény visszatérési értéke új DataFrame legyen.

## 6.7. `src/visualization.py`

Készíts legalább három ábrát. Az ábrák: - legyenek magyar vagy
egyértelmű angol címkékkel; - tartalmazzanak címet és
tengelyfeliratokat; - legyenek olvashatók; - mentsék el a PNG fájlokat
az `outputs/charts/` könyvtárba; - notebookban is jelenjenek meg.

Elvárt függvények:

``` python
def plot_population_by_age(df, output_dir):
    """Korcsoportos népesség idősora."""

def plot_ageing_index(df, output_dir):
    """Öregedési index idősora, 100-as referencia-vonallal."""

def plot_economy_and_employment(df, output_dir):
    """Foglalkoztatás és GDP kapcsolatának szemléltetése."""
```

A harmadik diagram lehet: - két külön idősor, ha az eltérő mértékegység
miatt a scatter félrevezető lenne; vagy - scatter plot, ha az évekhez
tartozó értékek és a mutatók definíciói összehasonlíthatók.

A diagramon ne sugallj ok-okozati összefüggést pusztán korreláció
alapján.

------------------------------------------------------------------------

# 7. Jupyter Notebook specifikáció

Hozd létre a `notebooks/demographic_analysis.ipynb` fájlt érvényes
Jupyter Notebook formátumban.

A notebook cellái a következő sorrendben legyenek:

## 1. Bevezetés -- Markdown cella

-   projekt címe;
-   elemzési kérdés;
-   rövid célkitűzés;
-   adatforrások és módszertani figyelmeztetés.

## 2. Környezet és importok -- Code cella

-   szükséges package-ek importálása;
-   projekt gyökérkönyvtárának beállítása;
-   saját `src` modulok importálása.

## 3. Adatgyűjtés -- Markdown + Code cella

-   KSH API adatkészlet-listájának lekérése;
-   releváns dataset azonosítása vagy konfiguráció betöltése;
-   API-adat letöltése és mentése;
-   hiba esetén egyértelmű útmutatás a helyi mintaadat használatához.

Ne próbálja minden notebook-futtatás automatikusan letölteni az összes
adatot, ha az API lassú vagy nem elérhető. Legyen egy jól látható
konfigurációs változó, például:

``` python
USE_SAMPLE_DATA = True
```

A mintamód legyen alapértelmezés szerint futtatható. A valódi API-hívás
külön cellában vagy kapcsolóval legyen kipróbálható.

## 4. Adatok betöltése -- Code cella

-   a három adatforrás betöltése;
-   `head()`;
-   `info()`;
-   `describe()`.

## 5. Adatminőség ellenőrzése -- Code cella

-   hiányzó értékek;
-   duplikátumok;
-   adattípusok;
-   évintervallumok;
-   mértékegységek ellenőrzése.

## 6. Tisztítás és transzformáció -- Code cella

A saját modulok függvényeit hívd meg. A notebookban ne másold be újra a
modulok teljes implementációját.

## 7. KPI-k számítása -- Code cella

Mutasd meg az elkészült KPI-k első és utolsó néhány sorát.

## 8. Eredmények exportálása -- Code cella

Mentsd a feldolgozott adatot ide:

`data/processed/hungary_indicators.csv`

## 9. Vizualizáció -- Markdown + Code cellák

Készítsd el a három diagramot a `visualization.py` modul függvényeinek
meghívásával.

## 10. Következtetések -- Markdown cella

Legyenek előre megadott kérdések, amelyekre a résztvevő a saját
eredményei alapján válaszol:

1.  Hogyan változott a 15--64 éves népesség aránya?
2.  Hogyan változott az öregedési index?
3.  Mely időszakban volt a legnagyobb változás?
4.  Mit mutat a foglalkoztatás és a GDP idősora?
5.  Milyen korlátai vannak az elemzésnek?

A notebook ne tartalmazzon előre kitalált eredményeket vagy hamis
következtetéseket. A szöveges következtetéseket a ténylegesen betöltött
adatokból kell levonni.

------------------------------------------------------------------------

# 8. Mintaadatok

A projektnek akkor is végigfuttathatónak kell lennie, ha a KSH API
átmenetileg nem érhető el.

Hozz létre három kis CSV mintaadatot, legalább 10--15 évvel, az alábbi
oszlopokkal:

### `population_sample.csv`

``` text
year,total_population,population_0_14,population_15_64,population_65_plus
```

### `employment_sample.csv`

``` text
year,employment_rate
```

### `gdp_sample.csv`

``` text
year,gdp
```

Ha a mintaadatok szintetikusak, a README-ben és a notebookban jól
láthatóan tüntesd fel:

**„FIGYELEM: Ezek szintetikus, oktatási célú mintaadatok, nem hivatalos
KSH-statisztikák. Valós következtetés levonására nem használhatók."**

A szintetikus adatok legyenek életszerű nagyságrendűek, de ne próbáld
őket hivatalos statisztikaként feltüntetni. A projekt struktúrája és
függvényei ugyanúgy működjenek velük.

------------------------------------------------------------------------

# 9. Követelmények és futtatás

A `requirements.txt` legyen minimális:

``` text
requests
pandas
numpy
matplotlib
seaborn
jupyter
ipykernel
```

A README tartalmazza az alábbi lépéseket:

``` bash
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

A README mutassa meg: - a projektstruktúrát; - a csomagok telepítését; -
a notebook futtatását; - a mintaadat és az API mód közötti váltást; - az
adatforrások URL-jeit; - az adatok definícióit és mértékegységeit; - az
ismert korlátokat.

A `.gitignore` zárja ki legalább: - `.venv/`; - `__pycache__/`; -
`.ipynb_checkpoints/`; - szükség szerint a nagyobb, letöltött raw
fájlokat.

A kis mintaadatok maradjanak verziókezelhetők.

------------------------------------------------------------------------

# 10. Tesztelés

Készíts legalább néhány egyszerű tesztet a `tests/test_indicators.py`
fájlban.

Teszteld: - az öregedési index helyes számítását; - a munkaképes korú
népesség arányát; - a nullával osztás kezelését; - hogy a bemeneti
DataFrame nem módosul váratlanul.

A tesztekhez használj kicsi, kézzel megadott Pandas DataFrame-et. Ne
legyen szükség hálózati kapcsolatra.

A tesztek futtatása:

``` bash
python -m unittest discover -s tests
```

Ha `pytest` használata mellett döntesz, add hozzá a
`requirements.txt`-hez és dokumentáld.

------------------------------------------------------------------------

# 11. Minőségi és technikai elvárások

-   Python 3.10+ kompatibilitás.
-   Egyszerű, olvasható függvények.
-   Type hint használata, ahol nem teszi nehézkessé a kódot.
-   Docstring minden publikus függvényhez.
-   Érthető hibaüzenetek.
-   HTTP timeout és HTTP hibakezelés.
-   Nincs API-kulcs vagy titok a kódban.
-   Nincs kitalált API-végpont vagy dataset-azonosító.
-   Nincs csendes adatvesztés az összekapcsoláskor.
-   A nyers adatot ne írd felül a transzformált adattal.
-   A feldolgozott adat külön fájlba kerüljön.
-   A notebook a saját modulokat használja.
-   A notebook Kernel → Restart & Run All művelettel, tiszta
    környezetben is fusson.
-   A mintaadat-alapú útvonal internet nélkül is működjön.
-   A diagramok fájlba is mentődjenek.
-   A szintetikus és hivatalos adat egyértelműen legyen
    megkülönböztetve.

------------------------------------------------------------------------

# 12. Definition of Done -- elfogadási kritériumok

A projekt akkor tekinthető késznek, ha:

-   [ ] A teljes könyvtárstruktúra létrejött.
-   [ ] A `requirements.txt` telepíthető.
-   [ ] A README alapján a projekt elindítható.
-   [ ] Van dokumentált KSH API-kapcsolódási példa, amely nem használ
    kitalált végpontot.
-   [ ] A projekt mintaadatokkal internet nélkül is futtatható.
-   [ ] A nyers és feldolgozott adatok külön könyvtárban vannak.
-   [ ] A tisztítás és transzformáció saját Python modulokban található.
-   [ ] A KPI-számítás saját Python modulban található.
-   [ ] A notebook a modulokat importálja, nem másolja a teljes üzleti
    logikát.
-   [ ] Legalább három diagram elkészül és PNG-ként elmentődik.
-   [ ] A feldolgozott eredmény CSV-be exportálódik.
-   [ ] A KPI-k tesztjei sikeresen lefutnak.
-   [ ] A notebook Restart & Run All módban végigfuttatható.
-   [ ] A mintaadatok státusza (hivatalos vagy szintetikus) egyértelmű.

------------------------------------------------------------------------

# 13. Claude-nak szóló végrehajtási utasítás

A fenti specifikáció alapján építsd fel a teljes projektet.

**Munkamenet:**

1.  Először ellenőrizd a KSH aktuális API dokumentációját és az elérhető
    adatköröket. Ne találj ki endpointokat vagy dataset-azonosítókat.
2.  Válaszd ki a leginkább megfelelő demográfiai adatforrást.
    Dokumentáld a kiválasztás okát és a séma részleteit.
3.  Ha valamelyik adatkör programozott lekérése nem valósítható meg
    gyorsan és megbízhatóan, használd a dokumentált CSV fallback
    megoldást.
4.  Hozd létre az összes fájlt a fenti struktúrában.
5.  Készíts futtatható, önálló modulokat.
6.  Készíts teljes Jupyter Notebookot, amely a modulokat importálja.
7.  Hozz létre mintaadatokat, hogy internet nélkül is tesztelhető legyen
    a projekt.
8.  Futtasd le a teszteket.
9.  Ellenőrizd, hogy a notebook összes cellája lefuttatható-e a
    mintaadatokkal.
10. A végén adj rövid összefoglalót a létrehozott fájlokról, a futtatási
    lépésekről, az API ténylegesen ellenőrzött elérhetőségéről és az
    esetleges korlátozásokról.

**Ne állj meg a projektterv vagy a kódváz elkészítésénél. A teljes,
futtatható MVP-t hozd létre.** Ha egy külső adatforrás nem érhető el, ne
állítsd, hogy sikeresen letöltötted; dokumentáld a korlátot, és
biztosíts működő mintaadat-alapú megoldást.
