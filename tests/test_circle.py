"""Unit tests for the Circle primitive."""

import math
from typing import Dict

import pytest

from prim import Circle


def test_area() -> None:
    circle = Circle(x=10, y=20, radius=5)

    assert circle.area() == pytest.approx(math.pi * 25)


def test_bounding_box() -> None:
    circle = Circle(x=10, y=20, radius=5)

    assert circle.bounding_box() == (5, 15, 15, 25)


def test_rejects_non_positive_radius() -> None:
    with pytest.raises(ValueError):
        Circle(x=10, y=20, radius=0)


@pytest.mark.parametrize(
    "coordinates",
    [
        {"x": -1, "y": 20, "radius": 5},
        {"x": 10, "y": -1, "radius": 5},
    ],
)
def test_rejects_coordinates_that_are_not_bigger_than_zero(
    coordinates: Dict[str, float],
) -> None:
    with pytest.raises(ValueError):
        Circle(**coordinates)


def test_rejects_message_names_invalid_coordinates() -> None:
    with pytest.raises(ValueError, match="Invalid: x, y"):
        Circle(x=-1, y=-1, radius=5)


def test_svg() -> None:
    svg = Circle(x=10, y=20, radius=5, color="red").to_svg()

    assert "<circle" in svg
    assert 'cx="10"' in svg
    assert 'cy="20"' in svg
    assert 'r="5"' in svg
    assert 'fill="red"' in svg


def test_order_defaults_to_zero() -> None:
    circle = Circle(x=10, y=20, radius=5)

    assert circle.order == 0
