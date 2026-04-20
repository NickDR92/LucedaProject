"""Integration tests for drawings composed of multiple primitives."""

import math
import unittest
from typing import Dict, Tuple

from prim import Circle, BaseShape, ShapeKind, Square, Triangle
from drawing import Drawing


class TestObject(BaseShape):
    """Simple custom object used to test dynamic object-kind scoring."""

    kind: str = "custom"
    order: int = 0

    def area(self) -> float:
        """Return a fixed test area."""
        return 100

    def start_point(self) -> Tuple[float, float]:
        """Return a valid start point inside the drawing."""
        return 0, 0

    def to_svg(self) -> str:
        """Return a minimal SVG element for integration tests."""
        return '<rect x="0" y="0" width="10" height="10" />'


class DrawingTest(unittest.TestCase):
    """Verify drawing-level behavior."""

    def test_area_by_kind(self) -> None:
        drawing: Drawing = Drawing()
        drawing.add(Square(x=0, y=0, side=10))
        drawing.add(Circle(x=0, y=0, radius=10))
        drawing.add(Triangle(x1=0, y1=0, x2=10, y2=0, x3=0, y3=10))

        areas: Dict[str, float] = drawing.area_by_kind()

        # Drawing groups the mathematical area by primitive kind.
        self.assertEqual(areas["square"], 100)
        self.assertEqual(areas["circle"], math.pi * 100)
        self.assertEqual(areas["triangle"], 50)

    def test_area_by_kind_supports_extra_object_kinds(self) -> None:
        drawing: Drawing = Drawing()
        drawing.add(TestObject())

        areas: Dict[str, float] = drawing.area_by_kind()

        # New object kinds should be included without changing Drawing.
        self.assertEqual(areas["custom"], 100)

    def test_beautiful_score_is_100_for_equal_area_distribution(self) -> None:
        drawing: Drawing = Drawing()

        # Each primitive contributes exactly 100 area units.
        drawing.add(Square(x=0, y=0, side=10))
        drawing.add(Circle(x=0, y=0, radius=math.sqrt(100 / math.pi)))
        drawing.add(Triangle(x1=0, y1=0, x2=20, y2=0, x3=0, y3=10))

        self.assertEqual(drawing.beautiful_score(), 100)

    def test_beautiful_score_uses_number_of_present_object_kinds(self) -> None:
        drawing: Drawing = Drawing()

        # Four kinds with equal areas should target 25% each.
        drawing.add(Square(x=0, y=0, side=10))
        drawing.add(Circle(x=0, y=0, radius=math.sqrt(100 / math.pi)))
        drawing.add(Triangle(x1=0, y1=0, x2=20, y2=0, x3=0, y3=10))
        drawing.add(TestObject())

        self.assertEqual(drawing.beautiful_score(), 100)

    def test_beautiful_score_is_100_for_one_present_object_kind(self) -> None:
        drawing: Drawing = Drawing()
        drawing.add(Square(x=0, y=0, side=10))

        self.assertEqual(drawing.beautiful_score(), 100)

    def test_svg_contains_all_primitive_types(self) -> None:
        drawing: Drawing = Drawing()
        drawing.extend(
            [
                Square(x=10, y=10, side=40),
                Circle(x=100, y=100, radius=25),
                Triangle(x1=150, y1=20, x2=220, y2=90, x3=130, y3=120),
            ]
        )

        svg: str = drawing.to_svg()

        # The drawing renderer delegates SVG output to each primitive.
        self.assertIn("<rect", svg)
        self.assertIn("<circle", svg)
        self.assertIn("<polygon", svg)

    def test_svg_uses_shape_order(self) -> None:
        drawing: Drawing = Drawing()
        drawing.extend(
            [
                Circle(x=0, y=0, radius=10, color="red", order=2),
                Square(x=0, y=0, side=10, color="blue", order=1),
                Triangle(x1=0, y1=0, x2=10, y2=0, x3=0, y3=10, color="green", order=3),
            ]
        )

        svg: str = drawing.to_svg()

        self.assertLess(svg.index('fill="blue"'), svg.index('fill="red"'))
        self.assertLess(svg.index('fill="red"'), svg.index('fill="green"'))

    def test_svg_keeps_insertion_order_when_shape_order_is_equal(self) -> None:
        drawing: Drawing = Drawing()
        drawing.extend(
            [
                Circle(x=0, y=0, radius=10, color="red"),
                Square(x=0, y=0, side=10, color="blue"),
            ]
        )

        svg: str = drawing.to_svg()

        self.assertLess(svg.index('fill="red"'), svg.index('fill="blue"'))

    def test_add_allows_shape_area_to_exceed_drawing_area(self) -> None:
        drawing: Drawing = Drawing(width=100, height=100)

        drawing.add(Square(x=90, y=90, side=50))

        self.assertEqual(len(drawing.shapes), 1)

    def test_add_rejects_shape_with_start_point_outside_drawing_area(self) -> None:
        drawing: Drawing = Drawing(width=100, height=100)

        with self.assertRaisesRegex(ValueError, "square start point \\(101, 50\\)"):
            drawing.add(Square(x=101, y=50, side=10))

    def test_extend_rejects_shapes_with_start_point_outside_drawing_area(self) -> None:
        drawing: Drawing = Drawing(width=100, height=100)

        with self.assertRaisesRegex(ValueError, "circle start point \\(50, 101\\)"):
            drawing.extend(
                [
                    Square(x=10, y=10, side=10),
                    Circle(x=50, y=101, radius=10),
                ]
            )

        self.assertEqual(len(drawing.shapes), 0)

    def test_primitive_classes_are_importable_from_prim_package(self) -> None:
        # Users should be able to import all primitives from the package root.
        self.assertEqual(Circle(x=0, y=0, radius=1).kind, "circle")
        self.assertEqual(Square(x=0, y=0, side=1).kind, "square")
        self.assertEqual(Triangle(x1=0, y1=0, x2=1, y2=0, x3=0, y3=1).kind, "triangle")

    def test_builtin_primitives_use_shape_kind_enum(self) -> None:
        self.assertEqual(Circle(x=0, y=0, radius=1).kind, ShapeKind.CIRCLE)
        self.assertEqual(Square(x=0, y=0, side=1).kind, ShapeKind.SQUARE)
        self.assertEqual(Triangle(x1=0, y1=0, x2=1, y2=0, x3=0, y3=1).kind, ShapeKind.TRIANGLE)


if __name__ == "__main__":
    unittest.main()
