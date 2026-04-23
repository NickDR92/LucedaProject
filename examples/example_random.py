"""Random demo script."""

import random
from typing import Callable, List

from draw.drawing import Drawing
from prim import Circle, Square, Triangle, BaseShape

COLORS: List[str] = [
    "#2d7dd2", "#97cc04", "#f45d48", "#7b2cbf", "#f7b801", "#00a6a6", "#f46036", "#1b998b"
]


def random_circle(width: int, height: int, order: int) -> Circle:
    """Create a random circle within the draw area."""
    radius: int = random.randint(20, 80)
    return Circle(
        x=random.randint(radius, width - radius),
        y=random.randint(radius, height - radius),
        radius=radius,
        color=random.choice(COLORS),
        order=order,
    )


def random_square(width: int, height: int, order: int) -> Square:
    """Create a random square within the draw area."""
    side: int = random.randint(35, 120)
    return Square(
        x=random.randint(1, width - side),
        y=random.randint(1, height - side),
        side=side,
        color=random.choice(COLORS),
        order=order,
    )


def random_triangle(width: int, height: int, order: int) -> Triangle:
    """Create a random triangle within the draw area."""
    return Triangle(
        x1=random.randint(1, width),
        y1=random.randint(1, height),
        x2=random.randint(1, width),
        y2=random.randint(1, height),
        x3=random.randint(1, width),
        y3=random.randint(1, height),
        color=random.choice(COLORS),
        order=order,
    )


def build_random_art(shape_count: int = 12) -> Drawing:
    """Create a random draw.

    Args:
        shape_count: Number of random shapes to add.

    Returns:
        A draw filled with randomly generated shapes.
    """
    width: int = 700
    height: int = 420
    drawing: Drawing = Drawing(width=width, height=height, background="#fbfaf6")
    shape_factories: List[Callable[[int, int, int], BaseShape]] = [random_circle, random_square, random_triangle]

    for order in range(shape_count):
        factory: Callable[[int, int, int], BaseShape] = random.choice(shape_factories)
        drawing.add(factory(width, height, order))

    return drawing


if __name__ == "__main__":
    drawing = build_random_art()
    output_path = drawing.save_svg("example_random.svg")
    print(f"\nSaved random visualization to: {output_path.resolve()}")
    print(drawing.summary())
    drawing.show()
