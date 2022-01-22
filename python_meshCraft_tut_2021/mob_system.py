"""
Mob system and ai
"""
# from ursina import lerp, time, floor, Entity
# from ursina import load_texture, FrameAnimation3d, Vec3
from ursina import *

# guy = Entity(model='panda_mod',texture='panda_tex.png')
guy = FrameAnimation3d('panda_mod_',1)
guy.position = Vec3(0,-2.9,10)
guy.texture = 'panda_tex'
# guy.scale*=3

def move(mob,sub_pos,_td):
    # Looks like we can access lookAt instead of 
    # look_at and therefore pass in a speed.
    # NB 100*time.dt will be close to instant.
    mob.lookAt(sub_pos,10*time.dt)
    mob.rotation = Vec3(0,mob.rotation.y+180,0)

    mob.position = lerp(mob.position,sub_pos,time.dt*0.08)
    # mob.y = _td.get((mob.x,mob.y,mob.z))
    
    blockFound=False
    step = 4
    height = 1
    x = floor(mob.x+0.5)
    z = floor(mob.z+0.5)
    y = floor(mob.y+0.5)
    for i in range(-step,step):
        if _td.get((x,y+i,z))=='t':
            if _td.get((x,y+i+1,z))=='t':
                target = y+i+height+1
                blockFound=True
                break
            target = y+i+height
            blockFound=True
            break
    if blockFound==True:
        # Step up or down :>
        mob.y = lerp(mob.y, target, 6 * time.dt)
    else:
        # Gravity fall :<
        mob.y -= 9.8 * time.dt