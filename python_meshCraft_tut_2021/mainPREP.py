from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrainPREP import MeshTerrain
from flake import SnowFall
import random as ra
import bumpPrep
# ***
from PREP_saveload import load_world, save_world

app = Ursina()

window.color = color.rgb(0,200,255)

indra = Sky()
indra.color = window.color
subject = FirstPersonController()
subject.gravity = 0.0
subject.cursor.visible=True
subject.cursor.color=color.white
# ***
subject.ump=False
window.fullscreen=False
# window.show_ursina_splash=True
# ***
camera.clip_plane_far=100
indra.scale*=0.01
camDash=10

terrain = MeshTerrain()
# snowfall = SnowFall(subject)
generatingTerrain=True

for i in range(256):
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
    if key=='space':
        subject.ump=True

    # ***
    if key=='b':
        save_world(terrain,subject)
    if key=='n':
        load_world(terrain,subject)

count = 0
def update():
    global count, pX, pZ

    # *** Camera dash effect. FOV default is 90.
    if held_keys['shift'] and held_keys['w']:
        subject.speed=12
        if camera.fov<100:
            camera.fov+=camDash*time.dt
    else: 
        subject.speed=6
        if camera.fov>90:
            camera.fov-=camDash*4*time.dt
            if camera.fov<90:camera.fov=90

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

    mob_move(guy,subject.position,terrain.td)

    bumpPrep.bumpWall(subject,terrain)
    
# Mobs deserve their own module :)
from mob_systemPREP import *

app.run()