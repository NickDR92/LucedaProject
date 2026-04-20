"""Integration tests for complete PrimitiveArt workflows."""

import math
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict

from drawing import Drawing
from prim import BaseShape, Circle, Square, Triangle


class CustomShape(BaseShape):
    """Custom shape used to verify framework extensibility end to end."""

    kind: str = "custom"

    def area(self) -> float:
        """Return a fixed area for integration assertions."""
        return 100

    def to_svg(self) -> str:
        """Render a simple SVG element for integration assertions."""
        return '<rect x="1" y="1" width="10" height="10" fill="black" />'


class PrimitiveArtIntegrationTest(unittest.TestCase):
    """Verify complete user-facing PrimitiveArt workflows."""

    def test_user_can_create_score_and_save_svg_drawing(self) -> None:
        drawing: Drawing = Drawing(width=320, height=240, background="white")
        drawing.extend(
            [
                Square(x=10, y=10, side=10, color="blue"),
                Circle(x=50, y=50, radius=math.sqrt(100 / math.pi), color="red"),
                Triangle(x1=100, y1=10, x2=120, y2=10, x3=100, y3=20, color="gold"),
            ]
        )

        with TemporaryDirectory() as temp_dir:
            output_path: Path = drawing.save_svg(Path(temp_dir) / "art.svg")

            self.assertTrue(output_path.exists())
            self.assertEqual(drawing.beautiful_score(), 100)

            svg: str = output_path.read_text(encoding="utf-8")
            self.assertIn('<svg xmlns="http://www.w3.org/2000/svg"', svg)
            self.assertIn('width="320"', svg)
            self.assertIn('height="240"', svg)
            self.assertIn("<circle", svg)
            self.assertIn("<rect", svg)
            self.assertIn("<polygon", svg)

    def test_summary_matches_area_distribution_for_mixed_shapes(self) -> None:
        drawing: Drawing = Drawing()
        drawing.add(Square(x=0, y=0, side=10))
        drawing.add(Circle(x=0, y=0, radius=math.sqrt(100 / math.pi)))
        drawing.add(Triangle(x1=0, y1=0, x2=20, y2=0, x3=0, y3=10))

        summary: str = drawing.summary()

        self.assertIn("Beautiful score: 100.0/100", summary)
        self.assertIn("Square", summary)
        self.assertIn("Circle", summary)
        self.assertIn("Triangle", summary)
        self.assertIn("( 33.3%)", summary)

    def test_custom_shape_kind_flows_through_area_score_and_svg(self) -> None:
        drawing: Drawing = Drawing()
        drawing.add(Square(x=0, y=0, side=10))
        drawing.add(CustomShape())

        areas: Dict[str, float] = drawing.area_by_kind()
        svg: str = drawing.to_svg()

        self.assertEqual(areas["square"], 100)
        self.assertEqual(areas["custom"], 100)
        self.assertEqual(drawing.beautiful_score(), 100)
        self.assertIn('fill="black"', svg)

    def test_empty_drawing_can_still_be_exported(self) -> None:
        drawing: Drawing = Drawing(width=100, height=80, background="gray")

        with TemporaryDirectory() as temp_dir:
            output_path: Path = drawing.save_svg(Path(temp_dir) / "empty.svg")

            svg: str = output_path.read_text(encoding="utf-8")
            self.assertEqual(drawing.beautiful_score(), 0.0)
            self.assertIn('width="100"', svg)
            self.assertIn('height="80"', svg)
            self.assertIn('fill="gray"', svg)


if __name__ == "__main__":
    unittest.main()
