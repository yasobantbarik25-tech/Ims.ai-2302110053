from dataclasses import dataclass
from cadquery import func as cf

@dataclass
class CellSpec:
    r_cell: float
    h_cell: float

def make_cell(spec):
    return cf.cylinder(
        d=2 * spec.r_cell,
        h=spec.h_cell
    )

def tray(spec, n=3, rows=2,
         clearance=0.3,
         wall=4.0,
         thickness=6.0,
         depth=3.0):

    pocket_r = spec.r_cell + clearance
    pitch = 2 * pocket_r + wall

    # Tray dimensions
    length = n * pitch + wall
    width = rows * pitch + wall

    plate = cf.box(length, width, thickness)

    # Pocket geometry
    pocket = cf.cylinder(
        d=2 * pocket_r,
        h=depth + 1
    ).moved(z=thickness - depth)

    # Create n x rows pockets
    for i in range(n):
        for j in range(rows):

            x = (i - (n - 1) / 2) * pitch
            y = (j - (rows - 1) / 2) * pitch

            plate = plate - pocket.moved(x=x, y=y)

    return plate


# Battery specifications
cells = {
    "18650": CellSpec(9.0, 65.0),
    "21700": CellSpec(10.5, 70.0),
    "4680": CellSpec(23.0, 80.0),
}


if __name__ == "__main__":

    for name, spec in cells.items():

        t = tray(spec, n=3, rows=2)

        print(
            name,
            t.isValid(),
            round(t.Volume(), 1)
        )

        t.exportStl(f"tray_{name}_2row.stl")
