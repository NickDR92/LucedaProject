"""Base types for PrimitiveArt primitives."""

from abc import ABC, abstractmethod
from typing import Tuple

from prim.constants import ShapeKind

Color = str


class BaseShape(ABC):
    """Abstract base class for all drawable shapes.

    Attributes:
        kind: The type name used for grouping and scoring.
        order: The drawing order. Higher values are rendered later and appear on top.
    """

    kind: str | ShapeKind
    order: int

    @abstractmethod
    def start_point(self) -> Tuple[float, float]:
        """Return the point that must be inside the drawing area.

        Returns:
            The `(x, y)` point used to place the shape in the drawing.
        """
        raise NotImplementedError

    @abstractmethod
    def area(self) -> float:
        """Calculate the mathematical area of the object.

        Returns:
            The area covered by the object in square units.
        """
        raise NotImplementedError

    @abstractmethod
    def to_svg(self) -> str:
        """Render the object as an SVG element.

        Returns:
            An SVG element string representing the object.
        """
        raise NotImplementedError
