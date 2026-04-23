"""Constants used by ShapeArt shape classes."""

from enum import StrEnum

DEFAULT_WIDTH: int = 800
DEFAULT_HEIGHT: int = 600
DEFAULT_BACKGROUND: str = "white"


class ShapeKind(StrEnum):
    """Built-in shape kind names.

    These values describe the shape types shipped by the framework. Custom
    shapes can still use their own string `kind` values.
    """

    CIRCLE = "circle"
    SQUARE = "square"
    TRIANGLE = "triangle"
