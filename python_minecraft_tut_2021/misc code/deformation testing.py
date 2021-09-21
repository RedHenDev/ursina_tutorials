"""
Minecraft in Python, with Ursina, tut 5 PREP

1) Different block types - simple class enum
2) build mode... *=-1 toggle
3) Night-time atmos? -- with imported module to model this?
4) clouds
"""

from random import randrange
from ursina import * 
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor
from numpy import abs
import time
from perlin_noise import PerlinNoise  
from nMap import nMap
from weatherCraft import Weather

app = Ursina()

weather = Weather()

weather.setSky()

# window.color = color.rgb(0,200,211)
window.exit_button.visible = False

prevTime = time.time()

scene.fog_color = color.rgb(0,222,0)
scene.fog_density = 0.02

grassStrokeTex = load_texture('grass_14.png')
monoTex = load_texture('stroke_mono.png')
wireTex = load_texture('wireframe.png')
stoneTex = load_texture('grass_mono.png')

bte = Entity(model='cube',texture=wireTex)

def buildTool():
    bte.position = round(subject.position +
                    camera.forward * 3)
    bte.y += 2
    bte.y = round(bte.y)
    bte.x = round(bte.x)
    bte.z = round(bte.z)
def build():
    e = duplicate(bte)
    e.collider = 'cube'
    e.texture = stoneTex
    e.shake(duration=0.5,speed=0.01)
def regenerate(wh, v3):
    global freq, amp, terrainWidth
    for i in range(subWidth):
        x = subCubes[i].x = v3[0]
        z = subCubes[i].z = v3[2]
        y = subCubes[i].y = -1+floor((noise([x/freq,z/freq]))*amp)
        subsets[wh].model = None
        subCubes[i].parent = subsets[wh]

        # Set colour of subCube :D
        y += randrange(-4,4)
        r = 0
        g = 0
        b = 0
        if y > amp*0.3:
            b = 255
        if y == 4:
            r = g = b = 255
        else:
            g = nMap(y, 0, amp*0.5, 0, 255)
        # Red zone?
        if z > terrainWidth*0.5:
            g = 0
            b = 0
            r = nMap(y, 0, amp, 110, 255)     
        subCubes[i].color = color.rgb(r,g,b)
        subCubes[i].visible = False
    subsets[wh].texture = monoTex
    subsets[wh].combine(auto_destroy=False)
def mine():
    global terrain, subsets
    print('Started mining...')
    # First thing, work out which subset and
    # which subCube...
    which = (bte.z*terrainWidth)+(bte.x/(terrainWidth/subWidth))
    which = int(floor(which))
    regenerate(which, bte.position)
    """
    newHole = 0
    for i in terrain.model.vertices:
        if i[0] > bte.x - 0.6 and \
            i[0] < bte.x + 0.6 and \
            i[2] > bte.z - 0.6 and \
            i[2] < bte.z + 0.6:   
            i[1] -= 1
            newHole = Vec3(bte.x,bte.z,i[1])
    if newHole != 0:
        holes.append(newHole)
    terrain.model.generate() 
    e = mouse.hovered_entity
    if e and e.visible == True:
        destroy(e)
# Data recording mined co-ordinates.
holes = [] # List of Vec3s - (x,z,depth)
"""


def input(key):
    if key == 'q' or key == 'escape':
        quit()
    if key == 'g': generateSubset()

    if key == 'left mouse up':
        build()
    elif key == 'right mouse up':
        mine()

def update():
    global prevZ, prevX, prevTime, amp
    if  abs(subject.z - prevZ) > 1 or \
        abs(subject.x - prevX) > 1:
            generateShell()

    if time.time() - prevTime > 0.05:
        generateSubset()
        prevTime = time.time()  
    
    # Safety net in case of glitching through terrain :)
    if subject.y < -amp-2:
        subject.y = floor((noise([subject.x/freq,
                            subject.z/freq]))*amp)
        subject.land()

    vincent.look_at(subject, 'forward')
    # vincent.rotation_x = 0

    buildTool()

    weather.update()

noise = PerlinNoise(octaves=4,seed=99)
amp = 24
freq = 100
terrain = Entity(model=None,collider=None)
terrainWidth = 10
subWidth = int(terrainWidth/10)
subsets = []
subCubes = []
sci = 0 # subCube index.
currentSubset = 0

# Instantiate our 'ghost' subset cubes.
for i in range(subWidth):
    bud = Entity(model='cube')
    subCubes.append(bud)

# Instantiate our empty subsets.
for i in range(int((terrainWidth*terrainWidth)/subWidth)):
    bud = Entity(model=None)
    bud.parent = terrain
    subsets.append(bud)

def generateSubset():
    global sci, currentSubset, freq, amp, terrainWidth
    if currentSubset >= len(subsets): 
        finishTerrain()
        return
    for i in range(subWidth):
        x = subCubes[i].x = floor((i+sci)/terrainWidth)
        z = subCubes[i].z = floor((i+sci)%terrainWidth)
        y = subCubes[i].y = floor((noise([x/freq,z/freq]))*amp)
        subCubes[i].parent = subsets[currentSubset]

        # Set colour of subCube :D
        y += randrange(-4,4)
        r = 0
        g = 0
        b = 0
        if y > amp*0.3:
            b = 255
        if y == 4:
            r = g = b = 255
        else:
            g = nMap(y, 0, amp*0.5, 0, 255)
        # Red zone?
        if z > terrainWidth*0.5:
            g = 0
            b = 0
            r = nMap(y, 0, amp, 110, 255)     
        subCubes[i].color = color.rgb(r,g,b)
        subCubes[i].visible = False
    subsets[currentSubset].texture = monoTex
    subsets[currentSubset].combine(auto_destroy=False)
    sci += subWidth
    currentSubset += 1

terrainFinished = True
def finishTerrain():
    global terrainFinished
    if terrainFinished==True: return
    terrain.texture = monoTex
    terrain.combine()
    terrainFinished = True
    # terrain.texture = grassStrokeTex
    


# for i in range(terrainWidth*terrainWidth):
#     bud = Entity(model='cube',color=color.green)
#     bud.x = floor(i/terrainWidth)
#     bud.z = floor(i%terrainWidth)
#     bud.y = floor((noise([bud.x/freq,bud.z/freq]))*amp)
#     bud.parent = terrain

# terrain.combine()
# terrain.collider = 'mesh'
# terrain.texture = grassStrokeTex

shellies = []
shellWidth = 3
for i in range(shellWidth*shellWidth):
    bud = Entity(model='cube',collider='box')
    bud.visible=False
    shellies.append(bud)

def generateShell():
    global shellWidth, amp, freq
    for i in range(len(shellies)):
        x = shellies[i].x = floor((i/shellWidth) + 
                            subject.x - 0.5*shellWidth)
        z = shellies[i].z = floor((i%shellWidth) + 
                            subject.z - 0.5*shellWidth)
        shellies[i].y = floor((noise([x/freq,z/freq]))*amp)
        # Now check for mined holes...
        # for j in holes:
        #     if x == j[0] and z == j[1]:
        #         shellies[i].y = j[2]
        #         break




subject = FirstPersonController()
subject.cursor.visible = False
subject.gravity = 0.5
subject.x = subject.z = 5
subject.y = 12
prevZ = subject.z
prevX = subject.x

chickenModel = load_model('chicken.obj')
vincent = Entity(model=chickenModel,scale=1,
                x=22,z=16,y=4,
                texture='chicken.png',
                double_sided=True)

generateShell()

app.run()