"""
Build tool system for mining and building :)
Good luck!
"""

from ursina import Entity, color
from numpy import floor

class Mining_system:
    def __init__(this, _subject, _camera, _subsets):

        # We create a reference to these here,
        # so that we can use them in buildTool()
        # and elsewhere?
        this.subject = _subject
        this.camera = _camera

        # A reference to the terrain's subsets
        # is needed for mining etc.
        this.subsets = _subsets

        this.wireTex = 'wireframe.png'
        this.stoneTex = 'grass_mono.png'
        # Build tool entity -- floating wireframe cube.
        this.bte = Entity(  model='cube',
                            texture=this.wireTex,
                            scale=1.01)

        # distance of build (Thanks, Ethan!)
        this.build_distance = 3

        # -1 is OFF, 1 is ON. For toggling.
        this.buildMode = -1

        # Our new block type system...
        this.blockTypes = []
        #  Stone
        this.blockTypes.append(color.rgb(255,255,255))
        # Grass
        this.blockTypes.append(color.rgb(0,255,0))
        # Soil
        this.blockTypes.append(color.rgb(255,80,100))
        # Ruby
        this.blockTypes.append(color.rgb(255,0,0))
        # Netherite
        this.blockTypes.append(color.rgb(0,0,0))
        # Our current block type.
        this.blockType = 0 # I.e. stone.
        

    def build(this):
        pass

    def mine(this):
        pass

    def input(this, key):
        # scroll down to build closer or 
        # scroll up to build further
        # Thanks again, Ethanalos! :)
        if key == 'scroll up':
            this.build_distance += 1
        if key == 'scroll down':
            this.build_distance -= 1

        if this.buildMode == 1 and key == 'left mouse up':
            this.build()
        elif this.buildMode == 1 and key == 'right mouse up':
            this.mine()
        
        # Toggle build mode.
        if key == 'f': this.buildMode *= -1
        
        # Hey, future you -- improve this system. Thaaanks.
        """
        if key == '1': blockType=BTYPE.SOIL
        if key == '2': blockType=BTYPE.GRASS
        if key == '3': blockType=BTYPE.STONE
        if key == '4': blockType=BTYPE.RUBY
        """

    # This is called from the main update loop.
    def buildTool(this):
        
        if this.buildMode == -1:
            this.bte.visible = False
            return
        else: this.bte.visible = True
        this.bte.position = round(this.subject.position +
                        this.camera.forward * this.build_distance)
        this.bte.y += 2
        this.bte.y = round(this.bte.y)
        this.bte.x = round(this.bte.x)
        this.bte.z = round(this.bte.z)
        this.bte.color = this.blockTypes[this.blockType]

    # Place a block at the bte's position.
    def build(this):
        if this.buildMode == -1: return

        e = Entity(model='cube',position=this.bte.position)
        e.collider = 'box'
        e.texture = this.stoneTex
        e.color = this.blockTypes[this.blockType]
        e.shake(duration=0.5,speed=0.01)
    
    def mine(this):
        # e = mouse.hovered_entity
        # destroy(e)

        # Our real mining of the terrain :)
        # Iterate over all the subsets that we have...
        for s in range(len(this.subsets)):
            vChange = False
            totalY = 0
            for v in this.subsets[s].model.vertices:
                # Is the vertex close enough to
                # where we want to mine (bte position)?
                if (v[0] >=this.bte.x - 0.5 and
                    v[0] <=this.bte.x + 0.5 and
                    v[1] >=this.bte.y - 0.5 and
                    v[1] <=this.bte.y + 0.5 and
                    v[2] >=this.bte.z - 0.5 and
                    v[2] <=this.bte.z + 0.5):
                    # Yes!
                    # v[1] -= 1
                    v[1] = 9999
                    # Note that we have made change.
                    # Gather average height for cave dic.
                    vChange = True
            
            if vChange == True:
                this.subsets[s].model.generate()
                return
                # anush.makeCave(bte.x,bte.z,bte.y-1)  