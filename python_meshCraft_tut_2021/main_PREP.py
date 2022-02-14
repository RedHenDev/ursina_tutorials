from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrain_PREP import MeshTerrain
from flake import SnowFall
import random as ra
from bump_system import *
from save_load_system import saveMap, loadMap

app = Ursina()

window.color = color.rgb(0,200,255)
indra = Sky()
indra.color = window.color
subject = FirstPersonController()
subject.gravity = 0.0
subject.cursor.visible=True
subject.cursor.color=color.white
subject.frog=False # For jumping...
subject.runSpeed=12
subject.walkSpeed=4
# ***
subject.y=100
camera.dash=10 # Rate at which fov changes when running.
window.fullscreen=False


terrain = MeshTerrain()
# ***
terrain.generatingTerrain=True
# snowfall = SnowFall(subject)
# *** 
# scene.fog_density=(0,50)
scene.fog_density=(3,50)
scene.fog_color=indra.color
camera.clip_plane_far=100
indra.scale*=1/camera.clip_plane_far

for i in range(32):
    terrain.genTerrain()

grass_audio = Audio('step.ogg',autoplay=False,loop=False)
snow_audio = Audio('snowStep.mp3',autoplay=False,loop=False)

pX = subject.x
pZ = subject.z

def input(key):
    terrain.input(key)
    if key=='g':
        terrain.generatingTerrain = not terrain.generatingTerrain
    # Jumping...
    if key=='space': subject.frog=True
    # Saving and loading...
    if key=='m': saveMap(subject.position,terrain.td)
    if key=='l': loadMap(subject,terrain)

count = 0
def update():
    global count, pX, pZ

    # Highlight terrain block for mining/building...
    terrain.update(subject.position,camera)

    # Handle mob ai.
    mob_movement(grey, subject.position, terrain.td)

    count+=1
    if count == 4:
        
        count=0
        # Generate terrain at current swirl position.
        if terrain.generatingTerrain:
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
    
    # Walk on solid terrain, and check wall collisions.
    bumpWall(subject,terrain)
    # Running and dash effect.
    if held_keys['shift'] and held_keys['w']:
        subject.speed=subject.runSpeed
        if camera.fov<100:
            camera.fov+=camera.dash*time.dt
    else:
        subject.speed=subject.walkSpeed
        if camera.fov>90:
            camera.fov-=camera.dash*4*time.dt
            if camera.fov<90:camera.fov=90

from mob_system import *

app.run()