"""
Minecraft in Python, with Ursina, tut 7

DONE -1) Theta reset!
DONE 0) Combine subsets into megasets
DONE 1) Create our own subCube model, with texture
DONE 2) rotate subCubes for better texture distribution
DONE 3) colours!
4) More efficient terrain generation
...
future) Mining? 
"""

from random import randrange
from numpy.core.shape_base import block
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor
from numpy import abs
from numpy import sin
from numpy import cos
from numpy import radians
import time
from perlin_noise import PerlinNoise  
from nMap import nMap

app = Ursina()

window.color = color.rgb(0,200,211)
window.exit_button.visible = False

prevTime = time.time()

scene.fog_color = color.rgb(0,222,0)
scene.fog_density = 0.004

grassStrokeTex = load_texture('grass_14.png')
monoTex = load_texture('stroke_mono.png')
wireTex = load_texture('wireframe.png')
stoneTex = load_texture('grass_mono.png')

# cubeTex = load_texture('block_texture.png')
# cubeModel = load_model('moonCube.obj')
cubeTex = load_texture('hexTex.png')
cubeModel = load_model('basic_hex.obj')

axoTex = load_texture('axolotl.png')
axoModel = load_model('axolotl.obj')

bte = Entity(model='cube',texture=wireTex)
class BTYPE:
    STONE= color.rgb(255,255,255) 
    GRASS= color.rgb(0,255,0)
    SOIL= color.rgb(255,80,100)
    RUBY= color.rgb(255,0,0) 

blockType = BTYPE.SOIL
buildMode = -1  # -1 is OFF, 1 is ON.

def buildTool():
    if buildMode == -1:
        bte.visible = False
        return
    else: bte.visible = True
    bte.position = round(subject.position +
                    camera.forward * 3)
    bte.y += 2
    bte.y = round(bte.y)
    bte.x = round(bte.x)
    bte.z = round(bte.z)
    bte.color = blockType
def build():
    e = duplicate(bte)
    e.collider = 'cube'
    e.texture = stoneTex
    e.color = blockType
    e.shake(duration=0.5,speed=0.01)

def input(key):
    global blockType, buildMode, generating
    global canGenerate
    if key == 'q' or key == 'escape':
        quit()
    if key == 'g': 
        generating *= -1
        canGenerate *= -1

    if buildMode == 1 and key == 'left mouse up':
        build()
    elif buildMode == 1 and key == 'right mouse up':
        e = mouse.hovered_entity
        destroy(e)
    
    if key == 'f': buildMode *= -1
    
    if key == '1': blockType=BTYPE.SOIL
    if key == '2': blockType=BTYPE.GRASS
    if key == '3': blockType=BTYPE.STONE
    if key == '4': blockType=BTYPE.RUBY

def update():
    global prevZ, prevX, prevTime, genSpeed, perCycle
    global rad, origin, generating, canGenerate
    global iterations, toIterate, currentVec
    global changes, subPos
    if  abs(subject.z - prevZ) > 1 or \
        abs(subject.x - prevX) > 1:
            subPos.x=floor(subject.x)
            subPos.y=floor(subject.z)
            currentVec = 0
            iterations = 0
            toIterate = 1
            changes = -1
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

noise = PerlinNoise(octaves=1,seed=99)

megasets = []
subsets = []
subCubes = []
# New variables :)
generating = 1 # -1 if off.
canGenerate = 1 # -1 if off.
genSpeed = 0.01
perCycle = 64
currentCube = 0
currentSubset = 0
numSubCubes = 32
numSubsets = 420 # I.e. how many combined into a megaset?
theta = 0
rad = 0
# Dictionary for recording whether terrain blocks exist
# at location specified in key.
subDic = {}

# For new position of subset.
currentVec = 0
iterations = 0
toIterate = 1
changes = -1
subPos = Vec2(0,0)
swirlVecs = [
    Vec2(0,0),
    Vec2(0,1),
    Vec2(1,0),
    Vec2(0,-1),
    Vec2(-1,0)
]

# Instantiate our 'ghost' subset cubes.
for i in range(numSubCubes):
    bud = Entity(model=cubeModel)
    # bud.rotation_y = random.randint(1,4)*90
    bud.disable()
    subCubes.append(bud)

# Instantiate our empty subsets.
for i in range(numSubsets):
    bud = Entity(model=None)
    bud.texture = cubeTex
    bud.disable()
    subsets.append(bud)

def genPerlin(_x, _z):
    y = 0
    freq = 64
    amp = 42      
    y += ((noise([_x/freq,_z/freq]))*amp)
    freq = 32
    amp = 21
    y += ((noise([(_x)/freq,(_z)/freq]))*amp)
    return floor(y)

def genTerrain():
    global currentCube, theta, rad, currentSubset
    global generating
    global iterations, toIterate, currentVec
    global changes, subPos

    if generating==-1: return

    # Decide where to place new terrain cube!
    subPos.x += floor(swirlVecs[currentVec].x)
    subPos.y += floor(swirlVecs[currentVec].y)
    x = subPos.x
    z = subPos.y
    # Check whether there is terrain here already...
    if subDic.get('x'+str(x)+'z'+str(z))!='i':
        subCubes[currentCube].enable()
        subCubes[currentCube].x = x
        subCubes[currentCube].z = z
        subDic['x'+str(x)+'z'+str(z)] = 'i'
        subCubes[currentCube].parent = subsets[currentSubset]
        y = subCubes[currentCube].y = genPerlin(x,z)
        g = nMap(y,-16,16,0,220)
        g += random.randint(-12,12)
        subCubes[currentCube].color = color.rgb(g,g,g)
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
                megasets.append(Entity(texture=cubeTex))
                # Parent all subsets to our new megaset.
                for s in subsets:
                    s.parent=megasets[-1]
                megasets[-1].combine(auto_destroy=False)
                currentSubset=0
                print('Megaset #' + str(len(megasets))+'!')

    else:
        pass
        # print('Bump!')
        # There was terrain already there, so
        # continue rotation to find new terrain spot.
    
    # Co-ordinate new vector by iteration around swirl.
    iterations+=1
    if iterations == toIterate:
        currentVec+=1
        if currentVec == len(swirlVecs):
            currentVec = 1
        changes+=1
        iterations = 0
        if changes == 2:
            changes=0
            toIterate+=1

shellies = []
shellWidth = 3
for i in range(shellWidth*shellWidth):
    bud = Entity(model='cube',collider='box')
    bud.visible=False
    shellies.append(bud)

def generateShell():
    global shellWidth
    for i in range(len(shellies)):
        x = shellies[i].x = floor((i/shellWidth) + 
                            subject.x - 0.5*shellWidth)
        z = shellies[i].z = floor((i%shellWidth) + 
                            subject.z - 0.5*shellWidth)
        shellies[i].y = genPerlin(x,z)

subject = FirstPersonController()
subject.cursor.visible = False
subject.gravity = 0.1
subject.x = subject.z = 5
subject.y = 24
prevZ = subject.z
prevX = subject.x
origin = subject.position # Vec3 object? .x .y .z

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