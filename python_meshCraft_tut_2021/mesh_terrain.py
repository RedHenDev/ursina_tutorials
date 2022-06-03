from perlin import Perlin
from ursina import *
from random import random
from swirl_engine import SwirlEngine
from mining_system import *
from building_system import *
from config import six_cube_dirs, minerals, mins

class MeshTerrain:
    def __init__(this,_sub,_cam):
        
        this.subject = _sub
        this.camera = _cam

        this.block = load_model('block.obj')
        this.textureAtlas = 'texture_atlas_3.png'
        this.numVertices = len(this.block.vertices)

        this.subsets = []
        this.numSubsets = 512
        
        # Must be even number! See genTerrain()
        this.subWidth = 10 
        this.swirlEngine = SwirlEngine(this.subWidth)
        this.currentSubset = 0

        # Our terrain dictionary :D
        this.td = {}

        # Our vertex dictionary -- for mining.
        this.vd = {}

        this.perlin = Perlin()

        # Instantiate our subset Entities.
        this.setup_subsets()

    def setup_subsets(this):
        for i in range(0,this.numSubsets):
            e = Entity( model=Mesh(),
                        texture=this.textureAtlas)
            e.texture_scale*=64/e.texture.width
            this.subsets.append(e)

    def do_mining(this):
        epi = mine(this.td,this.vd,this.subsets)
        if epi != None:
            this.genWalls(epi[0],epi[1])
            this.subsets[epi[1]].model.generate()

    # Highlight looked-at block :)
    # !*!*!*!*!*!*!
    # We don't need to pass in pos and cam anymore?!
    def update(this,pos,cam):
        highlight(pos,cam,this.td)
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
        if key=='right mouse up' and bte.visible==True and mouse.locked==True:
            bsite = checkBuild( bte.position,this.td,
                                this.camera.forward,
                                this.subject.position+Vec3(0,this.subject.height,0))
            if bsite!=None:
                this.genBlock(floor(bsite.x),floor(bsite.y),floor(bsite.z),subset=0,blockType=this.subject.blockType)
                gapShell(this.td,bsite)
                this.subsets[0].model.generate()
    
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

        if layingTerrain:
            # Randomly place stone blocks.
            if random() > 0.86:
                blockType='stone'
            # If high enough, cap with snow blocks :D
            if y > 2:
                blockType='snow'

        # Does the dictionary entry for this blockType
        # hold colour information? If so, use it :)
        if len(minerals[blockType])>2:
            # Decide random tint for colour of block :)
            c = random()-0.5
            # Grab the Vec4 colour data :)
            ce=minerals[blockType][2]
            # Adjust each colour channel separately to
            # ensure that hard-coded RGB combination is maintained.
            model.colors.extend(    (Vec4(ce[0]-c,ce[1]-c,ce[2]-c,ce[3]),)*
                                    this.numVertices)
        else:
            # Decide random tint for colour of block :)
            c = random()-0.5
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
        vob = (subset, len(model.vertices)-37)
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
                    this.genBlock(x+k,y,z+j,blockType='grass',layingTerrain=True)

        this.subsets[this.currentSubset].model.generate()
        # Current subset hack ;)
        if this.currentSubset<this.numSubsets-1:
            this.currentSubset+=1
        else: this.currentSubset=0
        this.swirlEngine.move()