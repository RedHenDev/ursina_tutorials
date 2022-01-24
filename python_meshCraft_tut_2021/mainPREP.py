from operator import truediv
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrainPREP import MeshTerrain
from flake import SnowFall
# *** to circumvent TypeError: 'module' object is not callable
# *** i.e. when mob_system module imported.
import random as ra
import bumpPrep

app = Ursina()

window.color = color.rgb(0,200,255)
indra = Sky()
indra.color = window.color
subject = FirstPersonController()
subject.gravity = 0.0
subject.cursor.visible=False
window.fullscreen=False
window.show_ursina_splash=True
camera.clip_plane_far=400

terrain = MeshTerrain()
# snowfall = SnowFall(subject)
generatingTerrain=True

for i in range(128):
    terrain.genTerrain()

grass_audio = Audio('step.ogg',autoplay=False,loop=False)
snow_audio = Audio('snowStep.mp3',autoplay=False,loop=False)

pX = subject.x
pZ = subject.z

# ***
def load_world():
    import pickle, sys, os
    global terrain

    # Open main module directory for correct file.
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(path)
    with open('test_map.mm', 'rb') as f:
        nd = pickle.load(f)

        # Empty out current terrain.
        for s in terrain.subsets:
            destroy(s)
        terrain.td={}
        terrain.vd={}
        terrain.subsets=[]
        terrain.setup_subsets()
        terrain.currentSubset=1
        terrain.td=copy(nd[1])
        # Iterate over terrain dictionary and
        # if we find 't' then generate a block.
        # Note this means we'll lose colour info etc.
        i = 0
        for key in terrain.td:
            if terrain.td.get(key)=='t':
                x = key[0]
                y = key[1]
                z = key[2]
                if i>=len(terrain.subsets)-1:
                    i=0
                terrain.genBlock(x,y,z,subset=i,gap=False,blockType='grass')
                i+=1

        # Reset swirl engine.
        terrain.swirlEngine.reset(  subject.position.x,
                                    subject.position.z)
        for s in terrain.subsets:
            s.model.generate()
        # And reposition subject according to saved map.
        subject.position=copy(nd[0])

def save_world():
    import pickle, sys, os

    # Open main module directory for correct file.
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(path)
    with open('test_map2.mm', 'wb') as f:
        
        new_data=[subject.position,terrain.td]

        pickle.dump(new_data, f)
        new_data.clear()

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
    # ***
    if key=='b':
        save_world()
    if key=='n':
        load_world()

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

    # ***
    bumpPrep.bumpWall(subject,terrain)
    
# ***
# Mobs deserve their own module :)
from mob_systemPREP import *

app.run()