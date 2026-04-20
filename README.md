# PrimitiveArt

A small dependency-free prototype for creating primitive art drawings with circles,
squares, and triangles. Users can define shapes in Python, render a drawing to
SVG, and calculate how balanced the drawing is by shape area.

## What Is Included

- Shape classes for circles, squares, and triangles.
- A `Drawing` class that stores shapes and renders them as SVG.
- A beauty score based on the area distribution between the shape kinds present
  in the drawing.
- Constants for built-in shape kinds via `ShapeKind`.
- Unit tests for each shape class and drawing-level behavior.

## Usage

```python
from prim import Circle, Square, Triangle
from drawing import Drawing

drawing = Drawing(width=700, height=420)
drawing.add(Square(x=55, y=55, side=130, color="dodgerblue"))
drawing.add(Circle(x=335, y=155, radius=82, color="tomato"))
drawing.add(Triangle(x1=450, y1=45, x2=610, y2=105, x3=525, y3=220, color="gold"))

print(drawing.summary())
drawing.save_svg("my_art.svg")
```

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

## Project Structure

```text
main.py              Demo script
drawing.py           Drawing container, SVG rendering, and beauty score
prim/                Shape classes, base shape, and constants
tests/               Unit tests
README.md            Project documentation
```
