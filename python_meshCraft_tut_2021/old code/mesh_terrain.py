"""
MeshTerrain class :)
"""
from ursina import *

class MeshTerrain:
    def __init__(this):

        this.subsets = []
        this.subNum = 128
        this.subWidth = 4
        this.blockTotal = this.subWidth*this.subWidth
        this.blockCount = 0

        this.block = load_model('block.obj')
        this.texture = 'texture_atlas_3.png'

    def setup_subsets(this):

        for i in range(this.subNum):
            e = Entity( model=Mesh(),
                        texture=this.texture)
            e.scale*=64/e.texture.width
            this.subsets.append(e)

    def paintTerrain(this):

        wid = this.subWidth

        for j in range(-wid, wid):
            for k in range(-wid,wid)