

# from perlin_noise import PerlinNoise
from perlin_noise_module import PerlinNoise

class Perlin:
    def __init__(this):

        this.octaves = 3
        this.seed = 123
        this.freq = 64
        this.amp = 12
        this.pNoise = PerlinNoise(  octaves=this.octaves,
                                    seed=this.seed)

    def getHeight(this, x, z):
        y = this.pNoise([x/this.freq, z/this.freq]) * this.amp
        return y