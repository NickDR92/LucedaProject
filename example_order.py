from prim import Circle, Square, Triangle
from drawing import Drawing


def build_demo_art() -> Drawing:
    # art = Drawing(width=700, height=420, background="#fbfaf6")  # Fail
    art = Drawing(width=1000, height=750, background="#fbfaf6")  # Pass

    art.extend(
        [
            Square(x=155, y=155, side=130, color="#2d7dd2", order=1),
            Square(x=670, y=430, side=115, color="#97cc04"),
            Circle(x=635, y=255, radius=82, color="#f45d48"),
            Circle(x=285, y=480, radius=62, color="#7b2cbf"),
            Square(x=55, y=55, side=130, color="#2d7dd2", order=1),
            Square(x=470, y=230, side=115, color="#97cc04"),
            Circle(x=335, y=155, radius=82, color="#f45d48"),
            Circle(x=185, y=280, radius=62, color="#7b2cbf"),
            Triangle(x1=450, y1=45, x2=610, y2=105, x3=525, y3=220, color="#f7b801"),
            Triangle(x1=275, y1=265, x2=390, y2=350, x3=220, y3=380, color="#00a6a6", order=10),
        ]
    )

    return art


if __name__ == "__main__":
    drawing = build_demo_art()
    output_path = drawing.save_svg("primitive_art_demo.svg")
    drawing.show()

    print(drawing.summary())
    print(f"\nSaved visualization to: {output_path.resolve()}")
