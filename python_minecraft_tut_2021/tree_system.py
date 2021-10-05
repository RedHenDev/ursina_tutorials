"""
This is our trees system.
It plants trees (if appropriate) having been
called from the genPerlin() function in our
main module.
"""
from perlin_noise import PerlinNoise
from ursina import Entity, color, Vec3 

class Trees:
    def __init__(this):
        this.noise = PerlinNoise(seed=4)

        # Parent of trees for optimization.
        this.trees = Entity()
        this.treesCounter = 0
        # List of all trees planted.
        this.treeslist = []

    def checkTree(this, _x,_y,_z):
        freq = 5
        amp = 100
        treeChance = ((this.noise([_x/freq,_z/freq]))*amp)
        # print(str(treeChance))
        if treeChance > 30:
            this.plantTree(_x,_y,_z)
            # Record tree location to list of trees.
            this.treeslist.append(Vec3(_x,_y,_z))

    def plantTree(this,_x,_y,_z):
        from random import randint
        tree = Entity(  model = None,
                        position=Vec3(_x,_y,_z))
        crown = Entity( model='cube',
                        scale=6,
                        y=7,
                        color=color.green)
        trunk = Entity( model='cube',
                        scale_y = 9,
                        scale_x = 0.6,
                        scale_z = 0.6,
                        color=color.brown,
                        collider='box')
        crown.parent=tree
        trunk.parent=tree
        tree.y += 4
        tree.rotation_y = randint(0,360)

        tree.parent = this.trees
        this.treesCounter += 1
        if this.treesCounter % 42 == 0:
            this.trees.combine()
            this.trees.collider = this.trees.model

