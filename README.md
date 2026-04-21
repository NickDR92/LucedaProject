# PrimitiveArt

A small dependency-free prototype for creating primitive art drawings with circles,
squares, and triangles. Users can define shapes in Python, render a drawing to
SVG, and calculate how balanced the drawing is by shape area.

## What Is Included

- Shape classes for circles, squares, and triangles.
- A `Drawing` class that stores shapes and renders them as SVG.
- A beauty score based on the area distribution between the shape kinds present
  in the drawing.
- Shape ordering with `order`, where higher values render later and appear on top.
- Start-point validation to ensure each shape starts inside the drawing area.
- Shape coordinate validation to keep all shape coordinates bigger than `0`.
- Constants for built-in shape kinds via `ShapeKind`.
- Unit and integration tests for shapes, drawings, SVG export, and custom shape
  behavior.

## Usage

```python
from prim import Circle, Square, Triangle
from draw import Drawing

drawing = Drawing(width=700, height=420)
drawing.add(Square(x=55, y=55, side=130, color="dodgerblue"))
drawing.add(Circle(x=335, y=155, radius=82, color="tomato"))
drawing.add(Triangle(x1=450, y1=45, x2=610, y2=105, x3=525, y3=220, color="gold"))

print(drawing.summary())
drawing.save_svg("my_art.svg")
```

See [API.md](API.md) for the shape API and run commands.

## Validation

Shape coordinates must be bigger than `0`.

- `Circle`: `x`, `y`, and `radius` must be positive.
- `Square`: `x`, `y`, and `side` must be positive.
- `Triangle`: `x1`, `y1`, `x2`, `y2`, `x3`, and `y3` must be positive.

When a shape is added to a `Drawing`, its start point must also be inside the
drawing area. The full shape is allowed to extend outside the SVG canvas.

## Beautiful Score

The beauty score is a number from `0` to `100`. A score of `100` means every
shape kind in the drawing contributes the same share of the total shape area.

Examples:

- 3 shape kinds target about `33.33%` each.
- 4 shape kinds target `25%` each.
- 1 shape kind scores `100` when it has area.
- An empty drawing scores `0`.

The score uses mathematical shape area. It does not subtract overlap between
shapes.

## Rendering Rules

Shapes are rendered in ascending `order`. Higher `order` values are drawn later,
so they appear on top when shapes overlap. If shapes have the same `order`, they
keep the order in which they were added to the drawing.

## Project Structure

```text
main.py               Demo script
example.py            Example drawing script
example_order.py      Example showing shape render order
example_random.py     Random drawing example
drawing.py            Drawing container, SVG rendering, and beauty score
prim/                 Shape classes, base shape, and constants
tests/                Unit and integration tests
README.md             Project documentation
API.md                API reference and run commands
```
