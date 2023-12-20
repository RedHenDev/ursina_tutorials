from perlin import Perlin
from ursina import *
# from random import random as rara
# random module comes with inventory_system as ra
from swirl_engine import SwirlEngine
from mining_system import *
from building_system import *
from config import six_cube_dirs, minerals, mins
from tree_system import *
from inventory_system import *

class MeshTerrain:
    def __init__(this,_sub,_cam):
        
        this.subject = _sub
        this.camera = _cam
        # *** - for ursina update fix
        this.block = load_model('block.obj',use_deepcopy=True)
        this.textureAtlas = 'texture_atlas_3.png'
        this.numVertices = len(this.block.vertices)

        this.subsets = []
        this.numSubsets = 1024
        
        # Must be even number! See genTerrain()
        this.subWidth = 6 
        this.swirlEngine = SwirlEngine(this.subWidth)
        this.currentSubset = 0

        # Our terrain dictionary :D
        this.td = {}

        # Our vertex dictionary -- for mining.
        this.vd = {}

        this.perlin = Perlin()

        # Our new planting terrain feature variables...
        this.tree_noise=PerlinNoise(
                octaves=32,
                seed=2022)
        this.tree_freq=64
        this.tree_amp=128

        # Instantiate our subset Entities.
        this.setup_subsets()

    def plant_tree(this,_x,_y,_z):

        # NB need to move these two lines
        # here to correctly apply wiggle.
        # have not shown on a tut vid yet!
        ent=TreeSystem.genTree(_x,_z)
        if ent==0: return

        # *** - disrupt grid.
        wiggle=floor(sin(_z*_x)*3)
        _z += wiggle
        _x += wiggle

        # Adjust tree x and z pos due to wiggle.
        _y = floor(this.perlin.getHeight(_x,_z))

        
        # TrunkyWunky.
        treeH=int(7*ent)
        for i in range(treeH):
            this.genBlock(_x,_y+i+1,_z,
                blockType='wood',layingTerrain=False)
        # Crown.
        for t in range(-2,3):
            for tt in range(4):
                for ttt in range(-2,3):
                    this.genBlock(_x+t,_y+treeH+tt,_z+ttt,
                    blockType='foliage')

    def plant_stone(this, _x, _z):
        probs=this.tree_noise(([_x/this.tree_freq,_z/this.tree_freq]))*this.tree_amp
        if probs > 32:
            return True
        return False

    def setup_subsets(this):
        for i in range(0,this.numSubsets):
            e = Entity( model=Mesh(),
                        texture=this.textureAtlas)
            e.texture_scale*=64/e.texture.width
            this.subsets.append(e)

    def do_mining(this):
        # Pass in block and textureAtlas for dropping
        # collectible. See mining_system mine().
        epi = mine( this.td,this.vd,this.subsets,
                    this.textureAtlas,this.subject)
        if (epi != None and epi[2]!='wood' and
            epi[2]!='foliage'):
            this.genWalls(epi[0],epi[1])
            this.subsets[epi[1]].model.generate()

    # Highlight looked-at block :)
    def update(this):
        highlight(  this.subject.position,
                    this.subject.height,
                    this.camera,this.td)
        # Blister-mining!
        if bte.visible==True and mouse.locked==True:
            if held_keys['shift'] and held_keys['left mouse']:
                this.do_mining()
            # for key, value in held_keys.items():
            #     if key=='left mouse' and value==1:
            #         this.do_mining()

    def input(this,key):
        if key=='left mouse up' and bte.visible==True and mouse.locked==True:
            this.do_mining()
        # Building :)
        # First, return and don't build if empty handed.
        if this.subject.blockType is None: return
        if key=='right mouse up' and bte.visible==True and mouse.locked==True:
            bsite = checkBuild( bte.position,this.td,
                                this.camera.forward,
                                this.subject.position+Vec3(0,this.subject.height,0))
            if bsite!=None:
                this.genBlock(floor(bsite.x),floor(bsite.y),floor(bsite.z),subset=0,blockType=this.subject.blockType)
                gapShell(this.td,bsite)
                this.subsets[0].model.generate()
                # *** Deplete a block from the stack ;)
                for h in hotspots:
                    # Is this hotspot highlighted?
                    if h.color==color.black:
                        # Decrease stack number by 1.
                        h.stack -= 1
                        if h.stack > 0:
                            h.item.update_stack_text()
                            break
                        # If we use up all blocks,
                        # empty out this hotspot.
                        elif h.stack <= 0:
                            if h.stack < 0:
                                h.stack=0
                            h.occupied=False
                            destroy(h.item)
                            h.t.text=""
                            # No blocks to build with!
                            this.subject.blockType=None




    
    # I.e. after mining, to create illusion of depth.
    def genWalls(this,epi,subset):
        
        if epi==None: return
        # Refactor this -- place in mining_system 
        # except for cal to genBlock?
        
        for i in range(0,6):
            np = epi + six_cube_dirs[i]
            if this.td.get( (floor(np.x),
                            floor(np.y),
                            floor(np.z)))==None:
                this.genBlock(np.x,np.y,np.z,subset,gap=False,blockType='soil')


    def genBlock(this,x,y,z,subset=-1,gap=True,blockType='grass',layingTerrain=False):
        if subset==-1: subset=this.currentSubset
        # Extend or add to the vertices of our model.
        model = this.subsets[subset].model

        model.vertices.extend([ Vec3(x,y,z) + v for v in 
                                this.block.vertices])

        # Does the dictionary entry for this blockType
        # hold colour information? If so, use it :)
        if len(minerals[blockType])>2:
            # Decide random tint for colour of block :)
            c = ra.random()-0.5
            # Grab the Vec4 colour data :)
            ce=minerals[blockType][2]
            # Adjust each colour channel separately to
            # ensure that hard-coded RGB combination is maintained.
            model.colors.extend(    (Vec4(ce[0]-c,ce[1]-c,ce[2]-c,ce[3]),)*
                                    this.numVertices)
        else:
            # Decide random tint for colour of block :)
            c = ra.random()-0.5
            model.colors.extend(    (Vec4(1-c,1-c,1-c,1),)*
                                    this.numVertices)

        # This is the texture atlas co-ord for grass :)
        uu=minerals[blockType][0]
        uv=minerals[blockType][1]

        model.uvs.extend([Vec2(uu,uv) + u for u in this.block.uvs])

        # Record terrain in dictionary :)
        this.td[(floor(x),floor(y),floor(z))] = blockType
        # Also, record gap above this position to
        # correct for spawning walls after mining.
        if gap==True:
            key=((floor(x),floor(y+1),floor(z)))
            if this.td.get(key)==None:
                this.td[key]='g'

        # Record subset index and first vertex of this block.
        vob = (subset, len(model.vertices)-this.numVertices-1)
        this.vd[(floor(x),
                floor(y),
                floor(z))] = vob

    def genTerrain(this):
        # Get current position as we swirl around world.
        x = floor(this.swirlEngine.pos.x)
        z = floor(this.swirlEngine.pos.y)

        d = int(this.subWidth*0.5)

        for k in range(-d,d):
            for j in range(-d,d):

                y = floor(this.perlin.getHeight(x+k,z+j))
                if this.td.get( (floor(x+k),
                                floor(y),
                                floor(z+j)))==None:
                    # Decide whether placing stone etc. or grass :)
                    # Assume we're laying grass.
                    bType='grass'
                    if this.plant_stone(x+k,z+j)==True:
                        bType='stone'
                    if y > 2:
                        bType='snow'
                    this.genBlock(x+k,y,z+j,blockType=bType,layingTerrain=True)
                    # Plant a tree?ß
                    this.plant_tree(x+k,y,z+j)

        this.subsets[this.currentSubset].model.generate()
        # Current subset hack ;)
        if this.currentSubset<this.numSubsets-1:
            this.currentSubset+=1
        else: this.currentSubset=0
        this.swirlEngine.move()