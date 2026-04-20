"""Unit tests for the Circle primitive."""

import math
import unittest

from prim import Circle


class CircleTest(unittest.TestCase):
    """Verify Circle area calculation, validation, and SVG rendering."""

    def test_area(self) -> None:
        circle = Circle(x=10, y=20, radius=5)

        # Circle area is pi * radius squared.
        self.assertEqual(circle.area(), math.pi * 25)

    def test_rejects_non_positive_radius(self) -> None:
        with self.assertRaises(ValueError):
            Circle(x=10, y=20, radius=0)

    def test_svg(self) -> None:
        svg = Circle(x=10, y=20, radius=5, color="red").to_svg()

        # The SVG should preserve the user-provided geometry and color.
        self.assertIn("<circle", svg)
        self.assertIn('cx="10"', svg)
        self.assertIn('cy="20"', svg)
        self.assertIn('r="5"', svg)
        self.assertIn('fill="red"', svg)

    def test_order_defaults_to_zero(self) -> None:
        circle: Circle = Circle(x=10, y=20, radius=5)

        self.assertEqual(circle.order, 0)


if __name__ == "__main__":
    unittest.main()
