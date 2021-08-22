"""
Minecraft in Python, with Ursina, tut 11
Petter Amland :)
3.2) Dictionary for stepping onto built blocks
4) Caves
5) Layers of terrain
DONE 6) Axe model
7) Fog darkens/changes colour as we descend height
DONE 8) Trees

9.-1) use round instead of floor for subject position.

9.0) Break out of subsets loop after mining.
9.1) 3D Cave_Dictionary - for recording y pos too.
9.2) Spawn and combine(?) 5 new blocks when mining.
9.3) Figure out where to spawn if mining sideways.
9.4) Improve controls (better replicate Minecraft's).

9.2) ELABORATION: adjust genTerrain for new 3D dictionary
        have to use Perlin twice. Also, need to correct
        our walking system. We now record built blocks as
        the object itself, and terrain cubes as 'terrain',
        and gaps that have been mined as 'gap'.
        So, how to use these to determine whether subject
        is stepping up or down etc.?   
        Need could use a new subset-like model into which
        spawned blocks during mining and building are
        combined.       
...
DONE near future) axe draw bug
DONE future) (very basic) Mining! 
"""


from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor,abs,sin,cos,radians, round
import time
from perlin_noise import PerlinNoise  
from nMap import nMap
from cave_system import Caves 
from tree_system import Trees

app = Ursina()

# Create a cave system object. It's called anush.
anush = Caves()
# Same again, but for trees :)
sol4r = Trees()

window.color = color.rgb(0,200,211)
window.exit_button.visible = False

prevTime = time.time()

scene.fog_color = color.rgb(0,222,0)
scene.fog_density = 0.02

# Load in textures and models.
grassStrokeTex = 'grass_14.png'
monoTex = 'stroke_mono.png'
wireTex = 'wireframe.png'
stoneTex = 'grass_mono.png'

cubeTex = 'block_texture.png'

cubeModel = 'moonCube'

# ***
axoTex = 'b_axolotl.png'
axoModel = 'b_axolotl.obj'

axeModel = 'Diamond-Pickaxe'
axeTex = 'diamond_axe_tex'

# Building code...
bte = Entity(model='cube',texture=wireTex,scale=1.01)
# distance of build (Thanks, Ethan!)
build_distance = 3
# Builds...
builds = Entity(model=cubeModel,texture=stoneTex)


class BTYPE:
    STONE= color.rgb(255,255,255) 
    GRASS= color.rgb(0,255,0)
    SOIL= color.rgb(255,80,100)
    RUBY= color.rgb(255,0,0) 
    NETHERITE= color.rgb(0,0,0)

blockType = BTYPE.SOIL
buildMode = -1  # -1 is OFF, 1 is ON.

def buildTool():
    global build_distance
    if buildMode == -1:
        bte.visible = False
        return
    else: bte.visible = True
    bte.position = round(subject.position +
                    camera.forward * build_distance)
    bte.y += 2
    bte.y = round(bte.y)
    bte.x = round(bte.x)
    bte.z = round(bte.z)
    bte.color = blockType
def build():
    # e = duplicate(bte)
    e = Entity(model='cube',position=bte.position)
    e.scale *= 0.99999
    # e.collider = 'box'
    e.texture = stoneTex
    e.color = blockType
    e.shake(duration=0.5,speed=0.01)
    e.parent = builds
