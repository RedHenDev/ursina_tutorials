# Mobs deserve their own mobule :)

from ursina import *

grey = FrameAnimation3d('panda_walk_',fps=1)
grey.texture='panda_tex'
grey.position = Vec3(0,-2.9,10)
grey.turnSpeed = 0.002
grey.speed = 1

def mob_movement(mob, subPos, _td):
    # First, turn towards target...
    # Turn speed not affected? BUG
    mob.lookAt(subPos, mob.turnSpeed * time.dt)
    mob.rotation = Vec3(0,mob.rotation.y+180,0)

    # Now move mob towards target...
    # How close can they approach?
    intimacyDist = 10
    # How far away from target?
    dist = subPos-mob.position
    # Magnitude of distance from target examined...
    if dist.length() > intimacyDist:
        # Approach target...
        mob.position -= mob.forward * mob.speed * time.dt
        mob.resume() # Animation.
        mob.is_playing=True
    else:
        mob.pause() # Animation.
        mob.is_playing=False

    terrain_walk(mob, _td)

def terrain_walk(mob, _td):
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
