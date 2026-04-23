"""Drawing container and rendering utilities for ShapeArt.

This module exposes the `Drawing` class, which collects BaseShape objects,
calculates area distribution, computes the beauty score, and exports SVG output.
"""

from __future__ import annotations

import webbrowser
from dataclasses import dataclass, field
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Dict, Iterable, List

from prim import Color, BaseShape
from prim.constants import DEFAULT_WIDTH, DEFAULT_HEIGHT, DEFAULT_BACKGROUND


@dataclass
class Drawing:
    """A draw made from all known shapes.

    Attributes:
        width: Width of the SVG canvas in pixels.
        height: Height of the SVG canvas in pixels.
        background: Background color of the SVG canvas.
        shapes: All shapes included in the draw.
    """

    width: int = DEFAULT_WIDTH
    height: int = DEFAULT_HEIGHT
    background: Color = DEFAULT_BACKGROUND
    shapes: List[BaseShape] = field(default_factory=list)

    def add(self, new_shape: BaseShape) -> None:
        """Add one shape to the draw.

        Args:
            new_shape: The shape to add.

        Raises:
            ValueError: If the shape bounding box is outside the draw area.
        """
        self._validate_bounding_box(new_shape)
        self.shapes.append(new_shape)

    def extend(self, new_shapes: Iterable[BaseShape]) -> None:
        """Add multiple shapes to the draw.

        Args:
            new_shapes: All shapes to append to the draw.
        """
        shapes_to_add: List[BaseShape] = list(new_shapes)
        for shape in shapes_to_add:
            self._validate_bounding_box(shape=shape)
        self.shapes.extend(shapes_to_add)

    def _validate_bounding_box(self, shape: BaseShape) -> None:
        """Validate that a shape is fully inside the draw area.

        Args:
            shape: The shape to validate.

        Raises:
            ValueError: If the shape bounding box is outside the draw area.
        """
        min_x, min_y, max_x, max_y = shape.bounding_box()

        if not (0 <= min_x <= self.width and 0 <= min_y <= self.height and
                0 <= max_x <= self.width and 0 <= max_y <= self.height):
            raise ValueError(
                f"{shape.kind} bounding box ({min_x}, {min_y}, {max_x}, {max_y}) "
                f"must be inside the draw area 0 <= x <= {self.width} "
                f"and 0 <= y <= {self.height}."
            )

    def area_by_kind(self) -> Dict[str, float]:
        """Calculate total area grouped per different shape.

        Returns:
            A dictionary with total area for every shape in the draw.
        """
        areas: Dict[str, float] = {}
        for shape in self.shapes:
            areas[shape.kind] = areas.get(shape.kind, 0.0) + shape.area()
        return areas

    def beautiful_score(self) -> float:
        """Calculate how close the draw is to equal area distribution.

        A perfect score means every object kind in the draw contributes the same share of the total object area.
        For example, 3 kinds target one third each, while 4 kinds target one fourth each.

        Returns:
            A score from 0 to 100, where 100 is perfectly balanced.
        """
        areas = self.area_by_kind()
        total_area = sum(areas.values())
        if total_area == 0:
            return 0.0

        kind_count = len(areas)
        if kind_count == 1:
            return 100.0

        target_dist = 1 / kind_count
        difference = sum(abs((area / total_area) - target_dist) for area in areas.values())
        worst_dist = 2 * (kind_count - 1) / kind_count
        return round(max(0.0, 100 * (1 - difference / worst_dist)), 2)

    def summary(self) -> str:
        """Build a human-readable summary of draw area and beauty score.

        Returns:
            A multiline summary containing the beauty score and area percentages.
        """
        areas = self.area_by_kind()
        total_area = sum(areas.values())
        if total_area == 0:
            return "No shapes yet. Beautiful score: 0.0/100"

        lines = [f"Beautiful score: {self.beautiful_score()}/100"]
        for kind, area in areas.items():
            percentage = area / total_area * 100
            lines.append(f"{kind.title():8} {area:10.2f} area units ({percentage:5.1f}%)")
        return "\n".join(lines)

    def to_svg(self) -> str:
        """Render the full draw as SVG text.

        Returns:
            An SVG document string containing the background and all objects.
        """
        ordered_shapes = sorted(self.shapes, key=lambda shape: shape.order)
        body = "\n  ".join(shape.to_svg() for shape in ordered_shapes)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" '
            f'height="{self.height}" viewBox="0 0 {self.width} {self.height}">\n'
            f'  <rect width="100%" height="100%" fill="{self.background}" />\n'
            f"  {body}\n"
            "</svg>\n"
        )

    def save_svg(self, path: str | Path) -> Path:
        """Save the draw as an SVG file.

        Args:
            path: File path where the SVG should be written.

        Returns:
            The resolved `Path` object used for the output file.
        """
        output_path = Path(path)
        output_path.write_text(self.to_svg(), encoding="utf-8")
        return output_path

    def show(self) -> Path:
        """Open the draw in the default browser as a temporary SVG file.

        Returns:
            The path to the temporary SVG file.
        """
        with NamedTemporaryFile("w", suffix=".svg", delete=False, encoding="utf-8") as file:
            file.write(self.to_svg())
            output_path = Path(file.name)
        webbrowser.open(output_path.as_uri())
        return output_path