def mine():
    # First check against 'builds' subset.
    
    vChange = False
            
    for v in builds.model.vertices:
        # Is the vertex close enough to
        # where we want to mine (bte position)?
        if (v[0] >= bte.x - 0.5 and
            v[0] <= bte.x + 0.5 and
            v[1] >= bte.y - 0.5 and
            v[1] <= bte.y + 0.5 and
            v[2] >= bte.z - 0.5 and
            v[2] <= bte.z + 0.5):
            # Yes!
            # v[1] -= 1
            v[1] = 999 # 'Delete' block.
            if subDic.get('x'+str(bte.x)+'y'+str(bte.y-1)+'z'+str(bte.z))== None and \
            subDic.get('x'+str(bte.x)+'y'+str(bte.y-1)+'z'+str(bte.z))!= 'gap':
                e = Entity( model=cubeModel,
                            texture=stoneTex,
                            color=BTYPE.SOIL)
                e.position = bte.position
                e.scale *= 0.9
                e.y -= 1
                # We are also going to have to combine this
                # new block into the current subset.
                e.parent = builds
                # Track new position of terrain.
                subDic['x'+str(e.x)+'y'+str(e.y)+'z'+str(e.z)] = e.y
                # Track position of mined gap.
                subDic['x'+str(bte.x)+'y'+str(bte.y)+'z'+str(bte.z)] = 'gap'
            # Note that we have made change.
            vChange = True
        # Record change of height in TERRAIN dictionary :)
        # Which now records y as value. 
    if vChange == True:
        # subsets[s].model.generate() # We have to do this later.
        x = floor(bte.x)
        z = floor(bte.z)
        y = floor(bte.y) - 1
            
        # Now we need to spawn surrounding cubes.
        pos1 = (x+1,y+1,z)
        pos2 = (x-1,y+1,z)
        pos3 = (x,y+1,z+1)
        pos4 = (x,y+1,z-1)
        spawnPos = []
        spawnPos.append(pos1)
        spawnPos.append(pos2)
        spawnPos.append(pos3)
        spawnPos.append(pos4)
        for i in range(4):
            x = spawnPos[i][0]
            z = spawnPos[i][2]
            y = spawnPos[i][1]
            if  subDic.get('x'+str(x)+'y'+str(y)+'z'+str(z)) == None and \
                subDic.get('x'+str(x)+'y'+str(y-1)+'z'+str(z))== None and \
                subDic.get('x'+str(x)+'y'+str(y-1)+'z'+str(z))!='gap' and \
                subDic.get('x'+str(x)+'y'+str(y)+'z'+str(z))!='gap':
                e = Entity( model=cubeModel,
                            texture=stoneTex,
                            color=BTYPE.SOIL)
                e.position = spawnPos[i]
                e.scale *= 0.99999
                e.parent = builds
                # Store position of block on main dictionary.
                subDic['x'+str(e.x)+'y'+str(e.y)+'z'+str(e.z)] = e.y
                # This is so that we can mine it (destroy it).
                print('spawned mine wall ' + str(i))
            # anush.makeCave(bte.x,bte.z,bte.y-1)
        builds.model.generate()
        builds.combine()   

    # Now check through all terrain subsets...
    for s in range(len(subsets)):
        # First, check to see if built block here.
        # If so, we can destroy it, and break.
        # Oh, but how do we get hold of it?
        # Perhaps save it in a new dictionary?
        vChange = False
            
        for v in subsets[s].model.vertices:
            # Is the vertex close enough to
            # where we want to mine (bte position)?
            if (v[0] >= bte.x - 0.5 and
                v[0] <= bte.x + 0.5 and
                v[1] >= bte.y - 0.5 and
                v[1] <= bte.y + 0.5 and
                v[2] >= bte.z - 0.5 and
                v[2] <= bte.z + 0.5):
                # Yes!
                # v[1] -= 1
                v[1] = 999 # 'Delete' block.
                if subDic.get('x'+str(bte.x)+'y'+str(bte.y-1)+'z'+str(bte.z))== None and \
                subDic.get('x'+str(bte.x)+'y'+str(bte.y-1)+'z'+str(bte.z))!= 'gap':
                    e = Entity( model=cubeModel,
                                texture=stoneTex,
                                color=BTYPE.SOIL)
                    e.position = bte.position
                    e.scale *= 0.99999
                    e.y -= 1
                    # We are also going to have to combine this
                    # new block into the current subset.
                    e.parent = builds
                    # Track new position of terrain.
                    subDic['x'+str(e.x)+'y'+str(e.y)+'z'+str(e.z)] = e.y
                    # Track position of mined gap.
                    subDic['x'+str(bte.x)+'y'+str(bte.y)+'z'+str(bte.z)] = 'gap'
                # Note that we have made change.
                vChange = True
        # Record change of height in TERRAIN dictionary :)
        # Which now records y as value. 
        if vChange == True:
            # subsets[s].model.generate() # We have to do this later.
            x = floor(bte.x)
            z = floor(bte.z)
            y = floor(bte.y) - 1
            
            # Now we need to spawn surrounding cubes.
            pos1 = (x+1,y+1,z)
            pos2 = (x-1,y+1,z)
            pos3 = (x,y+1,z+1)
            pos4 = (x,y+1,z-1)
            spawnPos = []
            spawnPos.append(pos1)
            spawnPos.append(pos2)
            spawnPos.append(pos3)
            spawnPos.append(pos4)
            for i in range(4):
                x = spawnPos[i][0]
                z = spawnPos[i][2]
                y = spawnPos[i][1]
                # Only spawn if no block already there, or
                # if block already underneath this pos.
                # We also don't want to fill in mine shaft...
                # which includes all the way below and above gap.
                # OK -- this does not suffice. Sometimes,
                # for instance, we do need a cave wall to spawn
                # even when a gap exists higher up at this location,
                # since there is intervening terrain. So, we need
                # dictionaries that record x,z, and y to be recorded.
                # So, we could just use one dictionary where the 
                # values are 'gap', or 'terrain', or 'cave_wall', etc.
                if  subDic.get('x'+str(x)+'y'+str(y)+'z'+str(z)) == None and \
                    subDic.get('x'+str(x)+'y'+str(y-1)+'z'+str(z))== None and \
                    subDic.get('x'+str(x)+'y'+str(y-1)+'z'+str(z))!='gap' and \
                    subDic.get('x'+str(x)+'y'+str(y)+'z'+str(z))!='gap':
                    e = Entity( model=cubeModel,
                                texture=stoneTex,
                                color=BTYPE.SOIL)
                    e.position = spawnPos[i]
                    e.scale *= 0.99999
                    e.parent = builds
                    # Store position of block on main dictionary.
                    subDic['x'+str(e.x)+'y'+str(e.y)+'z'+str(e.z)] = e.y
                    # This is so that we can mine it (destroy it).
                    print('spawned mine wall ' + str(i))
            # anush.makeCave(bte.x,bte.z,bte.y-1)
            subsets[s].model.generate()
            builds.combine()   
            break   



