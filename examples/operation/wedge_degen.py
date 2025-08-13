import os
from classy_blocks.util import functions as f

import classy_blocks as cb

# direction 0 - axial
# direction 1 - radial
# direction 2 - circumferential

mesh = cb.Mesh()

L_string=11999.95
L_Wellbore=12000
ID=0.0508
OD=0.0762
WellBore_OD=0.1075

core = cb.Face(
    # points
    [[0, 0, 0],
     [L_string, 0, 0],
     [L_string, ID, 0], 
     [0, ID, 0]],
    # edges
    [None, None, None, None],
)

#core_wedge = cb.Wedge(core)
core_wedge=cb.Revolve(core,angle=f.deg2rad(5),axis=[1,0,0],origin=[0,0,0])

for i in range(4):
    print(core_wedge.bottom_face.points[i].position[1], -core_wedge.top_face.points[i].position[1])

#core_wedge.set_outer_patch("fluid_pipe_ID")
#wedge.set_inner_patch("String_ID")

#core_wedge.set_patch("left", "inlet")
#core_wedge.set_patch("right", "core_master")

core_wedge.chop(1, start_size=2.1e-5, c2c_expansion=1.2) # core inflation layer
core_wedge.chop(0, length_ratio=0.5, start_size=0.01, c2c_expansion=1.05, preserve="start_size")
core_wedge.chop(0, length_ratio=0.5, end_size=0.001, c2c_expansion=1 / 1.05, preserve="end_size")
core_wedge.chop(2, count=1)

mesh.add(core_wedge)

'''
bha_core = cb.Face(
    # points
    [[L_string, 0, 0],
     [L_Wellbore, 0, 0],
     [L_Wellbore, ID, 0], 
     [L_string, ID, 0]],
    # edges
    [None, None, None, None],
)

bha_core_wedge = cb.Wedge(bha_core)
bha_core_wedge.set_outer_patch("bha_core_master")
#wedge.set_inner_patch("String_ID")

bha_core_wedge.set_patch("left", "core_slave")
bha_core_wedge.set_patch("right", "well_bottom")

bha_core_wedge.chop(1, start_size=2.1e-5, c2c_expansion=1.2) # core inflation layer
bha_core_wedge.chop(0, length_ratio=0.5, start_size=2.1e-5, c2c_expansion=1.05, preserve="start_size")
bha_core_wedge.chop(0, length_ratio=0.5, end_size=2.1e-5, c2c_expansion=1 / 1.05, preserve="end_size")

mesh.add(bha_core_wedge)

mesh.merge_patches("core_master", "core_slave")
'''

mesh.write(os.path.join("system", "fluid","blockMeshDict"), debug_path="debug.vtk")