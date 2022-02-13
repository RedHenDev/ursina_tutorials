"""
Mob system and ai
"""
# Importing everything from ursina module seems
# only way to get texturing loading to work.
from ursina import *

guy = FrameAnimation3d('panda_walk_',fps=1)
guy.position = Vec3(0,-2.9,10)
guy.texture = 'panda_texture'
guy.speed = 1
guy.turn_speed = 1

def mob_move(mob,sub_pos,_td):
    # Looks like we can access lookAt() instead of 
    # look_at() and therefore pass in a speed.
    # NB 100*time.dt will be close to instant.
    # ***
    tempR = mob.rotation
    mob.lookAt(sub_pos)
    mob.rotation = Vec3(0,mob.rotation.y+180,0)
    # ***
    mob.rotation = lerp(tempR,mob.rotation,mob.turn_speed*time.dt)
    dir = mob.position-sub_pos
    if dir.length() > 5:
        mob.position+=-mob.forward*time.dt*mob.speed
        mob.resume()
        mob.is_playing=True
    else:
        mob.pause()
        mob.is_playing=False
    
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
        mob.y = lerp(mob.y, target, 10 * time.dt)
    else:
        # Gravity fall :<
        mob.y -= 9.8 * time.dt