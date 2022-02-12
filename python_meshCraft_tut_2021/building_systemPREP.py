"""
Our building system :) 2022
Happy New Year!
"""
from ursina import Vec3, floor
from PREP_cfg import SIX_DIRS

def checkBuild(_bsite,_td):
    # Adjust build site, since build-tool-entity (bte) offset.
    _bsite += Vec3(0,-0.5,0)
    # Store in convenient variables and floor.
    # Also -- increment y by 1 - since building above!
    x = floor(_bsite.x)
    y = floor(_bsite.y+1)
    z = floor(_bsite.z)
    # Make sure no block here already...
    if _td.get((x,y,z))!='g' and _td.get((x,y,z))!=None:
        print("Can't build here, sorry :(") 
        return None
    # If we're here, we can build. Yessssss.
    return Vec3(x,y,z)

def gapShell(_td,_bsite):
    for i in range(6):
        # ***
        p = _bsite + SIX_DIRS[i]
        x=floor(p.x)
        y=floor(p.y)
        z=floor(p.z)
        if _td.get((x,y,z))==None:
            _td[(x,y,z)]='g'