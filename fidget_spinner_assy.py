# %%
from cadbuildr.foundation import (
    Part,
    Assembly,
    Sketch,
    Point,
    Extrusion,
    Hole,
    TFHelper,
    show,
)
from math import cos, sin, pi

from ball_bearing import BallBearing626D
from spinner_holder import SpinnerHolder

# Constants
OUTER_DIAMETER = 19
INNER_DIAMETER = 6
WIDTH = 6
SIDE_LENGTH = 100
CORNER_RADIUS = 20
BEARING_TOLERANCE = 0.4
BEARING_RADIUS = OUTER_DIAMETER / 2 + BEARING_TOLERANCE  # Radius for bearing holes
HOLE_RADIUS_DISTANCE = 30  # Distance from the center to the hole radius


class RoundedTriangularBody(Part):
    INSIDE_CIRCLE_RADIUS = 40  # Radius of the circle defining the triangular vertices
    OUTSIDE_CIRCLE_RADIUS = (
        20  # Increased radius for the arcs forming the rounded triangles
    )
    BODY_THICKNESS = 6  # Thickness of the 3D body
    BEARING_RADIUS = 19 / 2  # Radius of the bearings (diameter divided by 2)
    BEARING_CENTER_OFFSET = 50  # Offset for the center of the outside holes

    def __init__(self):
        self.create_body()
        self.add_bearing_holes()

    def create_body(self):
        """Creates the rounded triangular body."""
        sketch = Sketch(self.xy())
        pencil = sketch.pencil

        angle = 0  # Start angle for the first arc
        pencil.move_to(
            cos(angle) * self.BEARING_CENTER_OFFSET
            + sin(angle) * self.OUTSIDE_CIRCLE_RADIUS,
            sin(angle) * self.BEARING_CENTER_OFFSET
            - cos(angle) * self.OUTSIDE_CIRCLE_RADIUS,
        )

        for i in range(3):
            # Outside arc
            end_x = (
                cos(angle) * self.BEARING_CENTER_OFFSET
                - sin(angle) * self.OUTSIDE_CIRCLE_RADIUS
            )
            end_y = (
                sin(angle) * self.BEARING_CENTER_OFFSET
                + cos(angle) * self.OUTSIDE_CIRCLE_RADIUS
            )
            pencil.arc_to(end_x, end_y, -self.OUTSIDE_CIRCLE_RADIUS * 1.001)

            angle += 2 * pi / 3

            # Inside arc
            end_x = (
                cos(angle) * self.BEARING_CENTER_OFFSET
                + sin(angle) * self.OUTSIDE_CIRCLE_RADIUS
            )
            end_y = (
                sin(angle) * self.BEARING_CENTER_OFFSET
                - cos(angle) * self.OUTSIDE_CIRCLE_RADIUS
            )
            pencil.arc_to(end_x, end_y, self.INSIDE_CIRCLE_RADIUS)

        # Close the shape
        body_shape = pencil.close()

        # Extrude the body
        self.add_operation(Extrusion(body_shape, self.BODY_THICKNESS))

    def add_bearing_holes(self):
        """Adds holes for the bearings: one at the center and three on the arms of the triangle."""
        # Central hole
        center_point = Point(Sketch(self.xy()), 0, 0)
        self.add_operation(Hole(center_point, self.BEARING_RADIUS, self.BODY_THICKNESS))

        # Holes on each arm
        angle = 0
        for i in range(3):
            x = cos(angle) * self.BEARING_CENTER_OFFSET
            y = sin(angle) * self.BEARING_CENTER_OFFSET
            hole_point = Point(Sketch(self.xy()), x, y)
            self.add_operation(
                Hole(hole_point, self.BEARING_RADIUS, self.BODY_THICKNESS)
            )
            angle += 2 * pi / 3


class AssembledBearingBody(Assembly):
    def __init__(self):
        # Create the body and paint it red
        body = RoundedTriangularBody()
        body.paint("red")
        self.add_component(body)

        # Add the central bearing
        central_bearing = BallBearing626D()
        central_bearing.paint("grey")
        self.add_component(central_bearing)
        self.add_finger_holders(central_bearing, body)

        # Add the side bearings
        for i in range(3):
            bearing = BallBearing626D()  # Create a new instance for each bearing
            bearing.paint("grey")
            tf = TFHelper()
            angle = i * 2 * pi / 3  # Calculate the angle for each arm
            x_offset = cos(angle) * body.BEARING_CENTER_OFFSET
            y_offset = sin(angle) * body.BEARING_CENTER_OFFSET
            z_offset = (body.BODY_THICKNESS - bearing.HEIGHT) / 2
            tf.translate([x_offset, y_offset, z_offset])
            self.add_component(bearing, tf.get_tf())

    def add_finger_holders(self, central_bearing, body):
        # Add the top finger holder
        top_holder = SpinnerHolder()
        top_tf = TFHelper()
        z_top_offset = 3
        top_tf.translate([0, 0, z_top_offset])
        self.add_component(top_holder, top_tf.get_tf())

        # Add the bottom finger holder
        bottom_holder = SpinnerHolder()
        bottom_tf = TFHelper()
        z_bottom_offset = 3
        bottom_tf.translate([0, 0, z_bottom_offset])
        bottom_tf.rotate([1, 0, 0], pi)
        self.add_component(bottom_holder, bottom_tf.get_tf())

        top_holder.paint("pink")
        bottom_holder.paint("pink")


show(AssembledBearingBody())


# %%
