"""Subject terrain collisions -- i.e. not ghosting
through walls etc."""

from ursina import Vec3, held_keys, time, floor, lerp

def bumpWall(subject,terrain):
    blockFound=False
    step = 2
    jumpHeight = 3
    # ***
    height = subject.height
    x = round(subject.x)
    z = round(subject.z)
    y = round(subject.y)
    # Simple wall collision detection.
    # Front and Back.
    # inF is location of block ahead, behind, side, etc.
    def checkBump(inF):
        # ***
        for i in range(1,round(subject.height)):
            # ***
            whatval = terrain.td.get(  (round(inF.x),
                                floor(inF.y+i),
                                round(inF.z)) )
            if whatval is not None and whatval[0] is not 'g':
                return True
        return False
    # In front...
    # Also check diagonal left and right...
    howClose=0.55
    rPos=Vec3(x,y,z)
    subFor=subject.forward
    subFor.y=0
    bDir=rPos+subFor*howClose
    if (checkBump(bDir) or
        checkBump(bDir+subject.left*howClose*0.5) or
        checkBump(bDir+subject.right*howClose*0.5)):
        held_keys['w'] = 0
    # Behind...
    bDir=rPos-subFor*howClose
    if (checkBump(bDir) or
        checkBump(bDir+subject.left*howClose*0.5) or
        checkBump(bDir+subject.right*howClose*0.5)):
        held_keys['s'] = 0
    # Left...
    subFor=subject.left
    subFor.y=0
    bDir=rPos+subFor*howClose
    if (checkBump(bDir) or
        checkBump(bDir+subject.forward*howClose*0.5) or
        checkBump(bDir+subject.back*howClose*0.5)):
        held_keys['a'] = 0
    # Right...
    bDir=rPos-subFor*howClose
    if (checkBump(bDir) or
        checkBump(bDir+subject.forward*howClose*0.5) or
        checkBump(bDir+subject.back*howClose*0.5)):
        held_keys['d'] = 0
        
    # Walking on the terrain itself.
    for i in range(-2,step+1):
        dot=terrain.td.get((x,y+i,z))
        if dot is not None and dot[0] is not 'g':
            dot=terrain.td.get((x,y+i+1,z))
            if dot is not None and dot[0] is not 'g':
                target = y+i+height+1
                blockFound=True
                break
            # ***
            dot=terrain.td.get((x,y+i+2,z))
            if dot is not None and dot[0] is not 'g':
                target = y+i+height+2
                blockFound=True
                break
            target = y+i+height
            blockFound=True
            break
    if blockFound==True:
        # Step up or down :>
        # *** speed of lerp increased to 9...
        subject.y = lerp(subject.y, target, 9 * time.dt)
        # We are grounded -- so can jump...
        if subject.frog is True:
            subject.frog=False
            subject.y+=jumpHeight
    else:
        # Gravity fall :<
        subject.y -= 9.8 * time.dt