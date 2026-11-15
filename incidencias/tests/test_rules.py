import pytest

from incidencias.rules import mentions_danger, mileage_category


@pytest.mark.parametrize(
    ("km", "expected"),
    [(0, "Normal"), (99_999, "Normal"), (100_000, "Alto"), (200_000, "Muy alto")],
)

def test_mileage_category(km, expected):
    assert mileage_category(km) == expected

def test_mentions_danger_ignore_cases():
    assert mentions_danger("Sale HUMO del capó")
    assert not mentions_danger("el motor esta bien")
