"""Triangle primitive for PrimitiveArt drawings."""

from dataclasses import dataclass, field

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
        order: The drawing order. Higher values are rendered later and appear on top.
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

    def to_svg(self) -> str:
        """Render the triangle as an SVG element.

        Returns:
            An SVG polygon element string.
        """
        points = f"{self.x1},{self.y1} {self.x2},{self.y2} {self.x3},{self.y3}"
        return f'<polygon points="{points}" fill="{self.color}" fill-opacity="0.82" />'
