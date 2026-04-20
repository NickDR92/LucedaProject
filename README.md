# PrimitiveArt

A small dependency-free prototype for creating PrimitiveArt drawings with circles,
squares, and triangles.

## Usage

```python
from prim import Circle, Square, Triangle
from drawing import Drawing

drawing = Drawing(width=700, height=420)
drawing.add(Square(55, 55, 130, "dodgerblue"))
drawing.add(Circle(335, 155, 82, "tomato"))
drawing.add(Triangle(450, 45, 610, 105, 525, 220, "gold"))

print(drawing.summary())
drawing.save_svg("my_art.svg")
```

Run the demo:

```powershell
.venv\Scripts\python.exe main.py
```

Run tests:

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Beautiful Score

The score is `0-100`. A score of `100` means circles, squares, and triangles each
contribute exactly one third of the total primitive area. The current prototype
uses mathematical primitive area, not pixel coverage after overlap.

## Prototype To Product

- Add a packaged public API, docs, examples, and semantic versioning.
- Decide how overlap should be treated: mathematical area or true visible pixels.
- Add richer validation, error messages, and a stable file format.
- Add PNG/PDF export, interactive preview, and test coverage for edge cases.
- Add CI, formatting, type checks, and performance benchmarks.

## Scalability

The current SVG renderer is fine for small and medium drawings. For larger art:

- Stream SVG output instead of building one large string.
- Use spatial indexes for hit-testing or visible-area calculations.
- Use raster/vector backends such as Pillow, Cairo, Skia, or browser canvas when
  true pixel coverage or high-volume rendering matters.

## Future PrimitiveArtRounded

Rounded variants can be introduced by adding new primitive classes or renderer
strategies while keeping the `Primitive` interface: `area()` and `to_svg()`.
For example, `RoundedSquare` could preserve the same area semantics while
rendering with SVG `rx` and `ry` attributes.
