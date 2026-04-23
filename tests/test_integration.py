"""Integration tests for complete PrimitiveArt workflows."""

import math
from pathlib import Path
from typing import Dict, Tuple

from draw import Drawing
from prim import BaseShape, Circle, Square, Triangle


class CustomShape(BaseShape):
    """Custom shape used to verify framework extensibility end to end."""

    kind: str = "custom"
    order: int = 0

    def area(self) -> float:
        """Return a fixed area for integration assertions."""
        return 100

    def bounding_box(self) -> Tuple[float, float, float, float]:
        """Return valid bounds inside the draw."""
        return 1, 1, 11, 11

    def to_svg(self) -> str:
        """Render a simple SVG element for integration assertions."""
        return '<rect x="1" y="1" width="10" height="10" fill="black" />'


def test_user_can_create_score_and_save_svg_drawing(tmp_path: Path) -> None:
    drawing = Drawing(width=320, height=240, background="white")
    drawing.extend(
        [
            Square(x=10, y=10, side=10, color="blue"),
            Circle(x=50, y=50, radius=math.sqrt(100 / math.pi), color="red"),
            Triangle(x1=100, y1=10, x2=120, y2=10, x3=100, y3=20, color="gold"),
        ]
    )

    output_path = drawing.save_svg(tmp_path / "art.svg")

    assert output_path.exists()
    assert drawing.beautiful_score() == 100

    svg = output_path.read_text(encoding="utf-8")
    assert '<svg xmlns="http://www.w3.org/2000/svg"' in svg
    assert 'width="320"' in svg
    assert 'height="240"' in svg
    assert "<circle" in svg
    assert "<rect" in svg
    assert "<polygon" in svg


def test_summary_matches_area_distribution_for_mixed_shapes() -> None:
    drawing = Drawing()
    drawing.add(Square(x=1, y=1, side=10))
    drawing.add(Circle(x=10, y=10, radius=math.sqrt(100 / math.pi)))
    drawing.add(Triangle(x1=1, y1=1, x2=21, y2=1, x3=1, y3=11))

    summary = drawing.summary()

    assert "Beautiful score: 100.0/100" in summary
    assert "Square" in summary
    assert "Circle" in summary
    assert "Triangle" in summary
    assert "( 33.3%)" in summary


def test_custom_shape_kind_flows_through_area_score_and_svg() -> None:
    drawing = Drawing()
    drawing.add(Square(x=1, y=1, side=10))
    drawing.add(CustomShape())

    areas: Dict[str, float] = drawing.area_by_kind()
    svg = drawing.to_svg()

    assert areas["square"] == 100
    assert areas["custom"] == 100
    assert drawing.beautiful_score() == 100
    assert 'fill="black"' in svg


def test_empty_drawing_can_still_be_exported(tmp_path: Path) -> None:
    drawing = Drawing(width=100, height=80, background="gray")

    output_path = drawing.save_svg(tmp_path / "empty.svg")

    svg = output_path.read_text(encoding="utf-8")
    assert drawing.beautiful_score() == 0.0
    assert 'width="100"' in svg
    assert 'height="80"' in svg
    assert 'fill="gray"' in svg
