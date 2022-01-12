"""
Build/place block functions.
"""
from ursina import Vec3, floor

def checkBuild(key,bte,td):
    if key=='right mouse up':
        bepi = bte + Vec3(0,-0.5,0)
        x = bepi.x = floor(bepi.x)
        y = bepi.y = floor(bepi.y+1)
        z = bepi.z = floor(bepi.z)
        # First, check there isn't already terrain there:
        if td.get((x,y,z))!='g' and \
           td.get((x,y,z))!=None:
            print('Nope-terrain there already, bub.')
            return None 
        return bepi
    else: return None

def gapShell(td,bsite):
    wp =[   Vec3(0,1,0),
            Vec3(0,-1,0),
            Vec3(-1,0,0),
            Vec3(1,0,0),
            Vec3(0,0,-1),
            Vec3(0,0,1)]
    for i in range(0,6):
        p = bsite + wp[i]
        if td.get((floor(p.x),floor(p.y),floor(p.z)))==None:
            td[(floor(p.x),floor(p.y),floor(p.z))]='g'