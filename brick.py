!pip install cadquery

import math
import cadquery as cq

def clutch_brick(length, width, height,
                 stud_d, stud_h, spacing,
                 nx=4, ny=2):

    # Create rectangular brick body
    brick = cq.Workplane("XY").box(
        length, width, height,
        centered=(True, True, False)
    )

    # Stud positions
    x_positions = [
        (i - (nx-1)/2) * spacing
        for i in range(nx)
    ]

    y_positions = [
        (j - (ny-1)/2) * spacing
        for j in range(ny)
    ]

    # Add cylindrical studs
    for x in x_positions:
        for y in y_positions:

            stud = (
                cq.Workplane("XY")
                .workplane(offset=height)
                .center(x, y)
                .circle(stud_d/2)
                .extrude(stud_h)
            )

            brick = brick.union(stud)

    return brick


# Dimensions in mm
length = 31.6
width = 15.8
height = 9.6

stud_d = 4.8
stud_h = 1.7
spacing = 8.0

nx = 4
ny = 2

num_studs = nx * ny

# Generate brick
brick = clutch_brick(
    length, width, height,
    stud_d, stud_h, spacing,
    nx, ny
)

# Calculate expected volume
stud_volume = math.pi * (stud_d/2)**2 * stud_h

expected = (
    length * width * height
    + num_studs * stud_volume
)

# Verify volume
actual = brick.val().Volume()

print("Expected Volume:", expected)
print("Actual Volume:", actual)
print("Number of Studs:", num_studs)

assert abs(actual - expected) < 0.5

# Export STL
cq.exporters.export(brick, "brick.stl")

print("STL file exported successfully!")
