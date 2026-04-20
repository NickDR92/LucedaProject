"""Unit tests for the Triangle primitive."""

import unittest

from prim import Triangle


class TriangleTest(unittest.TestCase):
    """Verify Triangle area calculation and SVG rendering."""

    def test_area(self) -> None:
        triangle = Triangle(x1=0, y1=0, x2=10, y2=0, x3=0, y3=5)

        # This right triangle has base 10 and height 5, so area is 25.
        self.assertEqual(triangle.area(), 25)

    def test_area_is_not_affected_by_point_order(self) -> None:
        triangle = Triangle(x1=0, y1=5, x2=10, y2=0, x3=0, y3=0)

        # The shoelace formula returns the same area regardless of point order.
        self.assertEqual(triangle.area(), 25)

    def test_svg(self) -> None:
        svg = Triangle(x1=0, y1=0, x2=10, y2=0, x3=0, y3=5, color="green").to_svg()

        # SVG polygons encode all triangle points in a single points attribute.
        self.assertIn("<polygon", svg)
        self.assertIn('points="0,0 10,0 0,5"', svg)
        self.assertIn('fill="green"', svg)


if __name__ == "__main__":
    unittest.main()
