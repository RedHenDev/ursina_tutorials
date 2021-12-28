from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrain import MeshTerrain
from random import random
from snowflake import Snowflake

app = Ursina()

window.color = color.rgb(0,200,255)
indra = Sky()
indra.color = window.color
subject = FirstPersonController()
subject.gravity = 0.0
subject.cursor.visible=False
window.fullscreen=False
scene.fog_color = color.white
scene.fog_density = 0.04

# ***
flakes=[]
for i in range(1024):
    e = Snowflake()
    flakes.append(e)

terrain = MeshTerrain() 

pX = subject.x
pZ = subject.z
# ***
grassVox = Audio('step.ogg',autoplay=False,loop=False)
snowVox = Audio('snowStep.mp3',autoplay=False,loop=False)

def input(key):
    terrain.input(key)

count = 0
def update():
    global count, pX, pZ

    count+=1
    if count == 4:
        
        count=0

        #***
        # Let it snow!
        for i in range(1024):
            flakes[i].update()

        # Generate terrain at current swirl position.
        terrain.genTerrain()

        # Highlight terrain block for mining/building...
        terrain.update(subject.position,camera)

    # Change subset position based on subject position.
    if abs(subject.x-pX)>1 or abs(subject.z-pZ)>1:
        pX=subject.x
        pZ=subject.z 
        terrain.swirlEngine.reset(pX,pZ)
        
        # ***
        # terrain.td.get("x"+x+"y"+str(y+i)+"z"+z)
        if subject.y > 4:
            if not snowVox.playing:
                snowVox.pitch=random()+0.5-0.25
                snowVox.play()
        elif not grassVox.playing:
                grassVox.pitch=random()+0.7
                grassVox.play()
        
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