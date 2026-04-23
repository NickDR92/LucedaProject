# PrimitiveArt API

## Imports

```python
from draw import Drawing
from prim import BaseShape, Circle, Color, ShapeKind, Square, Triangle
```

## Drawing

```python
Drawing(width=800, height=600, background="white", shapes=[])
```

Attributes:

- `width`: SVG canvas width.
- `height`: SVG canvas height.
- `background`: SVG background fill color.
- `shapes`: List of shapes currently in the drawing.

### `add(new_shape)`

Add one shape to the drawing.

Raises:

- `ValueError`: If the shape bounding box is outside the drawing area.

### `extend(new_shapes)`

Add multiple shapes to the drawing.

The method validates every shape before appending any of them. If one shape is
invalid, no shapes from that `extend()` call are added.

Raises:

- `ValueError`: If any shape bounding box is outside the drawing area.

### `area_by_kind()`

Return total mathematical area grouped by shape kind.

```python
{"square": 100.0, "circle": 314.1592653589793}
```

### `beautiful_score()`

Return a score from `0` to `100`.

The score compares each present shape kind against an equal target share of the
total area. Empty drawings return `0.0`. Drawings with one present kind return
`100.0`.

### `summary()`

Return a multiline text summary containing the beauty score and area percentage
per shape kind.

### `to_svg()`

Return the full SVG document as a string.

Shapes are sorted by ascending `order`; higher values are rendered later and
appear on top.

### `save_svg(path)`

Save the SVG document to `path`.

Returns:

- A `Path` object for the written file.

### `show()`

Write the drawing to a temporary SVG file and open it in the default browser.

Returns:

- A `Path` object for the temporary SVG file.

## Shape Interface

All drawable shapes implement `BaseShape`.

Required attributes:

- `kind`: A string or `ShapeKind` used for grouping area and scoring.
- `order`: Integer render order.

Required methods:

- `area() -> float`
- `bounding_box() -> tuple[float, float, float, float]`
- `to_svg() -> str`

The `bounding_box()` tuple is:

```python
(min_x, min_y, max_x, max_y)
```

`Drawing.add()` and `Drawing.extend()` use this bounding box to ensure the full
shape fits inside the canvas.

## Circle

```python
Circle(x, y, radius, color="tomato", order=0)
```

Arguments:

- `x`, `y`: Center point.
- `radius`: Circle radius.
- `color`: SVG fill color.
- `order`: Render order.

Methods:

- `area()`: Returns `pi * radius ** 2`.
- `bounding_box()`: Returns `(x - radius, y - radius, x + radius, y + radius)`.
- `to_svg()`: Returns an SVG `<circle>` element.

Validation:

- `x` and `y` must be `>= 0`.
- `radius` must be `> 0`.

## Square

```python
Square(x, y, side, color="dodgerblue", order=0)
```

Arguments:

- `x`, `y`: Top-left point.
- `side`: Square side length.
- `color`: SVG fill color.
- `order`: Render order.

Methods:

- `area()`: Returns `side ** 2`.
- `bounding_box()`: Returns `(x, y, x + side, y + side)`.
- `to_svg()`: Returns an SVG `<rect>` element.

Validation:

- `x` and `y` must be `>= 0`.
- `side` must be `> 0`.

## Triangle

```python
Triangle(x1, y1, x2, y2, x3, y3, color="gold", order=0)
```

Arguments:

- `x1`, `y1`: First point.
- `x2`, `y2`: Second point.
- `x3`, `y3`: Third point.
- `color`: SVG fill color.
- `order`: Render order.

Methods:

- `area()`: Returns the triangle area using the shoelace formula.
- `bounding_box()`: Returns the minimum rectangle containing all three points.
- `to_svg()`: Returns an SVG `<polygon>` element.

Validation:

- All point coordinates must be `>= 0`.

## ShapeKind

```python
ShapeKind.CIRCLE    # "circle"
ShapeKind.SQUARE    # "square"
ShapeKind.TRIANGLE  # "triangle"
```

Built-in primitives use `ShapeKind` values for `kind`. Custom shapes can use any
string `kind`.

## Custom Shapes

Custom shapes can participate in rendering, area scoring, and validation by
implementing `BaseShape`.

```python
from prim import BaseShape


class CustomShape(BaseShape):
    kind = "custom"
    order = 0

    def area(self) -> float:
        return 100

    def bounding_box(self) -> tuple[float, float, float, float]:
        return 10, 10, 20, 20

    def to_svg(self) -> str:
        return '<rect x="10" y="10" width="10" height="10" fill="black" />'
```
