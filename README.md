# PrimitiveArt

PrimitiveArt is a small runtime dependency-free Python project for creating SVG
drawings from primitive shapes. It includes circles, squares, and triangles,
plus a `Drawing` container that validates shapes, renders SVG, and calculates a
beauty score based on area balance.

## What Is Included

- Shape classes for `Circle`, `Square`, and `Triangle`.
- A `Drawing` class for collecting shapes, exporting SVG, and opening drawings
  in a browser.
- Full bounding-box validation when shapes are added to a drawing.
- Shape ordering with `order`, where higher values render later and appear on
  top.
- A beauty score from `0` to `100` based on area distribution by shape kind.
- A `BaseShape` interface for custom drawable shapes.
- Built-in shape kind constants through `ShapeKind`.
- Pytest tests for primitives, drawing behavior, SVG export, custom shapes, and
  browser display behavior.

## Usage

```python
from draw import Drawing
from prim import Circle, Square, Triangle

drawing = Drawing(width=700, height=420)
drawing.add(Square(x=55, y=55, side=130, color="dodgerblue"))
drawing.add(Circle(x=335, y=155, radius=82, color="tomato"))
drawing.add(Triangle(x1=450, y1=45, x2=610, y2=105, x3=525, y3=220, color="gold"))

print(drawing.summary())
drawing.save_svg("my_art.svg")
```

## Validation

Primitive coordinates must be non-negative. Dimensions must be positive.

- `Circle`: `x` and `y` must be `>= 0`; `radius` must be `> 0`.
- `Square`: `x` and `y` must be `>= 0`; `side` must be `> 0`.
- `Triangle`: all point coordinates must be `>= 0`.

When a shape is added to a `Drawing`, its full bounding box must fit inside the
drawing area:

```text
0 <= min_x <= width
0 <= min_y <= height
0 <= max_x <= width
0 <= max_y <= height
```

This means a circle center can be inside the drawing while the circle is still
rejected if its radius makes the edge extend outside the canvas.

## Beautiful Score

The beauty score measures how close the drawing is to equal area distribution
between the shape kinds that are present. It returns a number from `0` to `100`.

- A perfectly balanced drawing scores `100`.
- One present shape kind scores `100` when it has area.
- An empty drawing scores `0`.
- Three present shape kinds target about `33.33%` each.
- Four present shape kinds target `25%` each.

The score uses mathematical shape area. It does not subtract overlaps between
rendered shapes.

## Rendering Rules

Shapes are rendered in ascending `order`. Higher `order` values are drawn later,
so they appear on top when shapes overlap. If shapes have the same `order`, they
keep the order in which they were added to the drawing.

## Project Structure

```text
draw/
  drawing.py          Drawing container, validation, SVG rendering, and scoring
  __init__.py         Public drawing package exports
prim/
  baseshape.py        BaseShape interface and Color alias
  circle.py           Circle primitive
  square.py           Square primitive
  triangle.py         Triangle primitive
  constants.py        Defaults and ShapeKind enum
examples/             Example scripts and generated SVG output
tests/                Pytest test suite
pytest.ini            Pytest configuration
README.md             Project overview
API.md                API reference
```

See [API.md](API.md) for detailed class and method documentation.
