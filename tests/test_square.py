"""Unit tests for the Square primitive."""

import unittest

from prim import Square


class SquareTest(unittest.TestCase):
    """Verify Square area calculation, validation, and SVG rendering."""

    def test_area(self) -> None:
        square = Square(x=10, y=20, side=5)

        # Square area is side squared.
        self.assertEqual(square.area(), 25)

    def test_rejects_non_positive_side(self) -> None:
        with self.assertRaises(ValueError):
            Square(x=10, y=20, side=0)

    def test_rejects_coordinates_that_are_not_bigger_than_zero(self) -> None:
        invalid_coordinates = [
            {"x": -1, "y": 20, "side": 5},
            {"x": 10, "y": -1, "side": 5},
        ]

        for coordinates in invalid_coordinates:
            with self.subTest(coordinates=coordinates):
                with self.assertRaises(ValueError):
                    Square(**coordinates)

    def test_rejects_message_names_invalid_coordinates(self) -> None:
        with self.assertRaisesRegex(ValueError, "Invalid: x, y"):
            Square(x=-1, y=-1, side=5)

    def test_svg(self) -> None:
        svg = Square(x=10, y=20, side=5, color="blue").to_svg()

        # Squares are rendered as SVG rectangles with equal width and height.
        self.assertIn("<rect", svg)
        self.assertIn('x="10"', svg)
        self.assertIn('y="20"', svg)
        self.assertIn('width="5"', svg)
        self.assertIn('height="5"', svg)
        self.assertIn('fill="blue"', svg)

    def test_order_defaults_to_zero(self) -> None:
        square: Square = Square(x=10, y=20, side=5)

        self.assertEqual(square.order, 0)


if __name__ == "__main__":
    unittest.main()
