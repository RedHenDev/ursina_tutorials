from perlin_module import PerlinNoise

class Perlin:
    def __init__(this):
        
        this.seed = ord('y')+ord('o')
        # Original values: -
        # oct 8 freq 256 amp 24
        # pretty cool, no tears: 16 640 24
        this.octaves = 8
        this.freq = 256
        this.amp = 16    

        this.pNoise = PerlinNoise(  seed=this.seed,
                                    octaves=this.octaves)

    def getHeight(this,x,z):
        from math import sin
        y = 0
        y = this.pNoise([x/(this.freq),z/(this.freq)])*this.amp
        # ***
        y+=sin(z)*0.33
        y+=sin(x*0.5)*0.33
        return y