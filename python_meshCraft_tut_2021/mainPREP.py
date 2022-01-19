from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrainPREP import MeshTerrain
from flake import SnowFall
from random import random

app = Ursina()

window.color = color.rgb(0,200,255)
indra = Sky()
indra.color = window.color
subject = FirstPersonController()
subject.gravity = 0.0
# subject.cursor.visible=False
window.fullscreen=False
# ***
scene.fog_density=0.02
scene.fog_color=color.rgb(0,255,255)
# ***
indra.scale*=0.01
# camera.clip_plane_far=400

terrain = MeshTerrain(subject,camera)
# snowfall = SnowFall(subject)
# ***
generating=True

for i in range(128):
    terrain.genTerrain()

grass_audio = Audio('step.ogg',autoplay=False,loop=False)
snow_audio = Audio('snowStep.mp3',autoplay=False,loop=False)

pX = subject.x
pZ = subject.z
# ***
# pRot = subject.rotation_y

def input(key):
    global generating
    terrain.input(key)
    if key=='g':
        generating = not generating

count = 0
def update():
    global count, pX, pZ, pRot

    # ***
    # Highlight terrain block for mining/building...
    terrain.update(subject.position,camera)

    # ***
    if generating:
        count+=1
        if count == 4:
            # Generate terrain at current swirl position.
            for i in range(4):
                terrain.genTerrain()
            count=0
    
    # ***
    # Reset origin for terrain gen when subject rotates...
    # if abs(subject.rotation_y-pRot)>1:
    #     ppX = floor(pX + 64 * math.sin(math.radians(subject.rotation_y)))
    #     ppZ = floor(pZ + 64 * math.cos(math.radians(subject.rotation_y)))
    #     # Now project ahead...
    #     terrain.swirlEngine.reset(ppX,ppZ)
    #     pRot = subject.rotation_y

    # Change subset position based on subject position.
    if abs(subject.x-pX)>1 or abs(subject.z-pZ)>1:
        pX=subject.x
        pZ=subject.z 
        # *** 
        terrain.swirlEngine.reset(pX,pZ)
        # Make sure immediate surrounding area catered for..
        # terrain.swirlEngine.reset(subject.x,subject.z)
        # terrain.genTerrain()
        # Now project ahead...
        # ppX = floor(pX + 64 * math.sin(math.radians(subject.rotation_y)))
        # ppZ = floor(pZ + 64 * math.cos(math.radians(subject.rotation_y)))
        # terrain.swirlEngine.reset(ppX,ppZ)
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

# terrain.genTerrain()

app.run()