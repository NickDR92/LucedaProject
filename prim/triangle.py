"""Triangle primitive for PrimitiveArt drawings."""

from dataclasses import dataclass, field
from typing import Tuple

from prim.baseshape import Color, BaseShape
from prim.constants import ShapeKind


@dataclass(frozen=True)
class Triangle(BaseShape):
    """A triangle object.

    Attributes:
        x1: The x-coordinate of the first point.
        y1: The y-coordinate of the first point.
        x2: The x-coordinate of the second point.
        y2: The y-coordinate of the second point.
        x3: The x-coordinate of the third point.
        y3: The y-coordinate of the third point.
        color: The SVG fill color used to draw the triangle.
        order: The draw order. Higher values are rendered later and appear on top.
        kind: The type name.
    """

    x1: float
    y1: float
    x2: float
    y2: float
    x3: float
    y3: float
    color: Color = "gold"
    order: int = 0
    kind: ShapeKind = field(init=False, default=ShapeKind.TRIANGLE)

    def __post_init__(self) -> None:
        """Validate triangle coordinates after initialization.

        Raises:
            ValueError: If any triangle coordinate is not bigger than 0.
        """
        coordinates = {
            "x1": self.x1,
            "y1": self.y1,
            "x2": self.x2,
            "y2": self.y2,
            "x3": self.x3,
            "y3": self.y3,
        }
        invalid_coordinates = [
            name for name, value in coordinates.items() if value < 0
        ]
        if invalid_coordinates:
            invalid_names = ", ".join(invalid_coordinates)
            raise ValueError(
                f"Triangle coordinates must be bigger than 0. Invalid: {invalid_names}."
            )

    def area(self) -> float:
        """Calculate the area of the triangle.

        Returns:
            The area of the triangle in square units.
        """
        return abs(
            self.x1 * (self.y2 - self.y3)
            + self.x2 * (self.y3 - self.y1)
            + self.x3 * (self.y1 - self.y2)
        ) / 2

    def bounding_box(self) -> Tuple[float, float, float, float]:
        """Return the smallest rectangle containing the triangle.

        Returns:
            The `(min_x, min_y, max_x, max_y)` bounds of the triangle.
        """
        min_x = min(self.x1, self.x2, self.x3)
        min_y = min(self.y1, self.y2, self.y3)
        max_x = max(self.x1, self.x2, self.x3)
        max_y = max(self.y1, self.y2, self.y3)

        return (min_x, min_y, max_x, max_y)

    def to_svg(self) -> str:
        """Render the triangle as an SVG element.

        Returns:
            An SVG polygon element string.
        """
        points = f"{self.x1},{self.y1} {self.x2},{self.y2} {self.x3},{self.y3}"
        return f'<polygon points="{points}" fill="{self.color}" fill-opacity="0.82" />'
