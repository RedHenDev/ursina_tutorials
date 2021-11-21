"""
So, we want, first, to create a highlight at position.
Oh- we could add colider to this object too :) - for
building relative to specific face...?
"""
from ursina import color, Entity

bte = Entity(model='cube',color=color.rgba(1,1,0,0.4))
bte.scale*=1.001

def highlight(pos,cam,td):
    wp=pos+cam.forward*5
    x = int(wp.x)
    y = int(wp.y+3)
    z = int(wp.z)
    bte.x = x
    bte.z = z
    bte.y = y+0.5
    
    if td.get(  "x"+str(x)+
                "y"+str(y)+
                "z"+str(z))=="t":
        bte.visible=True 
    else:
        bte.visible=False   
        # td[ "x"+str(bte.x)+
        #     "y"+str(bte.y)+
        #     "z"+str(bte.z)]=None