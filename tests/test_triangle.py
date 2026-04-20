"""Unit tests for the Triangle primitive."""

import unittest

from prim import Triangle


class TriangleTest(unittest.TestCase):
    """Verify Triangle area calculation and SVG rendering."""

    def test_area(self) -> None:
        triangle = Triangle(x1=1, y1=1, x2=11, y2=1, x3=1, y3=6)

        # This right triangle has base 10 and height 5, so area is 25.
        self.assertEqual(triangle.area(), 25)

    def test_area_is_not_affected_by_point_order(self) -> None:
        triangle = Triangle(x1=1, y1=6, x2=11, y2=1, x3=1, y3=1)

        # The shoelace formula returns the same area regardless of point order.
        self.assertEqual(triangle.area(), 25)

    def test_rejects_coordinates_that_are_not_bigger_than_zero(self) -> None:
        invalid_coordinates = [
            {"x1": -1, "y1": 1, "x2": 10, "y2": 1, "x3": 1, "y3": 5},
            {"x1": 1, "y1": -1, "x2": 10, "y2": 1, "x3": 1, "y3": 5},
            {"x1": 1, "y1": 1, "x2": -1, "y2": 1, "x3": 1, "y3": 5},
            {"x1": 1, "y1": 1, "x2": 10, "y2": -1, "x3": 1, "y3": 5},
            {"x1": 1, "y1": 1, "x2": 10, "y2": 1, "x3": -1, "y3": 5},
            {"x1": 1, "y1": 1, "x2": 10, "y2": 1, "x3": 1, "y3": -1},
        ]

        for coordinates in invalid_coordinates:
            with self.subTest(coordinates=coordinates):
                with self.assertRaises(ValueError):
                    Triangle(**coordinates)

    def test_rejects_message_names_invalid_coordinates(self) -> None:
        with self.assertRaisesRegex(ValueError, "Invalid: x1, y2, x3"):
            Triangle(x1=-1, y1=1, x2=10, y2=-1, x3=-1, y3=5)

    def test_svg(self) -> None:
        svg = Triangle(x1=1, y1=1, x2=11, y2=1, x3=1, y3=6, color="green").to_svg()

        # SVG polygons encode all triangle points in a single points attribute.
        self.assertIn("<polygon", svg)
        self.assertIn('points="1,1 11,1 1,6"', svg)
        self.assertIn('fill="green"', svg)

    def test_order_defaults_to_zero(self) -> None:
        triangle: Triangle = Triangle(x1=1, y1=1, x2=11, y2=1, x3=1, y3=6)

        self.assertEqual(triangle.order, 0)


if __name__ == "__main__":
    unittest.main()
