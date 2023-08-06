

import zerogravity.zerog as g

# const
tf_BLACK = (0, 0, 0)
tf_BLUE = (0, 0, 1)
tf_CYAN = (0, 0.5, 0.5)
tf_GREEN = (0, 1, 0)
tf_WHITE = (1, 1, 1)
tf_YELLOW = (0.5, 0.5, 0)
tf_ORANGE = (0.64, 0.32, 0.04)
tf_RED = (1, 0, 0)

# get blender
o_zerog = g.zeroGblender()

# add meshes
o_torus = g.Mesh(
    relative_path_file="stl/torus.stl",
    diffuse_color=tf_ORANGE,
    visibility_key="NINE"
)
o_zerog.add(o_torus)

o_grid = g.Mesh(
    relative_path_file="stl/grid.stl",
    diffuse_color=tf_GREEN
)
o_zerog.add(o_grid)

# add navigation
o_navi = g.Navigation()
o_zerog.add(o_navi)

# add tourch
o_torch = g.Torch()
o_zerog.add(o_torch)

# add global position system
o_gps = g.GlobalPositionSystem(key="ONE")
o_zerog.add(o_gps)

# render game for a specific os
#o_zerog.zerog_os = "Windows"
#o_zerog.blend_game(b_debug=True)

#o_zerog.zerog_os = "Darwin"
#o_zerog.blend_game(b_debug=True)

#o_zerog.zerog_os = "Linux"
#o_zerog.blend_game(b_debug=True)

# render game for host os
o_zerog.blend_game(b_debug=True)
