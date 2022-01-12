from perlin import Perlin
from ursina import *
from random import random
from swirl_engine import SwirlEngine
from mining_system import *

class MeshTerrain:
    def __init__(this):
        
        this.block = load_model('block.obj')
        this.textureAtlas = 'texture_atlas_3.png'
        this.numVertices = len(this.block.vertices)

        this.subsets = []
        this.numSubsets = 512
        
        # Must be even number! See genTerrain()
        this.subWidth = 8 
        this.swirlEngine = SwirlEngine(this.subWidth)
        this.currentSubset = 0

        # Our terrain dictionary :D
        this.td = {}

        # Our vertex dictionary -- for mining.
        this.vd = {}

        this.perlin = Perlin()

        for i in range(0,this.numSubsets):
            e = Entity( model=Mesh(),
                        texture=this.textureAtlas)
            e.texture_scale*=64/e.texture.width
            this.subsets.append(e)
        
    # Highlight looked-at block :)
    def update(this,pos,cam):
        highlight(pos,cam,this.td)
    
    def input(this,key):
        if key=='left mouse up' and bte.visible==True:
            epi = mine(this.td,this.vd,this.subsets)
            if epi != None:
                this.genWalls(epi[0],epi[1])
                this.subsets[epi[1]].model.generate()
    
    # I.e. after mining, to create illusion of depth.
    def genWalls(this,epi,subset):
        if epi==None: return
        # Refactor this -- place in mining_system 
        # except for cal to genBlock?
        wp =    [   Vec3(0,1,0),
                    Vec3(0,-1,0),
                    Vec3(-1,0,0),
                    Vec3(1,0,0),
                    Vec3(0,0,-1),
                    Vec3(0,0,1)]
        for i in range(0,6):
            np = epi + wp[i]
            if this.td.get( 'x'+str(floor(np.x))+
                            'y'+str(floor(np.y))+
                            'z'+str(floor(np.z)))==None:
                this.genBlock(np.x,np.y,np.z,subset,gap=False,blockType='soil')

    def genBlock(this,x,y,z,subset=-1,gap=True,blockType='grass'):
        if subset==-1: subset=this.currentSubset
        # Extend or add to the vertices of our model.
        model = this.subsets[subset].model

        model.vertices.extend([ Vec3(x,y,z) + v for v in 
                                this.block.vertices])
        # Record terrain in dictionary :)
        this.td["x"+str(floor(x))+
                "y"+str(floor(y))+
                "z"+str(floor(z))] = "t"
        # Also, record gap above this position to
        # correct for spawning walls after mining.
        if gap==True:
            key =  ("x"+str(floor(x))+
                    "y"+str(floor(y+1))+
                    "z"+str(floor(z)))
            if this.td.get(key)==None:
                this.td[key] = "g"

        # Record subset index and first vertex of this block.
        vob = (subset, len(model.vertices)-37)
        this.vd["x"+str(floor(x))+
                "y"+str(floor(y))+
                "z"+str(floor(z))] = vob

        # Decide random tint for colour of block :)
        c = random()-0.5
        model.colors.extend( (Vec4(1-c,1-c,1-c,1),)*
                                this.numVertices)

        # This is the texture atlas co-ord for grass :)
        uu = 8
        uv = 7
        if blockType=='soil':
            uu = 10
            uv = 7
        elif blockType=='stone':
            uu = 8
            uv = 5
        elif blockType=='ice':
            uu = 9
            uv = 7
        # Randomly place stone blocks.
        if random() > 0.86:
            uu = 8
            uv = 5
        # If high enough, cap with snow blocks :D
        if y > 2:
            uu = 8
            uv = 6
        model.uvs.extend([Vec2(uu,uv) + u for u in this.block.uvs])

    def genTerrain(this):
        # Get current position as we swirl around world.
        x = floor(this.swirlEngine.pos.x)
        z = floor(this.swirlEngine.pos.y)

        d = int(this.subWidth*0.5)

        for k in range(-d,d):
            for j in range(-d,d):

                y = floor(this.perlin.getHeight(x+k,z+j))
                if this.td.get( "x"+str(floor(x+k))+
                                "y"+str(floor(y))+
                                "z"+str(floor(z+j)))==None:
                    this.genBlock(x+k,y,z+j,blockType='ice')

        this.subsets[this.currentSubset].model.generate()
        # Current subset hack ;)
        if this.currentSubset<this.numSubsets-1:
            this.currentSubset+=1
        else: this.currentSubset=0
        this.swirlEngine.move()