def input(key):
    global blockType, buildMode, generating
    global canGenerate
    global build_distance

    # scroll down to build closer or 
    # scroll up to build further
    # Thanks again, Ethanalos! :)
    if key == 'scroll up':
        build_distance -= 1
    if key == 'scroll down':
        build_distance += 1


    if key == 'b' or key == 'escape':
        quit()
    if key == 'g': 
        generating *= -1
        canGenerate *= -1

    if buildMode == 1 and key == 'left mouse up':
        build()
    elif buildMode == 1 and key == 'right mouse up':
        mine()
    
    if key == 'f': buildMode *= -1
    
    if key == '1': blockType=BTYPE.SOIL
    if key == '2': blockType=BTYPE.GRASS
    if key == '3': blockType=BTYPE.STONE
    if key == '4': blockType=BTYPE.RUBY
    if key == '5': blockType=BTYPE.NETHERITE

def update():
    global prevZ, prevX, prevTime, genSpeed, perCycle
    global rad, origin, generating, canGenerate, theta
    if  abs(subject.z - prevZ) > 1 or \
        abs(subject.x - prevX) > 1:
            origin=subject.position
            rad=0
            theta=0
            generating = 1 * canGenerate
            prevZ = subject.z
            prevX = subject.x
            
    
    generateShell()

    if time.time() - prevTime > genSpeed:
        for i in range(perCycle):
            genTerrain()
        prevTime = time.time()  
    
    vincent.look_at(subject, 'forward')
    # vincent.rotation_x = 0

    buildTool()

noise = PerlinNoise(octaves=1,seed=1220115)

megasets = []
subsets = []
subCubes = []
# New variables :)
generating = 1 # -1 if off.
canGenerate = 1 # -1 if off.
genSpeed = 0
perCycle = 64
currentCube = 0
currentSubset = 0
numSubCubes = 64
numSubsets = 420 # I.e. how many combined into a megaset?
theta = 0
rad = 0
# Dictionary for recording whether terrain blocks exist
# at location specified in key.
subDic = {}

# Instantiate our 'ghost' subset cubes.
for i in range(numSubCubes):
    bud = Entity(model=cubeModel,texture=cubeTex)
    bud.scale *= 0.99999
    bud.rotation_y = random.randint(1,4)*90
    bud.disable()
    subCubes.append(bud)

# Instantiate our empty subsets.
for i in range(numSubsets):
    bud = Entity(model=cubeModel)
    bud.texture = cubeTex
    bud.disable()
    subsets.append(bud)

def genPerlin(_x, _z, plantTree=False):
    y = 0
    freq = 64
    amp = 42      
    y += ((noise([_x/freq,_z/freq]))*amp)
    freq = 32
    amp = 21
    y += ((noise([_x/freq,_z/freq]))*amp)

    # Is there are cave-gap here?
    # If so, lower the cube by 32...or something ;)
    whatCaveHeight = anush.checkCave(_x, _z)
    if whatCaveHeight != None:
        y = whatCaveHeight
    elif plantTree==True:
        sol4r.checkTree(_x,y,_z)

    return floor(y)

