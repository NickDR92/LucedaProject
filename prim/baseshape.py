"""Base types for ShapeArt shapes."""

from abc import ABC, abstractmethod
from typing import Tuple

from prim.constants import ShapeKind

Color = str


class BaseShape(ABC):
    """Abstract base class for all drawable shapes.

    Attributes:
        kind: The type name used for grouping and scoring.
        order: The draw order. Higher values are rendered later and appear on top.
    """

    kind: str | ShapeKind
    order: int

    @abstractmethod
    def bounding_box(self) -> Tuple[float, float, float, float]:
        """Return the smallest rectangle containing the shape.

        Returns:
            The `(min_x, min_y, max_x, max_y)` bounds of the shape.
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
