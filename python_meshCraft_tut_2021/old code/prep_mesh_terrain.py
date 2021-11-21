from perlin import Perlin
from ursina import *
from random import random
# ***
from swirl import SwirlEngine

class MeshTerrain:
    def __init__(this):
        
        this.block = load_model('block.obj')
        this.textureAtlas = 'texture_atlas_3.png'

        this.subsets = []
        this.numSubsets = 256
        this.subWidth = 12
        # ***
        this.currentSubset=0
        this.count=0
        this.swirlEngine = SwirlEngine(this.subWidth)

        # Our terrain dictionary :D
        this.td = {}

        this.perlin = Perlin()

        for i in range(this.numSubsets):
            e = Entity( model=Mesh(),
                        texture=this.textureAtlas)
            e.texture_scale*=64/e.texture.width
            this.subsets.append(e)
        

    def genBlock(this,x,y,z):
        model = this.subsets[this.currentSubset].model
        # Extend or add to the vertices of our model.
        model.vertices.extend([ Vec3(x,y,z) + v for v in 
                                this.block.vertices])
        # Record terrain in dictionary :)
        this.td["x"+str(floor(x))+
                "y"+str(floor(y))+
                "z"+str(floor(z))] = "t"
        # ***
        cc = random()*0.5
        model.colors.extend((   Vec4(1-cc,1-cc,1-cc,1),) * 
                                len(this.block.vertices))

        # This is the texture atlas co-ord for grass :)
        uu = 10
        uv = 7
        if y > 2:
            uu = 8
            uv = 6
        model.uvs.extend([Vec2(uu,uv) + u for u in this.block.uvs])


    def genTerrain(this):

        x = 0
        z = 0
        # ***
        x = this.swirlEngine.pos.x
        z = this.swirlEngine.pos.y

        d = int(this.subWidth*0.5)

        for k in range(-d,d):
            for j in range(-d,d):

                y = floor(this.perlin.getHeight(x+k,z+j))
                # ***
                if this.td.get( "x"+str(floor(x+k))+
                                "y"+str(floor(y))+
                                "z"+str(floor(z+j)))==None:
                    this.genBlock(x+k,y,z+j)
                    this.count+=1
                    # ***
                    if this.count==this.subWidth*this.subWidth:
                        this.subsets[this.currentSubset].model.generate()
                        this.currentSubset+=1
                        this.count=0

        # if madeNew==True:
            # this.subsets[this.currentSubset].model.generate()

        # *** Swirl to next position.
        this.swirlEngine.move()
        if this.currentSubset==this.numSubsets-1:
            this.currentSubset=0