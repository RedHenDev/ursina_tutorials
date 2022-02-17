"""
Our building system :) 2022
Happy New Year!
"""
from ursina import Vec3, floor

def checkBuild(_bsite,_td,_camF,_pos): 
    # Store in convenient variables and floor.
    # Also -- increment y by 1 - since building above!

    #  OK - we want to decide where to build a new block
    # based on where we're looking.
    # _camF is camera's forward.
    # _pos is the subject's position.
    # First, create some kind of vector from
    # the player's eyes to the highlighted block...
    dist = _bsite - _pos
    mouseInWorld = _pos + _camF * dist.length()
    mouseInWorld -= _camF * 0.75
    x = round(mouseInWorld.x)
    y = floor(mouseInWorld.y)
    z = round(mouseInWorld.z)
    # Oh, but what if we're trying to build inside bte?
    # Build 1 above current block!
    if _bsite == Vec3(x,y,z):
        y+=1

    # x = floor(_bsite.x)
    # y = floor(_bsite.y+1)
    # z = floor(_bsite.z)

    # Make sure no block here already...
    if _td.get((x,y,z))!='g' and _td.get((x,y,z))!=None:
        print("Can't build here, sorry :(") 
        return None
    # If we're here, we can build. Yessssss.
    return Vec3(x,y,z)

def gapShell(_td,_bsite):
    from config import six_cube_dirs
    for i in range(6):
        p = _bsite + six_cube_dirs[i]
        if _td.get((floor(p.x),floor(p.y),floor(p.z)))==None:
            _td[(floor(p.x),floor(p.y),floor(p.z))]='g'