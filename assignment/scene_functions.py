"""
DIGM 131 - Assignment 3: Function Library (scene_functions.py)
===============================================================

OBJECTIVE:
    Create a library of reusable functions that each generate a specific
    type of scene element. This module will be imported by main_scene.py.

REQUIREMENTS:
    1. Implement at least 5 reusable functions.
    2. Every function must have a complete docstring with Args and Returns.
    3. Every function must accept parameters for position and/or size so
       they can be reused at different locations and scales.
    4. Every function must return the name(s) of the Maya object(s) it creates.
    5. Follow PEP 8 naming conventions (snake_case for functions/variables).

GRADING CRITERIA:
    - [30%] At least 5 functions, each creating a distinct scene element.
    - [25%] Functions accept parameters and use them (not hard-coded values).
    - [20%] Every function has a complete docstring (summary, Args, Returns).
    - [15%] Functions return the created object name(s).
    - [10%] Clean, readable code following PEP 8.
"""

import maya.cmds as cmds


def create_building(building_width=4, building_height=8, building_depth=4, position=(0, 0, 0)):
    """Create a simple building from a cube, placed on the ground plane.

    The building is a single scaled cube whose base sits at ground level
    (y = 0) at the given position.

    Args:
        building_width (float): Width of the building along the X axis.
        building_height (float): Height of the building along the Y axis.
        building_depth (float): Depth of the building along the Z axis.
        position (tuple): (x, y, z) ground-level position. The building
            base will rest at this point; y is typically 0.

    Returns:
        str: The name of the created building transform node.
    """
    
    #Create a building and position it with the given parameters
    building = cmds.polyCube(width=building_width, height=building_height, depth=building_depth, name="building")[0]
    cmds.move(position[0], (building_height / 2.0) + position[1], position[2], building)
    
    return building


def create_tree(trunk_radius=0.3, trunk_height=3, canopy_radius=2,
                position=(0, 0, 0)):
    """Create a simple tree using a cylinder trunk and a sphere canopy.

    Args:
        trunk_radius (float): Radius of the cylindrical trunk.
        trunk_height (float): Height of the trunk cylinder.
        canopy_radius (float): Radius of the sphere used for the canopy.
        position (tuple): (x, y, z) ground-level position for the tree base.

    Returns:
        str: The name of a group node containing the trunk and canopy.
    """
    
    #Create a tree trunk and position it to ground level
    trunk = cmds.polyCylinder(radius=trunk_radius, height=trunk_height, name="tree_trunk")[0]
    cmds.move(0, trunk_height / 2.0, 0, trunk)
    
    #Create a tree canopy and position it relative to the tree trunk
    canopy = cmds.polySphere(radius=canopy_radius, name="tree_canopy")[0]
    cmds.move(0, trunk_height + trunk_height / 2.0, 0, canopy)
    
    #Group the trunk and canopy together and position the group at the given parameters
    tree_group = cmds.group(trunk, canopy, name="tree_grp")
    cmds.move(position[0], position[1], position[2], tree_group)
    
    return tree_group
    

def create_fence(length=10, height=1.5, post_count=6, position=(0, 0, 0)):
    """Create a simple fence made of posts and rails.

    The fence runs along the X axis starting at the given position.

    Args:
        length (float): Total length of the fence along the X axis.
        height (float): Height of the fence posts.
        post_count (int): Number of vertical posts (must be >= 2).
        position (tuple): (x, y, z) starting position of the fence.

    Returns:
        str: The name of a group node containing all fence parts.
    """
    
    #Fence Post Parameters
    spacing = length / (post_count - 1)
    post_base = 0.25
    
    #Store references for the fence posts
    fence_posts = []
    
    #Create the fence posts and position them to ground level; the loop allows for a post_count number of lamp posts to be evenly spread out by increments of spacing
    for i in range(post_count):
        post_name = f"post_{i}"
        post = cmds.polyCube(width=post_base, height=height, depth=post_base, name=post_name)[0]
        cmds.move(i*spacing, height / 2.0, 0, post)
        fence_posts.append(post_name)
    
    #Railing Parameters
    railing_base = 0.2
    
    #Create the railing for the fence and position it relative to the fence posts    
    railing = cmds.polyCube(width=length, height = railing_base, depth = railing_base, name="railing")[0]
    cmds.move(length / 2.0, height / 1.5, 0, railing)
    
    #Group the fence posts and railing together and position the group with the given parameters
    fence_group = cmds.group(fence_posts, railing, name="fence_grp")
    cmds.move(position[0], position[1], position[2], fence_group)
    
    return fence_group
    

def create_lamp_post(pole_height=5, light_radius=0.5, position=(0, 0, 0)):
    """Create a street lamp using a cylinder pole and a sphere light.

    Args:
        pole_height (float): Height of the lamp pole.
        light_radius (float): Radius of the sphere representing the light.
        position (tuple): (x, y, z) ground-level position.

    Returns:
        str: The name of a group node containing the pole and light.
    """
    
    #Pole Parameters
    pole_radius = 0.15
    
    #Create the lamp post pole and position it at ground level
    pole = cmds.polyCylinder(radius=pole_radius, height=pole_height, name="lamp_pole")[0]
    cmds.move(0, pole_height / 2.0, 0, pole)
    
    #Create the lamp post light and position it relative to the lamp post pole
    light = cmds.polySphere(radius=light_radius, name="lamp_light")[0]
    cmds.move(0, pole_height, 0, light)
    
    #Group the lamp post pole and light together and position the group with the given parameters
    lamp_post_group = cmds.group(pole, light, name="lamp_post_grp")
    cmds.move(position[0], position[1], position[2], lamp_post_group)
    
    return lamp_post_group
    
    
def place_in_circle(create_func, count=8, radius=10, center=(0, 0, 0),
                     **kwargs):
    """Place objects created by 'create_func' in a circular arrangement.

    This is a higher-order function: it takes another function as an
    argument and calls it repeatedly to place objects around a circle.

    Args:
        create_func (callable): A function from this module (e.g.,
            create_tree) that accepts a 'position' keyword argument
            and returns an object name.
        count (int): Number of objects to place around the circle.
        radius (float): Radius of the circle.
        center (tuple): (x, y, z) center of the circle.
        **kwargs: Additional keyword arguments passed to create_func
            (e.g., trunk_height=4).

    Returns:
        list: A list of object/group names created by create_func.
    """
    import math
    
    #Store references for the object being placed in a circle
    results = []
    
    #Place the objects created by the used function in a circle with the given parameters
    for i in range(count):
        angle = (2 * math.pi / count) * i
        x = center[0] + radius * math.cos(angle)
        z = center[2] + radius * math.sin(angle)
        result = create_func(position=(x, center[1], z), **kwargs)
        results.append(result)
    
    #Group the objects placed in a circle together
    cmds.group(results, name=create_func)
    
    return results
    
