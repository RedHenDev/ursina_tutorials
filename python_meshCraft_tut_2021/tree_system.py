"""
Our Tree system :)
"""
from perlin_module import PerlinNoise

class TreeSystem:
    @staticmethod
    def setup():
        # Create our Perlin noise object.
        treeOctaves=8
        treeSeed=2022
        TreeSystem.amp=10
        TreeSystem.freq=256
        TreeSystem.noise=PerlinNoise(
                octaves=treeOctaves,
                seed=treeSeed)

    def genTree(_x,_z):
        # Check whether to generate a tree here...
        if _x % 3==0: return 0
        if _z % 3==0: return 0
        if _x % 5==0: return 0
        if _z % 5==0: return 0
        if _x % 7==0: return 0
        if _z % 7==0: return 0
        if _x % 2==0: return 0
        if _z % 2==0: return 0

        ent=TreeSystem.noise(([  _x/TreeSystem.freq,
                                _z/TreeSystem.freq]))
        ent*=TreeSystem.amp
        if ent>1:
            return ent
        else:
            return 0


TreeSystem.setup()