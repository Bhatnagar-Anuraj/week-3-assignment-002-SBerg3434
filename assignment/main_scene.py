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


def create_city_block(building_row_count=3, building_column_count=3, position=(0,0,0)):
    """Create a city block by creating a grid of buildings with random heights.

    Args:
        building_row_count (int): The number of rows of buildings
        building_column_count (int): The number of columns of buildings
        position (tuple): (x, y, z) ground-level position for the city block.

    Returns:
        str: The name of a group node containing all the buildings.
    """
    #Grid Pattern Parameters
    rows = building_row_count
    cols = building_column_count
    building_count = building_row_count * building_column_count
    grid_spacing = 66 / 2.84
    building_height_minimum = 26
    building_height_maximum = 50
    
    #Store references for the buildings
    all_buildings = []
    
    #Nested loop allows for a simple grid of buildings with random heights to be created
    for row in range(rows):
        for col in range(cols):         
            #Building Parameters
            x_grid = col * grid_spacing
            z_grid = row * grid_spacing  # offset behind the columns
            building_height_random = random.randint(building_height_minimum,building_height_maximum)
            
            #Create a building with the given parameters
            building = sf.create_building(building_width=16,building_height=building_height_random,building_depth=16,position=(x_grid,0,z_grid))
            
            #Add the newly created buildling to the reference list established before the loop
            all_buildings.append(building)
    
    #Group the buildings together and position them with the given parameters 
    city_block_group = cmds.group(all_buildings, name="city_block_grp")
    cmds.move(position[0],position[1],position[2],city_block_group)
    
    return city_block_group
   
    
def create_lamp_post_line(lamp_post_count=7,post_spacing=10,y_rotation=0,position=(0,0,0)):            
    """Create a line of lamp posts to line the streets.
    
        Args:
            lamp_post_count (int): The number of lamp posts
            post_spacing (float): The space between each lamp post
            y_rotation (float): The rotation of the full line of lamp posts
            position (tuple): (x, y, z) ground-level position for the city block.
    
        Returns:
            str: The name of a group node containing all the lamp posts.
    """

    #Store references for the lamp posts
    lamp_posts = []
    
    #Line the street with lamp posts; the loop allows for a lamp_post_count number of lamp posts to evenly line the street 
    for i in range(lamp_post_count):
        lamp_post = sf.create_lamp_post()
        cmds.move(i * post_spacing,0,0, lamp_post) 
        lamp_posts.append(lamp_post)     
    
    #Group the lamp posts together and position and rotate the group with the given parameters        
    lampost_group = cmds.group(lamp_posts, name="lamp_posts_grp")
    cmds.move(position[0],position[1],position[2],lampost_group)
    cmds.rotate(0,y_rotation,0,lampost_group)

    return lampost_group


def create_park(tree_count=10,tree_circle_radius=12,fence_length=32,fence_post_count=10,position=(0,0,0)):
    """Create a park that contains a circle of trees and a fence surrounding it.
    
        Args:
            tree_count (int): The number of trees
            tree_circle_radius (float): The radius of the tree circle
            fence_length (float): The length of the fence
            fence_post_count (int): The number of fence posts in the fence
            position (tuple): (x, y, z) ground-level position for the city block.
    
        Returns:
            str: The name of a group node containing the trees and fences.
    """
    #Create a circle of trees with the given parameters
    tree_circle = sf.place_in_circle(sf.create_tree,count=tree_count,radius=tree_circle_radius)
   
    #Create a fence with the given parameters
    fence_group = sf.create_fence(length=fence_length,post_count=fence_post_count,position=((-16),0,16))
    
    #Create the 3 other sides of the enclosure; the loop allows for the already created fence to be duplicated for use as the other sides of the enclosure
    for i in range(3):
        cmds.duplicate(fence_group)
    
    #Position and rotate the three newly created fences
    cmds.move((-16),0,(-16),"fence_grp1")
    cmds.rotate(0,90,0,"fence_grp2")
    cmds.rotate(0,90,0,"fence_grp3")
    cmds.move((0),0,(0),"fence_grp2")
    cmds.move((-32),0,(0),"fence_grp3")
    
    #Group all the fences together and position the group around the tree circle
    fence_full_group = cmds.group("fence_grp","fence_grp1","fence_grp2","fence_grp3",name="fence_full_grp")    
    cmds.move(0,0,0,fence_full_group)
    
    #Group the trees and fence together and position the group with the given parameters
    park_full_group = cmds.group(tree_circle,fence_full_group,name="full_park_grp")
    cmds.move(position[0],position[1],position[2],park_full_group)
    
    return park_full_group   
    
    
def apply_color(nodes,r,g,b,shader_name="colorShader"):
    """Apply a Lambert shader with the given RGB color to all listed nodes."""
    shader = cmds.shadingNode("lambert", asShader=True,name=shader_name)
    cmds.setAttr(shader+".color",r,g,b,type="double3")
    cmds.select(nodes)
    cmds.hyperShade(assign=shader)
    return shader
    
# ---------------------------------------------------------------------------
# Top Level Assembly - Create the full scene
# ---------------------------------------------------------------------------         
def build_full_scene():
    """Assemble the complete scene from modular parts."""
    
    #1) Ground - Apply the ground material to the ground
    apply_color(ground, 0.094, 0.094, 0.094, shader_name="ground_mat")
    
    #2) Park - Create the park and apply the park material to it
    full_park = create_park()
    apply_color(full_park, 0.266, 0.130, 0.061, shader_name="park_mat")
    
    #3) Buildings - Create the four city blocks and position them
    block_1 = create_city_block(position=(35,0,35))
    block_2 = create_city_block(position=((-85),0,35)) 
    block_3 = create_city_block(position=((-85),0,(-85))) 
    block_4 = create_city_block(position=(35,0,(-85)))
    
    #3.5) Building Shaders - Apply the four separate building materials to the city block groups
    apply_color(block_1, 0.447, 0.569, 0.934, shader_name="buildings1_mat")
    apply_color(block_2, 0.405, 0.504, 0.486, shader_name="buildings2_mat")
    apply_color(block_3, 0.334, 0.334, 0.334, shader_name="buildings3_mat")
    apply_color(block_4, 0.6, 0.5, 0.45, shader_name="buildings4_mat")  
    
    #4) Lamp Posts - Line one streets with lamp posts
    lampost_line_1 = create_lamp_post_line(position=(22,0,20))
    lampost_line_2 = create_lamp_post_line(position=(22,0,(-20))) 
    lampost_line_3 = create_lamp_post_line(position=((-82),0,20))
    lampost_line_4 = create_lamp_post_line(position=((-82),0,(-20)))  
    
    #4.5) Lamp Post Group and Shader - Group the lamp posts together and apply the lamp post material to the full group
    lined_street_group = cmds.group("lamp_posts_grp","lamp_posts_grp1","lamp_posts_grp2","lamp_posts_grp3", name="lined_street_1") 
    apply_color(lined_street_group, 0.129, 0.123, 0.169, shader_name="lamp_post_mat")
    
    #5) Lamp Post Second Street - Duplicate the group and rotate it such that it lines the other street in the intersection with lamp posts
    cmds.duplicate(lined_street_group)
    cmds.rotate(0,90,0,"lined_street_2")
      

# ---------------------------------------------------------------------------
# Final viewport framing (do not remove).
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    cmds.viewFit(allObjects=True)
    print("Main scene built successfully!")
    
build_full_scene()    
