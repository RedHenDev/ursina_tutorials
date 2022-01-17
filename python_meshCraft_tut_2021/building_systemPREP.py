"""
Our building system :) 2022
Happy New Year!
"""
from ursina import Vec3, floor,Entity

itin = Entity(model='quad')
itin.always_on_top=True

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
    wp =[   Vec3(0,1,0),
            Vec3(0,-1,0),
            Vec3(-1,0,0),
            Vec3(1,0,0),
            Vec3(0,0,-1),
            Vec3(0,0,1)]
    for i in range(6):
        p = _bsite + wp[i]
        if _td.get((floor(p.x),floor(p.y),floor(p.z)))==None:
            _td[(floor(p.x),floor(p.y),floor(p.z))]='g'