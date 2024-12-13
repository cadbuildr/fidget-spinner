from cadbuildr.foundation import Part, Lathe, Sketch, Axis, Line, Point, show


class SpinnerHolder(Part):
    # Dimensions for the holder
    FINGER_RADIUS = 10  # Radius for the finger grip
    BEARING_LIP_RADIUS = 3.5  # Radius for the lip that sits around the ball bearing
    BEARING_FIT_RADIUS = (
        3 - 0.1
    )  # Radius for the fitting to the inner diameter of the ball bearing (with clearance)
    HOLDER_HEIGHT = 5  # Total height of the holder
    BEARING_LIP_HEIGHT = 1  # Height of the lip around the bearing
    FITTING_HEIGHT = 3  # Height of the fitting portion inside the ball bearing

    def __init__(self):
        axis, shape = self.get_sketch()
        # Perform a lathe operation based on the sketch
        self.add_operation(Lathe(shape, axis))

    def get_sketch(self):
        sketch = Sketch(self.xz())
        pencil = sketch.pencil

        # Start at the center of rotation
        pencil.line_to(self.BEARING_FIT_RADIUS, 0)
        # Define the fitting portion inside the ball bearing
        pencil.line(0, self.FITTING_HEIGHT)

        # # Transition to the lip for the ball bearing
        pencil.line(self.BEARING_LIP_RADIUS - self.BEARING_FIT_RADIUS, 0)
        pencil.line(0, self.BEARING_LIP_HEIGHT)

        # # Extend to the finger grip
        pencil.line(self.FINGER_RADIUS - self.BEARING_LIP_RADIUS, 0)
        pencil.line(
            0, self.HOLDER_HEIGHT - self.BEARING_LIP_HEIGHT - self.FITTING_HEIGHT
        )

        pencil.line(-self.FINGER_RADIUS, 0)

        # Close the shape to the origin
        shape = pencil.close()
        # Create the axis of rotation for the lathe
        axis = Axis(Line(Point(sketch, 0, 0), Point(sketch, 0, self.HOLDER_HEIGHT)))

        return axis, shape


if __name__ == "__main__":
    holder = SpinnerHolder()
    show(holder)
