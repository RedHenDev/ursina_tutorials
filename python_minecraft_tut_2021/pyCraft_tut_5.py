"""
Minecraft in Python, with Ursina, tut 5

1) change building block type DONE
2) toggle build mode DONE
3) prevent building when already entity present
"""

from random import randrange
from numpy.core.shape_base import block
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor
from numpy import abs
import time
from perlin_noise import PerlinNoise  
from nMap import nMap

app = Ursina()

window.color = color.rgb(0,200,211)
window.exit_button.visible = False

prevTime = time.time()

scene.fog_color = color.rgb(0,222,0)
scene.fog_density = 0.02

grassStrokeTex = load_texture('grass_14.png')
monoTex = load_texture('stroke_mono.png')
wireTex = load_texture('wireframe.png')
stoneTex = load_texture('grass_mono.png')

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
    global blockType, buildMode
    if key == 'q' or key == 'escape':
        quit()
    if key == 'g': generateSubset()

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
    global prevZ, prevX, prevTime, amp
    if  abs(subject.z - prevZ) > 1 or \
        abs(subject.x - prevX) > 1:
            generateShell()

    if time.time() - prevTime > 0.05:
        generateSubset()
        prevTime = time.time()  
    
    # Safety net in case of glitching through terrain :)
    if subject.y < -amp-1:
        subject.y = 2 + floor((noise([subject.x/freq,
                            subject.z/freq]))*amp)
        subject.land()

    vincent.look_at(subject, 'forward')
    # vincent.rotation_x = 0

    buildTool()

noise = PerlinNoise(octaves=4,seed=99)
amp = 24
freq = 100
terrain = Entity(model=None,collider=None)
terrainWidth = 40
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
    
    subsets[currentSubset].combine(auto_destroy=False)
    # subsets[currentSubset].texture = monoTex
    sci += subWidth
    currentSubset += 1

terrainFinished = False
def finishTerrain():
    global terrainFinished
    if terrainFinished==True: return
    terrain.texture = grassStrokeTex
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