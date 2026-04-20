"""Circle primitive for PrimitiveArt drawings."""

import math
from dataclasses import dataclass, field
from typing import Tuple

from prim.baseshape import Color, BaseShape
from prim.constants import ShapeKind


@dataclass(frozen=True)
class Circle(BaseShape):
    """A circle object.

    Attributes:
        x: The x-coordinate of the circle center.
        y: The y-coordinate of the circle center.
        radius: The radius of the circle.
        color: The SVG fill color used to draw the circle.
        order: The drawing order. Higher values are rendered later and appear on top.
        kind: The type name.
    """

    x: float
    y: float
    radius: float
    color: Color = "tomato"
    order: int = 0
    kind: ShapeKind = field(init=False, default=ShapeKind.CIRCLE)

    def __post_init__(self) -> None:
        """Validate circle coordinates and dimensions after initialization.

        Raises:
            ValueError: If coordinates or radius are not positive.
        """
        invalid_coordinates = []
        if self.x < 0:
            invalid_coordinates.append("x")
        if self.y < 0:
            invalid_coordinates.append("y")
        if invalid_coordinates:
            invalid_names = ", ".join(invalid_coordinates)
            raise ValueError(
                f"Circle coordinates must be bigger than 0. Invalid: {invalid_names}."
            )

        if self.radius <= 0:
            raise ValueError("Circle radius must be positive.")

    def area(self) -> float:
        """Calculate the area of the circle.

        Returns:
            The area of the circle in square units.
        """
        return math.pi * self.radius**2

    def start_point(self) -> Tuple[float, float]:
        """Return the circle center point.

        Returns:
            The `(x, y)` center point.
        """
        return self.x, self.y

    def to_svg(self) -> str:
        """Render the circle as an SVG element.

        Returns:
            An SVG circle element string.
        """
        return (
            f'<circle cx="{self.x}" cy="{self.y}" r="{self.radius}" '
            f'fill="{self.color}" fill-opacity="0.82" />'
        )
