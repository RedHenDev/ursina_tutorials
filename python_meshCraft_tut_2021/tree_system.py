"""
Our Tree system :)
"""
from perlin_module import PerlinNoise

class TreeSystem:
    @staticmethod
    def setup():
        # Create our Perlin noise object.
        treeOctaves=32
        treeSeed=2022
        TreeSystem.freq=64
        TreeSystem.noise=PerlinNoise(
                octaves=treeOctaves,
                seed=treeSeed)

    def genTree(_x,_z):
        # Check whether to generate a tree here...

        ent=1+TreeSystem.noise(([  _x/TreeSystem.freq,
                                _z/TreeSystem.freq]))
        
        if ent>1.435:
            return ent
        else:
            return 0


TreeSystem.setup()