def genTerrain():
    global currentCube, theta, rad, currentSubset
    global generating

    if generating==-1: return

    # Decide where to place new terrain cube!
    x = floor(origin.x + sin(radians(theta)) * rad)
    z = floor(origin.z + cos(radians(theta)) * rad)
    # Check whether there is terrain here already...
    if subDic.get('x'+str(x)+'y'+str(genPerlin(x,z))+'z'+str(z))==None:
        subCubes[currentCube].enable()
        subCubes[currentCube].x = x
        subCubes[currentCube].z = z
        
        subCubes[currentCube].parent = subsets[currentSubset]
        # Pass in true to allow tree generation here.
        y = subCubes[currentCube].y = genPerlin(x,z,True)
        subDic['x'+str(x)+'y'+str(y)+'z'+str(z)] = y
        # OK -- time to decide colours :D
        c = nMap(y,-8,21,132,212)
        c += random.randint(-32,32)
        subCubes[currentCube].color = color.rgb(c,c,c)
        subCubes[currentCube].disable()
        currentCube+=1

        # Ready to build a subset?
        if currentCube==numSubCubes:
            subsets[currentSubset].combine(auto_destroy=False)
            subsets[currentSubset].enable()
            currentSubset+=1
            currentCube=0
            
            # And ready to build a megaset?
            if currentSubset==numSubsets:
                megasets.append(Entity( model=cubeModel,
                                        texture=cubeTex))
                # Parent all subsets to our new megaset.
                for s in subsets:
                    s.parent=megasets[-1]
                # In case user has Ursina version 3.6.0.
                # safe_combine(megasets[-1],auto_destroy=False)
                megasets[-1].combine(auto_destroy=False)
                for s in subsets:
                    s.parent=scene
                currentSubset=0
                print('Megaset #' + str(len(megasets))+'!')
            
    else:
        pass
        # print('TC at ' + 'x'+str(x)+'y'+str(genPerlin(x,z))+'z'+str(z))
        # There was terrain already there, so
        # continue rotation to find new terrain spot.
    
    if rad > 0:
        theta += 45/rad
    else: rad+=0.5
    
    if theta >= 360:
        theta = 0
        rad += 0.5

shellies = []
shellWidth = 3
for i in range(shellWidth*shellWidth):
    bud = Entity(model='cube',collider='box')
    bud.visible=False
    shellies.append(bud)

# Our new gravity system for moving the subject :)
def generateShell():
    global subject, grav_speed, grav_acc, subDic

    """
    OK -
    first bias stepping up. So, FIRST check whether there
    are any blocks above us and <= step_height.
    If yes, lerp to there as target_y.
    If no, then SECOND check whether there are any blocks
    below us and >= step_height. If yes, lerp to there.
    If neither, then use gravity.
    NB that we have to iterate * step_height during our
    check of terrain cubes above or below subject's
    current pos.
    """

    # How high or low can we step/drop?
    step_height = 5
    gravityON = True
    
    target_y = subject.y

    for i in range(step_height,-step_height,-1):
        # What y is the terrain at this position?
        # terra = genPerlin(subject.x,subject.z)
        terra = subDic.get( 'x'+str((round(subject.x)))+
                            'y'+str((floor(subject.y+i)))+
                            'z'+str((round(subject.z))))
        if terra != None and terra != 'gap':
            # print('TERRAIN FOUND! ' + str(terra + 2))
            target_y = terra + 2
            # subject.y = terra + 2
            grav_speed = 0
            gravityON = False
            break

    if gravityON==True:
        # This means we're falling!
        grav_speed += (grav_acc * time.dt)
        subject.y -= grav_speed
    else:
        subject.y = lerp(subject.y, target_y, 9.807*time.dt)
        grav_speed = 0 # Reset gravity speed: grounded.

    """
    # How far are we from the target y?
    # But first, see if gravity override, in which
    # case we pretend that there is a drop, not step.
    if gravityON==True:
        target_dist = -step_height-1 # Pretend drop.
    else: target_dist = target_y - subject.y
    # Can we step up or down?
    if target_dist < step_height and target_dist > -step_height:
        subject.y = lerp(subject.y, target_y, 9.807*time.dt)
        grav_speed = 0 # Reset gravity speed: grounded.
    elif target_dist < -step_height:
        # This means we're falling!
        grav_speed += (grav_acc * time.dt)
        subject.y -= grav_speed
    """

    # global shellWidth
    # for i in range(len(shellies)):
    #     x = shellies[i].x = floor((i/shellWidth) + 
    #                         subject.x - 0.5*shellWidth)
    #     z = shellies[i].z = floor((i%shellWidth) + 
    #                         subject.z - 0.5*shellWidth)
    #     shellies[i].y = genPerlin(x,z)

subject = FirstPersonController()
subject.cursor.visible = False
subject.gravity = 0
grav_speed = 0
grav_acc = 0.1
subject.x = subject.z = 5
subject.y = 32
prevZ = subject.z
prevX = subject.x
origin = subject.position # Vec3 object? .x .y .z
# Our axe :D
axe = Entity(   model=axeModel,
                texture=axeTex,
                scale=0.07,
                position = subject.position,
                always_on_top=True)
axe.x -= 3
axe.z -= 2.2
axe.y -= subject.y
axe.rotation_z = 90
axe.rotation_y = 180
axe.parent=camera

chickenModel = load_model('chicken.obj')
vincent = Entity(model=chickenModel,scale=1,
                x=22,z=16,y=4,
                texture='chicken.png',
                double_sided=True)

luke = Entity(model=axoModel,scale=10,
                x=-22,z=16,y=4,
                texture=axoTex,
                double_sided=True)

generateShell()

app.run()