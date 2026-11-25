!pip install cadquery
from cadquery import func as cf

plate = cf.box(80, 50, 10)          # length, width, height (mm)
hole = cf.cylinder(d=20, h=10)      # diameter, height
part = plate - hole                 # subtract = drill!

print("Valid:", part.isValid())
print("Volume:", round(part.Volume(),1),"mm^3")
part.exportStl("plate.stl")
print("STL file generate successfully!")
