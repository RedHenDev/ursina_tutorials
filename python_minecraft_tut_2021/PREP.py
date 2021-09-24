"""
Minecraft in Python, with Ursina, tut 18
Petter Amland :)
DONE 3.2) Dictionary for stepping onto built blocks
DONE 3.3) Tower-step algorithm - prevent smooth climb
DONE 3.4) Improve tower-step algorithm -- prevent pushing us
        through terrain bottom. Also, seems to require
        too tall a tower (i.e. > step-height + 1).
3.5) Teleport glitch -- how to make tower-builds solid? Hack
        just glitches us through walls etc. at the moment.
4) Caves - adapt the legacy system
DONE 5) Layers of terrain
DONE 6) Axe model
7) Fog darkens/changes colour as we descend height
DONE 8) Trees

...
DONE near future) axe draw bug
DONE future) (very basic) Mining!

DONE 9.0) Layers/Depth in terrain
DONE 9.1) Break from loop once mined
DONE 9.2) Create dedicated mining/building module
DONE 9.2.1) Does it work?
DONE 9.3) Different material types in layers (ores etc.)
9.31) Biomes! :D - colours and perlin changes
DONE 9.4) Correct spawning when 'mining' a built block
DONE 9.5) Improve block type selection via number keys
9.6) Bug - prevent gaps in terrain when spawning sometimes.

10.0) Smooth performance when building etc.
10.01) Plus at very start of game - move player forward?
DONE 10.1) Combine trees for efficiency
10.2) Improve build tool UI system (closer to Minecraft)
11) Save file -- e.g. current terrain with builds etc.
DONE 12) Axe animation
12.2) Improve axe animation.
DONE 13) Disable megaset system (for now)
DONE 14) Random seed for the terrain - display seed with Text()
DONE 15.0) Update the walking/gravity system (xYz)
DONE 15.01) Subject not aligned with terrain perfectly?
        (Do we just add 0.5 to both x and z in gravity system?)
DONE 15.1) Incorporate building in the new mining system

16.0) Enums for blocktypes
17) Add seed stuff to its own module - thank you.
DONE 18) Prevent building on top of extant blocks.

"""

from random import randrange
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor,abs,sin,cos,radians
import time
from perlin_noise import PerlinNoise  
from nMap import nMap
from cave_system import Caves 
from tree_system import Trees
from mining_PREP import Mining_system

app = Ursina()

# Our main character.
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

# Load in textures and models.
grassStrokeTex = 'grass_14.png'
monoTex = 'stroke_mono.png'
stoneTex = 'grass_mono.png'

cubeTex = 'block_texture.png'

cubeModel = 'moonCube.obj'

axoTex = 'axolotl.png'
axoModel = 'axolotl.obj'

axeModel = 'Diamond-Pickaxe'
axeTex = 'diamond_axe_tex'

# Important variables (e.g. for terrain generation).
noise = PerlinNoise(octaves=1,seed=int(randrange(99,111)))
seedMouth = Text(   text='<white><bold>Your seed, today, sir, is ' + 
                    str(noise.seed),background=True)
seedMouth.background.color = color.orange
seedMouth.scale *= 1.4
seedMouth.x = -0.52
seedMouth.y = 0.4
seedMouth.appear(speed=0.15)

# print('seed is ' + str(noise.seed))

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
currentMegaset = 0
numSubCubes = 64
numSubsets = 16 # I.e. how many combined into a megaset?
theta = 0
rad = 0
# Dictionary for recording whether terrain blocks exist
# at location specified in key.
subDic = {}

# Instantiate our empty subsets.
for i in range(numSubsets):
    bud = Entity(model=cubeModel)
    bud.texture = cubeTex
    bud.disable()
    subsets.append(bud)

# Instantiate our empty subsets.
for i in range(420):
    bud = Entity(model=cubeModel)
    bud.texture = cubeTex
    bud.disable()
    megasets.append(bud)

# Our axe :D
axe = Entity(   model=axeModel,
                texture=axeTex,
                scale=0.07,
                position = subject.position,
                always_on_top=True)

# Create a cave system object. It's called anush.
anush = Caves()
# Same again, but for trees :)
sol4r = Trees()
# And again, but for out mining system (built tools etc.).
varch = Mining_system(subject,axe,camera,subsets,megasets)

window.color = color.rgb(0,200,211)
window.exit_button.visible = False

prevTime = time.time()

scene.fog_color = color.rgb(0,222,0)
scene.fog_density = 0.02


def input(key):
    import pickle
    import os
    global generating, canGenerate

    # Deal with mining system's key inputs. Thanks.
    varch.input(key)
    # 'Smooth building' -- i.e. switch off
    # terrain generation when in build mode automatically.
    # On again if not in build mode (not automatic).
    if varch.buildMode == 1:
        generating = -1
        canGenerate = -1
    
    if key == 'q' or key == 'escape':
        quit()
    if key == 'g': 
        generating *= -1
        canGenerate *= -1
    
    if key == 'b':
        # os.path.realpath(__file__)
        with open('test_save.anush', 'wb') as f:
            pickle.dump(varch.tDic, f)
    

