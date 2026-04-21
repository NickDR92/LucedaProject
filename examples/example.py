from prim import Circle, Square, Triangle
from drawing import Drawing


drawing = Drawing(width=700, height=420, background="#fbfaf6")
drawing.extend(
    [
        Square(x=55, y=55, side=130, color="#2d7dd2"),
        Square(x=470, y=230, side=115, color="#97cc04"),
        Circle(x=335, y=155, radius=82, color="#f45d48"),
        Circle(x=185, y=280, radius=62, color="#7b2cbf"),
        Triangle(x1=450, y1=45, x2=610, y2=105, x3=525, y3=220, color="#f7b801"),
        Triangle(x1=275, y1=265, x2=390, y2=350, x3=220, y3=380, color="#00a6a6"),
    ]
)

output_path = drawing.save_svg("example.svg")
drawing.show()

print(drawing.summary())
print(f"\nSaved visualization to: {output_path.resolve()}")
