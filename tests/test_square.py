"""Unit tests for the Square shape."""
from typing import Dict

import pytest

from prim import Square


def test_area() -> None:
    square = Square(x=10, y=20, side=5)

    assert square.area() == 25


def test_bounding_box() -> None:
    square = Square(x=10, y=20, side=5)

    assert square.bounding_box() == (10, 20, 15, 25)


def test_rejects_non_positive_side() -> None:
    with pytest.raises(ValueError):
        Square(x=10, y=20, side=0)


@pytest.mark.parametrize(
    "coordinates",
    [
        {"x": -1, "y": 20, "side": 5},
        {"x": 10, "y": -1, "side": 5},
    ],
)
def test_rejects_coordinates_that_are_not_bigger_than_zero(
    coordinates: Dict[str, float],
) -> None:
    with pytest.raises(ValueError):
        Square(**coordinates)


def test_rejects_message_names_invalid_coordinates() -> None:
    with pytest.raises(ValueError, match="Invalid: x, y"):
        Square(x=-1, y=-1, side=5)


def test_svg() -> None:
    svg = Square(x=10, y=20, side=5, color="blue").to_svg()

    assert "<rect" in svg
    assert 'x="10"' in svg
    assert 'y="20"' in svg
    assert 'width="5"' in svg
    assert 'height="5"' in svg
    assert 'fill="blue"' in svg


def test_order_defaults_to_zero() -> None:
    square = Square(x=10, y=20, side=5)

    assert square.order == 0
