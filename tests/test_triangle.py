"""Unit tests for the Triangle primitive."""
from typing import Dict

import pytest

from prim import Triangle


def test_area() -> None:
    triangle = Triangle(x1=1, y1=1, x2=11, y2=1, x3=1, y3=6)

    assert triangle.area() == 25


def test_area_is_not_affected_by_point_order() -> None:
    triangle = Triangle(x1=1, y1=6, x2=11, y2=1, x3=1, y3=1)

    assert triangle.area() == 25


def test_bounding_box() -> None:
    triangle = Triangle(x1=4, y1=9, x2=12, y2=3, x3=2, y3=7)

    assert triangle.bounding_box() == (2, 3, 12, 9)


@pytest.mark.parametrize(
    "coordinates",
    [
        {"x1": -1, "y1": 1, "x2": 10, "y2": 1, "x3": 1, "y3": 5},
        {"x1": 1, "y1": -1, "x2": 10, "y2": 1, "x3": 1, "y3": 5},
        {"x1": 1, "y1": 1, "x2": -1, "y2": 1, "x3": 1, "y3": 5},
        {"x1": 1, "y1": 1, "x2": 10, "y2": -1, "x3": 1, "y3": 5},
        {"x1": 1, "y1": 1, "x2": 10, "y2": 1, "x3": -1, "y3": 5},
        {"x1": 1, "y1": 1, "x2": 10, "y2": 1, "x3": 1, "y3": -1},
    ],
)
def test_rejects_coordinates_that_are_not_bigger_than_zero(
    coordinates: Dict[str, float],
) -> None:
    with pytest.raises(ValueError):
        Triangle(**coordinates)


def test_rejects_message_names_invalid_coordinates() -> None:
    with pytest.raises(ValueError, match="Invalid: x1, y2, x3"):
        Triangle(x1=-1, y1=1, x2=10, y2=-1, x3=-1, y3=5)


def test_svg() -> None:
    svg = Triangle(x1=1, y1=1, x2=11, y2=1, x3=1, y3=6, color="green").to_svg()

    assert "<polygon" in svg
    assert 'points="1,1 11,1 1,6"' in svg
    assert 'fill="green"' in svg


def test_order_defaults_to_zero() -> None:
    triangle = Triangle(x1=1, y1=1, x2=11, y2=1, x3=1, y3=6)

    assert triangle.order == 0
