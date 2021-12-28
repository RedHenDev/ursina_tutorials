from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrain import MeshTerrain
from flake import Flake
from random import random

app = Ursina()

window.color = color.rgb(0,200,255)
indra = Sky()
indra.color = window.color
subject = FirstPersonController()
subject.gravity = 0.0
subject.cursor.visible=False
window.fullscreen=False

terrain = MeshTerrain() 
flakes = []
for i in range(512):
    e = Flake(subject.position)
    flakes.append(e)

grass_audio = Audio('step.ogg',autoplay=False,loop=False)
snow_audio = Audio('snowStep.mp3',autoplay=False,loop=False)

pX = subject.x
pZ = subject.z

def input(key):
    terrain.input(key)

count = 0
def update():
    global count, pX, pZ

    for i in range(512):
        flakes[i].physics(subject.position)

    # Generate terrain at current swirl position.
    terrain.genTerrain()

    count+=1
    if count == 4:
        
        count=0

        # Highlight terrain block for mining/building...
        terrain.update(subject.position,camera)

    # Change subset position based on subject position.
    if abs(subject.x-pX)>1 or abs(subject.z-pZ)>1:
        pX=subject.x
        pZ=subject.z 
        terrain.swirlEngine.reset(pX,pZ)
        # Sound :)
        if subject.y > 4:
            if snow_audio.playing==False:
                snow_audio.pitch=random()+0.25
                snow_audio.play()
        elif grass_audio.playing==False:
            grass_audio.pitch=random()+0.7
            grass_audio.play()

    blockFound=False
    step = 2
    height = 1.86
    x = str(floor(subject.x+0.5))
    z = str(floor(subject.z+0.5))
    y = floor(subject.y+0.5)
    for i in range(-step,step):
        if terrain.td.get("x"+x+"y"+str(y+i)+"z"+z)=="t":
            target = y+i+height
            blockFound=True
            break
    if blockFound==True:
        # Step up or down :>
        subject.y = lerp(subject.y, target, 6 * time.dt)
    else:
        # Gravity fall :<
        subject.y -= 9.8 * time.dt

terrain.genTerrain()

app.run()