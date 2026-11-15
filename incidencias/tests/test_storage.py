from pathlib import Path

import pytest

from incidencias.storage import StorageError, load_incidents, save_incidents


@pytest.fixture
def store(tmp_path: Path) -> Path:
    return tmp_path / "data" / "incidents.json"

def test_missing_file_returns_empty_list(store: Path) -> None:
    assert load_incidents(store) == []

def test_roundtrip(store: Path) -> None:
    data = [{"id": 1, "plate": "1234BCD", "description": "Ruido en el motor"}]
    save_incidents(store, data)
    assert load_incidents(store) == data

def test_corrupt_file_raises_storage_error(store: Path) -> None:
    store.parent.mkdir(parents=True)
    store.write_text("{roto", encoding="utf-8")
    with pytest.raises(StorageError, match="JSON válido"):
        load_incidents(store)
