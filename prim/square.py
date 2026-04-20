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
        order: The drawing order. Higher values are rendered later and appear on top.
        kind: The type name.
    """

    x: float
    y: float
    side: float
    color: Color = "dodgerblue"
    order: int = 0
    kind: ShapeKind = field(init=False, default=ShapeKind.SQUARE)

    def __post_init__(self) -> None:
        """Validate square dimensions after initialization.

        Raises:
            ValueError: If the side length is not positive.
        """
        if self.side <= 0:
            raise ValueError("Square side must be positive.")

    def area(self) -> float:
        """Calculate the area of the square.

        Returns:
            The area of the square in square units.
        """
        return self.side**2

    def start_point(self) -> Tuple[float, float]:
        """Return the square top-left point.

        Returns:
            The `(x, y)` top-left point.
        """
        return self.x, self.y

    def to_svg(self) -> str:
        """Render the square as an SVG element.

        Returns:
            An SVG rectangle element string.
        """
        return (
            f'<rect x="{self.x}" y="{self.y}" width="{self.side}" height="{self.side}" '
            f'fill="{self.color}" fill-opacity="0.82" />'
        )
