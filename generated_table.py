from cadbuildr.foundation import *
from typing import ClassVar

class SquareTable(Part):
    """A square table with 4 legs."""
    
    def __init__(self):
        super().__init__()
        
        # Dimensions
        table_top_size: float = 800.0
        table_top_thickness: float = 40.0
        leg_width: float = 60.0
        leg_height: float = 700.0
        leg_inset: float = 50.0
        
        # Create table top
        top_sketch = Sketch(self.xy())
        top_center = Point(top_sketch, 0, 0)
        top_square = Square.from_center_and_side(top_center, table_top_size)
        top_extrusion = Extrusion(top_square, table_top_thickness, start=leg_height)
        self.add_operation(top_extrusion)
        
        # Create 4 legs at corners
        leg_positions = [
            (table_top_size/2 - leg_inset - leg_width/2, table_top_size/2 - leg_inset - leg_width/2),
            (-table_top_size/2 + leg_inset + leg_width/2, table_top_size/2 - leg_inset - leg_width/2),
            (-table_top_size/2 + leg_inset + leg_width/2, -table_top_size/2 + leg_inset + leg_width/2),
            (table_top_size/2 - leg_inset - leg_width/2, -table_top_size/2 + leg_inset + leg_width/2),
        ]
        
        for x, y in leg_positions:
            leg_sketch = Sketch(self.xy())
            leg_center = Point(leg_sketch, x, y)
            leg_square = Square.from_center_and_side(leg_center, leg_width)
            leg_extrusion = Extrusion(leg_square, leg_height, start=0)
            self.add_operation(leg_extrusion)

if __name__ == "__main__":
    show(SquareTable())
