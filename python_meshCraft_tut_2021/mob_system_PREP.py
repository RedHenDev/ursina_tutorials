# Mobs deserve their own mobule :)

from ursina import *

grey = FrameAnimation3d('panda_walk_',fps=1)
# ***
grey.texture='panda_texture'
grey.position = Vec3(0,10,10)
grey.turnSpeed = 1
grey.speed = 3
grey.scale=0.33
# ***
lewlin = Entity(model='creeper.obj',texture='creeper')
lewlin.z=16
lewlin.rotation_y=190
lewlin.scale=0.1
lewlin.turnSpeed = 1
lewlin.speed = 3
lewlin.origin_y-=14
lewlin.y=20
# lewlin.model.colorize(smooth=False, world_space=True)
# ***
def mob_movement(mob, subPos, _td, animated=True):
    # ***
    if not animated:
        mob.model.colorize(smooth=False, world_space=True)

    # First, turn towards target...
    # BUG wiggle walk when aligned with subject?
    tempOR = mob.rotation_y
    mob.lookAt(subPos)
    if animated: rat = 180
    else: rat = 0
    mob.rotation = Vec3(0,mob.rotation.y+rat,0)
    mob.rotation_y = lerp(tempOR,mob.rotation_y,mob.turnSpeed*time.dt)

    # Now move mob towards target...
    # How close can they approach?
    intimacyDist = 3
    # How far away from target?
    dist = subPos-mob.position
    # Magnitude of distance from target examined...
    if dist.length() > intimacyDist:
        # Approach target...
        # ***
        if animated: wd=1
        else: wd=-1
        mob.position -= (mob.forward*wd) * mob.speed * time.dt
        # ***
        if animated:
            mob.resume() # Animation.
            mob.is_playing=True
    else:
        if animated:
            mob.pause() # Animation.
            mob.is_playing=False

    terrain_walk(mob, _td)

def terrain_walk(mob, _td):
    # Check mob hasn't fallen off the planet ;)

    if mob.y < -100:
        mob.y = 100
        print("I've fallen off!")

    blockFound=False
    step = 4
    height = 1
    x = floor(mob.x+0.5)
    z = floor(mob.z+0.5)
    y = floor(mob.y+0.5)
    # Walking on the terrain itself.
    # ***
    for i in range(-2,step+1):
        dot=_td.get((x,y+i,z))
        if dot is not None and dot[0] is not 'g':
            dot=_td.get((x,y+i+1,z))
            if dot is not None and dot[0] is not 'g':
                target = y+i+height+1
                blockFound=True
                break
            # ***
            dot=_td.get((x,y+i+2,z))
            if dot is not None and dot[0] is not 'g':
                target = y+i+height+2
                blockFound=True
                break
            target = y+i+height
            blockFound=True
            break
    if blockFound==True:
        # Step up or down :>
        mob.y = lerp(mob.y, target, 12 * time.dt)
        # We are grounded -- so can jump...
        # if mob.frog is True:
        #     mob.frog=False
        #     mob.y+=jumpHeight
    else:
        # Gravity fall :<
        mob.y -= 9.8 * time.dt
