"""
Build tool system for mining and building :)
Good luck!
"""

from random import randrange, randint, random
from ursina import Entity, color, texture, Vec3
from numpy import floor

class Mining_system:
    def __init__(this, _subject, _axe, _camera, _subsets):

        # We create a reference to these here,
        # so that we can use them in buildTool()
        # and elsewhere?
        this.subject = _subject
        this.axe = _axe
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
        this.blockTypes.append(color.rgb(102,51,0))
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
            # this.axe.position = Vec3(0.3, -0.5, 2.8)
        elif this.buildMode == 1 and key == 'right mouse up':
            this.mine()
            this.axe.shake( duration=0.3,magnitude=7,
                            direction=(-1,1))
            # this.axe.position = Vec3(0.3, -0.5, 2.8)
        # else: this.axe.position = Vec3(2, 0, 2.8)
        # I.e. return axe to default position if not in build mode.
        
        # Toggle build mode.
        if key == 'f': this.buildMode *= -1
        
        # Hey, future you -- improve this system. Thaaanks.
        
        if key == '1': this.blockType=0
        if key == '2': this.blockType=1
        if key == '3': this.blockType=2
        if key == '4': this.blockType=3
        if key == '5': this.blockType=4
    

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

    def adjustShadeAndRotation(this,_block):
        from copy import copy
        # Change colour to soil.
        _block.color = copy(this.blockTypes[2])
        # Adjust the tint of this block's colour.
        shade = randrange(-16,64)/256
        _block.color[0] += shade
        _block.color[1] += shade
        _block.color[2] += shade

        # Add random rotation.
        _block.rotation_y = (90 * randint(0,3))
        _block.rotation_z = (90 * randint(0,3))
        _block.rotation_x = (90 * randint(0,3))

    def mineSpawn(this):
        from copy import copy # For copying colours.

        # Spawn one block below dig position?
        if this.tDic.get(   'x'+str(this.bte.x)+
                            'y'+str(this.bte.y-1)+
                            'z'+str(this.bte.z)
                            ) == None:

            e = Entity( model=this.cubeModel,
                        texture=this.buildTex)
            # Shrink spawned block so that it
            # matches the size of ordinary terrain.
            e.scale *= 0.99999
            
            # Position under mined area.
            e.position = this.bte.position
            e.y -= 1
            
            this.adjustShadeAndRotation(e)

            # Parent spawned cube into builds entity.
            e.parent = this.builds
            # Record newly spawned block on dictionary.
            this.tDic[  'x'+str(this.bte.x)+
                        'y'+str(e.y)+
                        'z'+str(this.bte.z)] = e.y
            this.builds.combine()
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
                            # Position around mined area.
                            e.position = spawnPos[i]
                            this.adjustShadeAndRotation(e)
                            # Parent spawned cube into builds entity.
                            e.parent = this.builds
                            # Record newly spawned block on dictionary.
                            this.tDic[  'x'+str(x)+
                                        'y'+str(y)+
                                        'z'+str(z)] = e.y

    # Place a block at the bte's position.
    def build(this):
        if this.buildMode == -1: return

        # Is there already a block here?
        whatsHere = this.tDic.get(  'x'+str(this.bte.x)+
                                    'y'+str(this.bte.y)+
                                    'z'+str(this.bte.z))
        # Is so, return. No buildy.
        if whatsHere != 'gap' and whatsHere != None:
            print(str(whatsHere))
            return

        e = Entity( model=this.cubeModel,
                    position=this.bte.position)
        # e.collider = 'box'
        # e.texture = this.stoneTex
        e.texture = this.buildTex
        e.scale *= 0.99999
        # Netherite colour for testing :)
        # e.color = this.blockTypes[4]
        e.color = this.blockTypes[this.blockType]
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
        totalV = 0    
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
                totalV += 1
                if totalV >= 36: break
                
                
        if vChange == True:

            whatsHere = this.tDic.get(  'x'+str(this.bte.x)+
                                        'y'+str(this.bte.y)+
                                        'z'+str(this.bte.z))
            # Record new gap on dictionary.
            this.tDic[  'x'+str(this.bte.x)+
                        'y'+str(this.bte.y)+
                        'z'+str(this.bte.z)] = 'gap'
            if whatsHere !='b': 
                this.mineSpawn()
                this.builds.combine()
            # Update builds model Entity so that we
            # see the gaps -- update vertices.
            this.builds.model.generate()    
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
                # Record new gap on dictionary.
                this.tDic[  'x'+str(this.bte.x)+
                            'y'+str(this.bte.y)+
                            'z'+str(this.bte.z)] = 'gap'
                this.mineSpawn()
                # Now that we've spawned what (if anything)
                # we need to, update subset model. Done.
                this.subsets[s].model.generate()
                this.builds.combine()
                return