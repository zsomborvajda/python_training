"""Egyszerű kliens a KSH "Nagy értékű adatkészletek" API-hoz.

Csak a https://data.ksh.hu/dokumentacio oldalon dokumentált végpontokat használja:

1. ``GET /datasets.json``                      – adatkészletek listája (JSON)
2. ``GET /datasets/{dataset_id}/metadata.rdf`` – egy adatkészlet DCAT metaadata (RDF/XML)
3. a metaadatban szereplő ``downloadURL``      – az adatállomány (CSV vagy SDMX XML)

Hitelesítés nem szükséges.
"""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

from config import settings

RDF_NS = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}"


def _get(url: str) -> requests.Response:
    """HTTP GET timeouttal; HTTP-hiba esetén kivételt dob."""
    response = requests.get(url, timeout=settings.REQUEST_TIMEOUT)
    response.raise_for_status()
    return response


def get_datasets() -> list[dict]:
    """Lekéri az elérhető KSH adatkészleteket (``/datasets.json``)."""
    return _get(f"{settings.KSH_API_BASE_URL}/datasets.json").json()


def get_distribution_urls(dataset_id: str) -> dict[str, str]:
    """Visszaadja egy adatkészlet letölthető állományait: {distribution_id: downloadURL}.

    A ``metadata.rdf``-ből olvassa ki a ``dcat:downloadURL`` elemeket.
    """
    rdf_text = _get(f"{settings.KSH_API_BASE_URL}/datasets/{dataset_id}/metadata.rdf").text
    root = ET.fromstring(rdf_text)

    urls = {}
    for element in root.iter():
        if element.tag.endswith("downloadURL"):
            url = (element.text or "").strip() or element.get(f"{RDF_NS}resource", "")
            if url:
                distribution_id = Path(url).stem  # pl. .../data/<id>.csv -> <id>
                urls[distribution_id] = url
    return urls


def fetch_dataset(dataset_id: str, distribution_id: str, filepath: Path) -> Path:
    """Letölt egy dokumentált KSH adatállományt és nyersen elmenti.

    Args:
        dataset_id: az adatkészlet azonosítója (``datasets.json`` -> ``id``).
        distribution_id: az állomány azonosítója (``get_distribution_urls`` kulcsa).
        filepath: mentési útvonal (a ``data/raw`` könyvtárban).
    """
    urls = get_distribution_urls(dataset_id)
    if distribution_id not in urls:
        raise KeyError(
            f"A(z) {distribution_id} állomány nem található a(z) {dataset_id} adatkészletben. "
            f"Elérhető: {list(urls)}"
        )
    return download_file(urls[distribution_id], filepath)


def download_file(url: str, filepath: Path) -> Path:
    """Tetszőleges fájl letöltése bájtonként, változtatás nélkül (nyers adat)."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_bytes(_get(url).content)
    return filepath


def save_json(data, filepath: Path) -> Path:
    """JSON adat mentése UTF-8 kódolással, ékezetek megőrzésével."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return filepath