# Main game loop :D
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

    # Controls mining and building functions.
    varch.buildTool()



# Instantiate our 'ghost' subset cubes.
for i in range(numSubCubes):
    bud = Entity(model=cubeModel,texture=cubeTex)
    bud.scale *= 0.99999
    bud.rotation_y = random.randint(1,4)*90
    bud.disable()
    subCubes.append(bud)



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
    global generating, currentMegaset

    if generating==-1: return

    # Decide where to place new terrain cube!
    x = floor(origin.x + sin(radians(theta)) * rad)
    z = floor(origin.z + cos(radians(theta)) * rad)
    # Check whether there is terrain here already...
    if subDic.get('x'+str(x)+'z'+str(z))!='i':
        subCubes[currentCube].enable()
        subCubes[currentCube].x = x
        subCubes[currentCube].z = z
        subCubes[currentCube].parent = subsets[currentSubset]
        y = subCubes[currentCube].y = genPerlin(x,z,True)
        # Record position of this terrain in both
        # the subDic and the mining system's dictionary.
        subDic['x'+str(x)+'z'+str(z)] = 'i'
        varch.tDic['x'+str(x)+'y'+str(y)+'z'+str(z)]=y
        # OK -- time to decide colours :D
        c = nMap(y,-8,21,132,212)
        c += random.randint(-32,32)
        subCubes[currentCube].color = color.rgb(c,c,c)
        subCubes[currentCube].disable()
        currentCube+=1

        # Ready to build a subset?
        if currentCube==numSubCubes:
            # ***
            # Declare and set 'location' of subset to centre subCube...
            subsets[currentSubset].location = subCubes[32].position
            subsets[currentSubset].combine(auto_destroy=False)
            subsets[currentSubset].enable()
            currentSubset+=1
            currentCube=0
            
            # And ready to build a megaset?
            if currentSubset==numSubsets:
                currentSubset=0
                print('Hey -- is everything working?')
                print('*** Check the megaset stuff! :)')
                
                # megasets.append(Entity( model=cubeModel,
                #                         texture=cubeTex))
                # Parent all subsets to our new megaset.
                for s in subsets:
                    s.parent=megasets[currentMegaset]
                # In case user has Ursina version 3.6.0.
                # safe_combine(megasets[-1],auto_destroy=False)
                megasets[currentMegaset].combine(auto_destroy=False)
                for s in subsets:
                    s.parent=scene
                currentSubset=0
                print('Megaset #' + str(currentMegaset)+'!')
                currentMegaset+=1
                
    else:
        pass
        # There was terrain already there, so
        # continue rotation to find new terrain spot.
    
    if rad > 0:
        theta += 45/rad
    else: rad+=0.5
    
    if theta >= 360:
        theta = 0
        rad += 0.5


# Our new gravity system for moving the subject :)
def generateShell():
    global subject, grav_speed, grav_acc

    # New 'new' system :D
    # How high or low can we step/drop?
    step_height = 3
    subjectHeight = 2
    gravityON = True
    
    target_y = subject.y

    for i in range(step_height,-step_height,-1):
        # What y is the terrain at this position?
        # terra = genPerlin(subject.x,subject.z)
        terra = varch.tDic.get( 'x'+str((floor(subject.x+0.5)))+
                                'y'+str((floor(subject.y+i)))+
                                'z'+str((floor(subject.z+0.5))))
        # *** Tower algorithm -- to prevent being sucked up
        # beyond step-height -- bug is that it may force us
        # through the bottom of terrain.
        terraTop = varch.tDic.get( 'x'+str((floor(subject.x+0.5)))+
                                'y'+str((floor(subject.y+i+1)))+
                                'z'+str((floor(subject.z+0.5))))
        if terra != None and terra != 'gap':
            gravityON = False
            if terraTop == None or terraTop == 'gap':
                # print('TERRAIN FOUND! ' + str(terra + 2))
                target_y = floor(subject.y+i) + subjectHeight
                break
            
            # If here, then tower is too tall.
            # So, move subject from this position.
            subject.x -= 0.6
            subject.z -= 0.6

    if gravityON==True:
        # This means we're falling!
        grav_speed += (grav_acc * time.dt)
        subject.y -= grav_speed
    else:
        subject.y = lerp(subject.y, target_y, 9.807*time.dt)
        grav_speed = 0 # Reset gravity speed: gfloored.

    # 'New' old system.
    """
    # How high or low can we step/drop?
    step_height = 5

    # What y is the terrain at this position?
    target_y = genPerlin(subject.x,subject.z) + 2

    # How far are we from the target y?
    target_dist = target_y - subject.y
    # Can we step up or down?
    if target_dist < step_height and target_dist > -step_height:
        subject.y = lerp(subject.y, target_y, 9.807*time.dt)
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

baby = Entity(model=axoModel,scale=10,
                x=-22,z=16,y=4,
                texture=axoTex,
                double_sided=True)

generateShell()

app.run()
