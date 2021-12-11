"""
So, we want, first, to create a highlight at position.
Oh- we could add colider to this object too :) - for
building relative to specific face...?
"""
from ursina import color, Entity, floor
from ursina.vec3 import Vec3

bte = Entity(model='cube',color=color.rgba(1,1,0,0.4))
bte.scale*=1.001

# ***
def plantIdea(td,vd,subsets):
    if not bte.visible: return
    wv = vd.get('x'+str(floor(bte.x))+
                'y'+str(floor(bte.y))+
                'z'+str(floor(bte.z)))
    for v in range(wv[1]+1,wv[1]+37):
        subsets[wv[0]].model.vertices[v][1]+=999
    subsets[wv[0]].model.generate()
    # g for gap in terrain. And wipe vd entry.
    td[ 'x'+str(floor(bte.x))+
        'y'+str(floor(bte.y))+
        'z'+str(floor(bte.z))] = 'g'
    vd[ 'x'+str(floor(bte.x))+
        'y'+str(floor(bte.y))+
        'z'+str(floor(bte.z))] = None
    return (bte.position + Vec3(0,-0.5,0), wv[0])

# ***
def highlight(pos,cam,td):
    for i in range(1,15):
        wp=pos+cam.forward*i
        x = floor(wp.x)
        y = floor(wp.y+3)
        z = floor(wp.z)
        bte.x = x
        bte.z = z
        bte.y = y+0.5
        
        if td.get(  "x"+str(x)+
                    "y"+str(y)+
                    "z"+str(z))=="t":
            bte.visible=True
            # e = Entity(model='cube')
            # e.collider='box'
            break
        else:
            bte.visible=False   