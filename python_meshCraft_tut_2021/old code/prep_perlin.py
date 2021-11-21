from perlin_module import PerlinNoise
from ursina import math

class Perlin:
    def __init__(this):

        # ***
        this.seed = ord('y')+ord('o')
        this.octaves = 8
        this.freq = 256
        this.amp = 24

        this.pNoise = PerlinNoise(  seed=this.seed,
                                    octaves=this.octaves)

    def getHeight(this,x,z):
        y = 0
        y = this.pNoise([x/this.freq,z/this.freq])*this.amp
        return y