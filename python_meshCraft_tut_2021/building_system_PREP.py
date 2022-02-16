"""
Our building system :) 2022
Happy New Year!
"""
from ursina import Vec3, floor
# ***
def checkBuild(_bsite,_td,_camF,_pos,_bp):
# def checkBuild(_td,_bp):
    # Adjust build site, since build-tool-entity (bte) offset.
    # _bsite += Vec3(0,-0.5,0)
    # Store in convenient variables and floor.
    # Also -- increment y by 1 - since building above!
    # ***
    # _bsite = _bp
    # x = int(_bsite.x)
    # y = int(_bsite.y)
    # z = int(_bsite.z)

    dist = _bsite - _pos
    mouseInWorld = _pos + _camF * dist.length()
    # ***
    mouseInWorld -= _camF * 0.75
    x = round(mouseInWorld.x)
    y = floor(mouseInWorld.y)
    z = round(mouseInWorld.z)
    # Oh, but what if we're trying to build inside bte?
    # Build 1 above current block!
    if _bsite == Vec3(x,y,z):
        y+=1
    # ***
    # _bp.position=Vec3(x,y,z)

    # Make sure no block here already...
    # ***
    if _td.get((x,y,z))!= None and _td.get((x,y,z))[0]!='g':
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
        if _td.get((floor(p.x),floor(p.y),floor(p.z))) is None:
            _td[(floor(p.x),floor(p.y),floor(p.z))]=['g',0]