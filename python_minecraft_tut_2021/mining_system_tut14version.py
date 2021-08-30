"""
Build tool system for mining and building :)
Good luck!
"""

from ursina import Entity, color, texture
from numpy import floor

class Mining_system:
    def __init__(this, _subject, _camera, _subsets):

        # We create a reference to these here,
        # so that we can use them in buildTool()
        # and elsewhere?
        this.subject = _subject
        this.camera = _camera

        # Dictionaries for recording positions of terrain
        # including gaps.
        this.tDic = {}
        this.buildTex = 'build_texture.png' 
        this.cubeModel = 'moonCube.obj'
        this.builds = Entity(model=this.cubeModel,
                            texture=this.buildTex)

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
        #  Stone - 0
        this.blockTypes.append(color.rgb(255,255,255))
        # Grass - 1
        this.blockTypes.append(color.rgb(0,255,0))
        # Soil - 2
        this.blockTypes.append(color.rgb(255,80,100))
        # Ruby - 3
        this.blockTypes.append(color.rgb(255,0,0))
        # Netherite - 4
        this.blockTypes.append(color.rgb(0,0,0))
        # Our current block type.
        this.blockType = 0 # I.e. stone.

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

    def mineSpawn(this):
        # Spawn one block below dig position?
        if this.tDic.get(   'x'+str(this.bte.x)+
                            'y'+str(this.bte.y-1)+
                            'z'+str(this.bte.z)
                            ) == None:

            # Record gap location in dictionary.
            this.tDic[  'x'+str(this.bte.x)+
                        'y'+str(this.bte.y)+
                        'z'+str(this.bte.z)] = 'gap'
                    
            e = Entity( model=this.cubeModel,
                        texture=this.buildTex)
            # Shrink spawned block so that it
            # matches the size of ordinary terrain.
            e.scale *= 0.99999
            # Change colour to soil (this.blockTypes[2]).
            e.color = this.blockTypes[0]
            # Position under mined area.
            e.position = this.bte.position
            e.y -= 1
            # Parent spawned cube into builds entity.
            e.parent = this.builds
            # Record newly spawned block on dictionary.
            this.tDic[  'x'+str(this.bte.x)+
                        'y'+str(e.y)+
                        'z'+str(this.bte.z)] = e.y

            # OK -- now spawn 4 'cave wall' cubes.
            # For each cube, first check whether:
            # 1) No terrain there already
            # 2) No gaps
            # 3) No terrain below this pos
            x = this.bte.x
            y = this.bte.y
            z = this.bte.z
            pos1 = (x+1,y,z)
            pos2 = (x-1,y,z)
            pos3 = (x,y,z+1)
            pos4 = (x,y,z-1)
            spawnPos = []
            spawnPos.append(pos1)
            spawnPos.append(pos2)
            spawnPos.append(pos3)
            spawnPos.append(pos4)
            for i in range(4):
                x = spawnPos[i][0]
                z = spawnPos[i][2]
                y = spawnPos[i][1]
                    
                # We can ask None both times because
                # this covers both gaps and terrain
                # being in these positions (i.e
                # potential cave wall and below
                # potential cave wall.
                if this.tDic.get(   'x'+str(x)+
                                    'y'+str(y)+
                                    'z'+str(z)
                        ) == None and \
                        this.tDic.get(  'x'+str(x)+
                                        'y'+str(y-1)+
                                        'z'+str(z)
                        ) == None:
                            e = Entity( model=this.cubeModel,
                                        texture=this.buildTex)
                            # Shrink spawned block so that it
                            # matches the size of ordinary terrain.
                            e.scale *= 0.99999
                            # Change colour to soil (this.blockTypes[2]).
                            e.color = this.blockTypes[0]
                            # Position around mined area.
                            e.position = spawnPos[i]
                            # Parent spawned cube into builds entity.
                            e.parent = this.builds
                            # Record newly spawned block on dictionary.
                            this.tDic[  'x'+str(x)+
                                        'y'+str(y)+
                                        'z'+str(z)] = e.y

    # Place a block at the bte's position.
    def build(this):
        if this.buildMode == -1: return

        e = Entity( model=this.cubeModel,
                    position=this.bte.position)
        # e.collider = 'box'
        # e.texture = this.stoneTex
        e.texture = this.buildTex
        e.scale *= 0.99999
        # Netherite colour for testing :)
        e.color = this.blockTypes[4]
        # e.color = this.blockTypes[this.blockType]
        e.parent = this.builds
        # Record newly built block on dictionary.
        this.tDic[  'x'+str(e.x)+
                    'y'+str(e.y)+
                    'z'+str(e.z)] = 'b'
        this.builds.combine()
        # Shaking animation won't work since we're
        # destroying the temp block (.combine()).
        # e.shake(duration=0.5,speed=0.01)
    
    def mine(this):

        vChange = False
            
        for v in this.builds.model.vertices:
            # Is the vertex close enough to
            # where we want to mine (bte position)?
            if (v[0] >=this.bte.x - 0.5 and
                v[0] <=this.bte.x + 0.5 and
                v[1] >=this.bte.y - 0.5 and
                v[1] <=this.bte.y + 0.5 and
                v[2] >=this.bte.z - 0.5 and
                v[2] <=this.bte.z + 0.5):

                # Move vertex high into air to
                # give illusion of being destroyed.
                v[1] = 9999
                # Note that we have made change.
                vChange = True
                # Record new gap on dictionary.
                this.tDic[  'x'+str(this.bte.x)+
                            'y'+str(this.bte.y)+
                            'z'+str(this.bte.z)] = 'gap'
                
        if vChange == True:
            buildBlock = True
            if this.tDic.get(   'x'+str(this.bte.x)+
                                'y'+str(this.bte.y)+
                                'z'+str(this.bte.z)) \
                !='b':
                buildBlock = False
                this.mineSpawn()
            this.builds.model.generate()
            if buildBlock == False:
                this.builds.combine()
            # Not done! Also combine newly spawned blocks
            # into builds entity :)
            return  

        # Our real mining of the terrain :)
        # Iterate over all the subsets that we have...
        totalV = 0
        for s in range(len(this.subsets)):
            vChange = False
            
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
                    #v[1] -= 1
                    # Move vertex high into air to
                    # give illusion of being destroyed.
                    v[1] = 9999
                    # Note that we have made change.
                    # Gather average height for cave dic.
                    vChange = True
                    # Record new gap on dictionary.
                    this.tDic[  'x'+str(this.bte.x)+
                                'y'+str(this.bte.y)+
                                'z'+str(this.bte.z)] = 'gap'
                    totalV += 1
                    # The mystery of 36 vertices!! :o
                    # print('tV= ' + str(totalV))
                    if totalV==36: break
            
            if vChange == True:

                # Now we need to spawn a new cube below
                # the bte's position -- if no cube or
                # gap there already.
                # Next, spawn 4 cubes to create illusion
                # of more layers -- if each position is
                # neither a gap nor a place where terrain
                # already is.

                this.mineSpawn()
                # Now that we've spawned what (if anything)
                # we need to, update subset model. Done.
                this.subsets[s].model.generate()
                this.builds.combine()
                return