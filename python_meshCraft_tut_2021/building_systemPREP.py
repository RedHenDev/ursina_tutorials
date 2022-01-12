"""
Build/place block functions.
"""
from ursina import Vec3, floor

def checkBuild(key,bte):
    if key=='right mouse up' and bte.visible==True:
        epi = bte.position + Vec3(0,1,0)
        epi.x = floor(epi.x)
        epi.y = floor(epi.y)
        epi.z = floor(epi.z)
        return epi