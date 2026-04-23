"""Square primitive for PrimitiveArt drawings."""

from dataclasses import dataclass, field
from typing import Tuple

from prim.baseshape import Color, BaseShape
from prim.constants import ShapeKind


@dataclass(frozen=True)
class Square(BaseShape):
    """A square object.

    Attributes:
        x: The x-coordinate of the square's top-left corner.
        y: The y-coordinate of the square's top-left corner.
        side: The side length of the square.
        color: The SVG fill color used to draw the square.
        order: The draw order. Higher values are rendered later and appear on top.
        kind: The type name.
    """

    x: float
    y: float
    side: float
    color: Color = "dodgerblue"
    order: int = 0
    kind: ShapeKind = field(init=False, default=ShapeKind.SQUARE)

    def __post_init__(self) -> None:
        """Validate square coordinates and dimensions after initialization.

        Raises:
            ValueError: If coordinates or side length are not positive.
        """
        invalid_coordinates = []
        if self.x < 0:
            invalid_coordinates.append("x")
        if self.y < 0:
            invalid_coordinates.append("y")
        if invalid_coordinates:
            invalid_names = ", ".join(invalid_coordinates)
            raise ValueError(
                f"Square coordinates must be bigger than 0. Invalid: {invalid_names}."
            )

        if self.side <= 0:
            raise ValueError("Square side must be positive.")

    def area(self) -> float:
        """Calculate the area of the square.

        Returns:
            The area of the square in square units.
        """
        return self.side**2

    def bounding_box(self) -> Tuple[float, float, float, float]:
        """Return the smallest rectangle containing the square.

        Returns:
            The `(min_x, min_y, max_x, max_y)` bounds of the square.
        """
        return (self.x, self.y, self.x + self.side, self.y + self.side)

    def to_svg(self) -> str:
        """Render the square as an SVG element.

        Returns:
            An SVG rectangle element string.
        """
        return (
            f'<rect x="{self.x}" y="{self.y}" width="{self.side}" height="{self.side}" '
            f'fill="{self.color}" fill-opacity="0.82" />'
        )
