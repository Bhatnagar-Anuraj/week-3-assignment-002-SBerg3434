"""
DIGM 131 - Assignment 3: Function Library (main_scene.py)
==========================================================

OBJECTIVE:
    Use the functions you wrote in scene_functions.py to build a complete
    scene. This file demonstrates how importing and reusing functions makes
    scene creation clean and readable.

REQUIREMENTS:
    1. Import scene_functions (the module you completed).
    2. Call each of your 5+ functions at least once.
    3. Use place_in_circle with at least one of your create functions.
    4. The final scene should contain at least 15 objects total.
    5. Comment your code explaining what you are building.

GRADING CRITERIA:
    - [30%] All 5+ functions from scene_functions.py are called.
    - [25%] place_in_circle is used at least once.
    - [20%] Scene contains 15+ objects and looks intentional.
    - [15%] Code is well-commented.
    - [10%] Script runs without errors from top to bottom.
"""

import maya.cmds as cmds

import importlib
import scene_functions as sf
importlib.reload(sf) 

import random

# ---------------------------------------------------------------------------
# Scene Setup
# ---------------------------------------------------------------------------
cmds.file(new=True, force=True)

# Create a ground plane.
ground = cmds.polyPlane(name="ground", width=200, height=200,
                        subdivisionsX=1, subdivisionsY=1)[0]

    
def apply_color(nodes,r,g,b,shader_name="colorShader"):
    """Apply a Lambert shader with the given RGB color to all listed nodes."""
    shader = cmds.shadingNode("lambert", asShader=True,name=shader_name)
    cmds.setAttr(shader+".color",r,g,b,type="double3")
    for node in nodes:
        cmds.select(node)
        cmds.hyperShade(assign=shader)
    return shader
    
def create_city_block(building_row_count=3, building_column_count=3, position=(0,0,0)):

    #Grid Pattern Parameters
    rows = building_row_count
    cols = building_column_count
    building_count = building_row_count * building_column_count
    grid_spacing = 66 / 2.84
    building_height_minimum = 26
    building_height_maximum = 50
    
    #Store references for the base pillars
    all_buildings = []
    
    #Nested loop allows for a simple grid of polyCubes to be created; this forms the base of the temple
    
    

    #Nested loop allows for a simple grid of polyCubes to be created; this forms the base of the temple
    
    for row in range(rows):
        for col in range(cols):         
            x_grid = col * grid_spacing
            z_grid = row * grid_spacing  # offset behind the columns
            building_height_random = random.randint(building_height_minimum,building_height_maximum)
            
            building = sf.create_building(building_width=16,building_height=building_height_random,building_depth=16,position=(x_grid,0,z_grid))
            
            #Add the newly created pillar to the reference list established before the loop
            all_buildings.append(building)
     
    city_block_group = cmds.group(all_buildings, name="city_block_grp")
    cmds.move(position[0],position[1],position[2],city_block_group)
    
    
def create_lamp_post_line(y_rotation=0,position=(0,0,0)):            
    lamp_post_count = 7
    post_spacing = 10
    
    lamp_posts = []
    
    for i in range(lamp_post_count):
        lamp_post = sf.create_lamp_post()
        cmds.move(i * post_spacing,0,0, lamp_post) 
        lamp_posts.append(lamp_post)     
            
    lampost_group = cmds.group(lamp_posts, name="lamp_posts_grp")
    cmds.move(position[0],position[1],position[2],lampost_group)
    cmds.rotate(0,y_rotation,0,lampost_group)

def create_park(position=(0,0,0)):
    sf.place_in_circle(create_tree,count=10,radius=12)
   
    fence_group = sf.create_fence(length=32,post_count=10,position=((-16),0,16))
    
    for i in range(3):
        cmds.duplicate(fence_group)
    
    cmds.move((-16),0,(-16),"fence_grp1")
    
    cmds.rotate(0,90,0,"fence_grp2")
    cmds.rotate(0,90,0,"fence_grp3")
    cmds.move((0),0,(0),"fence_grp2")
    cmds.move((-32),0,(0),"fence_grp3")
    
    fence_full_group = cmds.group("fence_grp","fence_grp1","fence_grp2","fence_grp3",name="fence_full_grp")
    
    cmds.move(position[0],position[1],position[2],fence_full_group)
    
        
def build_full_scene():
    create_park()
    
    block_1 = create_city_block(position=(25,0,35))
    block_2 = create_city_block(position=((-75),0,35)) 
    block_3 = create_city_block(position=((-75),0,(-85))) 
    block_4 = create_city_block(position=(25,0,(-85)))
    apply_color(block_1, 0.55, 0.55, 0.65, shader_name="buildings1_mat")
    apply_color(block_2, 0.6, 0.5, 0.45, shader_name="buildings2_mat")
    apply_color(block_3, 0.55, 0.55, 0.65, shader_name="buildings3_mat")
    apply_color(block_4, 0.6, 0.5, 0.45, shader_name="buildings4_mat")  
    
    lampost_line_1 = create_lamp_post_line(position=(22,0,20))
    lampost_line_2 = create_lamp_post_line(position=(22,0,(-20))) 
    lampost_line_3 = create_lamp_post_line(position=((-82),0,20))
    lampost_line_4 = create_lamp_post_line(position=((-82),0,(-20)))  
    lined_street_group = cmds.group("lamp_posts_grp","lamp_posts_grp1","lamp_posts_grp2","lamp_posts_grp3", name="lined_street_1") 
    
    cmds.duplicate(lined_street_group)
    cmds.rotate(0,90,0,"lined_street_2")
    
build_full_scene()
# ---------------------------------------------------------------------------
# TODO: Build your scene below by calling functions from scene_functions.
#
# Example calls (uncomment and modify once your functions are implemented):
#
#   sf.create_building(width=5, height=10, depth=5, position=(-10, 0, 8))
#   sf.create_tree(position=(3, 0, -5))
#   sf.create_fence(length=12, post_count=7, position=(-6, 0, -3))
#   sf.create_lamp_post(position=(8, 0, 2))
#
#   # Place 8 trees in a circle of radius 15:
#   sf.place_in_circle(sf.create_tree, count=8, radius=15)
#
# Remember: call each function at least once, and aim for 15+ objects.
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Final viewport framing (do not remove).
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    cmds.viewFit(allObjects=True)
    print("Main scene built successfully!")
