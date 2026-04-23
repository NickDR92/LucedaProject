"""Integration tests for drawings composed of multiple primitives."""

import math
from pathlib import Path
from typing import Dict, Tuple

import pytest

import draw.drawing
from draw import Drawing
from prim import BaseShape, Circle, ShapeKind, Square, Triangle


class CustomObject(BaseShape):
    """Simple custom object used to test dynamic object-kind scoring."""

    kind: str = "custom"
    order: int = 0

    def area(self) -> float:
        """Return a fixed test area."""
        return 100

    def bounding_box(self) -> Tuple[float, float, float, float]:
        """Return valid bounds inside the draw."""
        return 0, 0, 10, 10

    def to_svg(self) -> str:
        """Return a minimal SVG element for integration tests."""
        return '<rect x="0" y="0" width="10" height="10" />'


def test_area_by_kind() -> None:
    drawing = Drawing()
    drawing.add(Square(x=1, y=1, side=10))
    drawing.add(Circle(x=10, y=10, radius=10))
    drawing.add(Triangle(x1=1, y1=1, x2=11, y2=1, x3=1, y3=11))

    areas: Dict[str, float] = drawing.area_by_kind()

    assert areas["square"] == 100
    assert areas["circle"] == pytest.approx(math.pi * 100)
    assert areas["triangle"] == 50


def test_area_by_kind_supports_extra_object_kinds() -> None:
    drawing = Drawing()
    drawing.add(CustomObject())

    areas = drawing.area_by_kind()

    assert areas["custom"] == 100


def test_beautiful_score_is_100_for_equal_area_distribution() -> None:
    drawing = Drawing()
    drawing.add(Square(x=1, y=1, side=10))
    drawing.add(Circle(x=10, y=10, radius=math.sqrt(100 / math.pi)))
    drawing.add(Triangle(x1=1, y1=1, x2=21, y2=1, x3=1, y3=11))

    assert drawing.beautiful_score() == 100


def test_beautiful_score_uses_number_of_present_object_kinds() -> None:
    drawing = Drawing()
    drawing.add(Square(x=1, y=1, side=10))
    drawing.add(Circle(x=10, y=10, radius=math.sqrt(100 / math.pi)))
    drawing.add(Triangle(x1=1, y1=1, x2=21, y2=1, x3=1, y3=11))
    drawing.add(CustomObject())

    assert drawing.beautiful_score() == 100


def test_beautiful_score_is_100_for_one_present_object_kind() -> None:
    drawing = Drawing()
    drawing.add(Square(x=1, y=1, side=10))

    assert drawing.beautiful_score() == 100


def test_svg_contains_all_primitive_types() -> None:
    drawing = Drawing()
    drawing.extend(
        [
            Square(x=10, y=10, side=40),
            Circle(x=100, y=100, radius=25),
            Triangle(x1=150, y1=20, x2=220, y2=90, x3=130, y3=120),
        ]
    )

    svg = drawing.to_svg()

    assert "<rect" in svg
    assert "<circle" in svg
    assert "<polygon" in svg


def test_svg_uses_shape_order() -> None:
    drawing = Drawing()
    drawing.extend(
        [
            Circle(x=10, y=10, radius=10, color="red", order=2),
            Square(x=1, y=1, side=10, color="blue", order=1),
            Triangle(x1=1, y1=1, x2=11, y2=1, x3=1, y3=11, color="green", order=3),
        ]
    )

    svg = drawing.to_svg()

    assert svg.index('fill="blue"') < svg.index('fill="red"')
    assert svg.index('fill="red"') < svg.index('fill="green"')


def test_svg_keeps_insertion_order_when_shape_order_is_equal() -> None:
    drawing = Drawing()
    drawing.extend(
        [
            Circle(x=10, y=10, radius=10, color="red"),
            Square(x=1, y=1, side=10, color="blue"),
        ]
    )

    svg = drawing.to_svg()

    assert svg.index('fill="red"') < svg.index('fill="blue"')


@pytest.mark.parametrize(
    ("shape", "message"),
    [
        (Square(x=90, y=90, side=50), r"square bounding box \(90, 90, 140, 140\)"),
        (Square(x=101, y=50, side=10), r"square bounding box \(101, 50, 111, 60\)"),
    ],
)
def test_add_rejects_shape_with_bounding_box_outside_drawing_area(
    shape: BaseShape,
    message: str,
) -> None:
    drawing = Drawing(width=100, height=100)

    with pytest.raises(ValueError, match=message):
        drawing.add(shape)


def test_extend_rejects_shapes_with_bounding_box_outside_drawing_area() -> None:
    drawing = Drawing(width=100, height=100)

    with pytest.raises(ValueError, match=r"circle bounding box \(40, 91, 60, 111\)"):
        drawing.extend(
            [
                Square(x=10, y=10, side=10),
                Circle(x=50, y=101, radius=10),
            ]
        )

    assert drawing.shapes == []


def test_primitive_classes_are_importable_from_prim_package() -> None:
    assert Circle(x=1, y=1, radius=1).kind == "circle"
    assert Square(x=1, y=1, side=1).kind == "square"
    assert Triangle(x1=1, y1=1, x2=2, y2=1, x3=1, y3=2).kind == "triangle"


def test_builtin_primitives_use_shape_kind_enum() -> None:
    assert Circle(x=1, y=1, radius=1).kind == ShapeKind.CIRCLE
    assert Square(x=1, y=1, side=1).kind == ShapeKind.SQUARE
    assert Triangle(x1=1, y1=1, x2=2, y2=1, x3=1, y3=2).kind == ShapeKind.TRIANGLE


def test_show_opens_temporary_svg_in_browser(monkeypatch: pytest.MonkeyPatch) -> None:
    opened_urls: list[str] = []
    drawing = Drawing(width=20, height=10, background="white")

    monkeypatch.setattr(draw.drawing.webbrowser, "open", opened_urls.append)

    output_path: Path = drawing.show()

    assert output_path.exists()
    assert opened_urls == [output_path.as_uri()]
    assert 'width="20"' in output_path.read_text(encoding="utf-8")
