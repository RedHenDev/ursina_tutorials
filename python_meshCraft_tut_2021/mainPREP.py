from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrain import MeshTerrain
from flake import SnowFall
# *** to circumvent TypeError: 'module' object is not callable
import random as ra

app = Ursina()

window.color = color.rgb(0,200,255)
indra = Sky()
indra.color = window.color
subject = FirstPersonController()
subject.gravity = 0.0
subject.cursor.visible=False
window.fullscreen=True

terrain = MeshTerrain()
snowfall = SnowFall(subject)
generatingTerrain=True

for i in range(64):
    terrain.genTerrain()

grass_audio = Audio('step.ogg',autoplay=False,loop=False)
snow_audio = Audio('snowStep.mp3',autoplay=False,loop=False)

pX = subject.x
pZ = subject.z

def input(key):
    global generatingTerrain
    terrain.input(key)
    if key=='g':
        generatingTerrain = not generatingTerrain
    # ***
    if key=='p':
        if guy.is_playing:
            guy.pause()
            guy.is_playing=False
        else: 
            guy.resume()
            guy.is_playing=True

count = 0
def update():
    global count, pX, pZ

    # Highlight terrain block for mining/building...
    terrain.update(subject.position,camera)

    count+=1
    if count == 4:
        
        count=0
        # Generate terrain at current swirl position.
        if generatingTerrain:
            for i in range(4):
                terrain.genTerrain()
        

    # Change subset position based on subject position.
    if abs(subject.x-pX)>1 or abs(subject.z-pZ)>1:
        pX=subject.x
        pZ=subject.z 
        terrain.swirlEngine.reset(pX,pZ)
        # Sound :)
        if subject.y > 4:
            if snow_audio.playing==False:
                snow_audio.pitch=ra.random()+0.25
                snow_audio.play()
        elif grass_audio.playing==False:
            grass_audio.pitch=ra.random()+0.7
            grass_audio.play()

    # ***
    mob_move(guy,subject.position,terrain.td)

    blockFound=False
    step = 2
    height = 1.86
    x = floor(subject.x+0.5)
    z = floor(subject.z+0.5)
    y = floor(subject.y+0.5)
    for i in range(-step,step):
        if terrain.td.get((x,y+i,z))=='t':
            if terrain.td.get((x,y+i+1,z))=='t':
                target = y+i+height+1
                blockFound=True
                break
            target = y+i+height
            blockFound=True
            break
    if blockFound==True:
        # Step up or down :>
        subject.y = lerp(subject.y, target, 6 * time.dt)
    else:
        # Gravity fall :<
        subject.y -= 9.8 * time.dt

# ***
# Mobs deserve their own module :)
# ***
from mob_system import *

app.run()