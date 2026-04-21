# PrimitiveArt API

## Drawing

```python
Drawing(width=800, height=600, background="white")
```

Main methods:

- `add(new_shape)`: Add one shape to the drawing.
- `extend(new_shapes)`: Add multiple shapes to the drawing.
- `area_by_kind()`: Return total mathematical area grouped by shape kind.
- `beautiful_score()`: Return a score from `0` to `100`.
- `summary()`: Return a readable score and area summary.
- `to_svg()`: Return the drawing as SVG text.
- `save_svg(path)`: Save the drawing as an SVG file.
- `show()`: Open the drawing as a temporary SVG in the browser.

## Circle

```python
Circle(x, y, radius, color="tomato", order=0)
```

- `x`, `y`: Center point.
- `radius`: Circle radius.
- `color`: SVG fill color.
- `order`: Render order.

## Square

```python
Square(x, y, side, color="dodgerblue", order=0)
```

- `x`, `y`: Top-left point.
- `side`: Square side length.
- `color`: SVG fill color.
- `order`: Render order.

## Triangle

```python
Triangle(x1, y1, x2, y2, x3, y3, color="gold", order=0)
```

- `x1`, `y1`: First point and drawing start point.
- `x2`, `y2`: Second point.
- `x3`, `y3`: Third point.
- `color`: SVG fill color.
- `order`: Render order.

