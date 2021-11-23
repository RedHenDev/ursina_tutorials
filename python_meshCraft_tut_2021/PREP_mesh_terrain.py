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
        this.numSubsets = 64
        
        # Must be even number! See genTerrain()
        this.subWidth = 8
        this.swirlEngine = SwirlEngine(this.subWidth)
        this.currentSubset = 0

        # Our terrain dictionary :D
        this.td = {}

        this.perlin = Perlin()

        for i in range(0,this.numSubsets):
            e = Entity( model=Mesh(),
                        texture=this.textureAtlas)
            e.texture_scale*=64/e.texture.width
            this.subsets.append(e)
        

    def genBlock(this,x,y,z):
        # Extend or add to the vertices of our model.
        model = this.subsets[this.currentSubset].model

        model.vertices.extend([ Vec3(x,y,z) + v for v in 
                                this.block.vertices])
        # Record terrain in dictionary :)
        this.td["x"+str(floor(x))+
                "y"+str(floor(y))+
                "z"+str(floor(z))] = "t"
        # Decide random tint for colour of block :)
        c = random()-0.5
        model.colors.extend( (Vec4(1-c,1-c,1-c,1),)*
                                this.numVertices)

        # This is the texture atlas co-ord for grass :)
        uu = 8
        uv = 7
        # ***
        # Occasionally place a soil block.
        if random() > 0.8:
            uu = 10
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
                                "z"+str(floor(z+j)))!="t":
                    this.genBlock(x+k,y,z+j)

        this.subsets[this.currentSubset].model.generate()
        # Current subset hack ;)
        if this.currentSubset<this.numSubsets-1:
            this.currentSubset+=1
        else: this.currentSubset=0
        this.swirlEngine.move()

    # ***
    def update(this,pos,cam):
        highlight(pos,cam,this.td)