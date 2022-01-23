from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrainPREP import MeshTerrain
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
generatingTerrain=False

for i in range(1):
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

        for s in terrain.subsets:
            destroy(s)
        subject.position=copy(nd[0])
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
        whatSub=0
        chunkSize=terrain.subWidth*terrain.subWidth
        for key in terrain.td:
            i+=1
            if terrain.td.get(key)=='t':
                x = key[0]
                y = key[1]
                z = key[2]
                # print(str(key)+'-->'+terrain.td.get(key))
                # if whatSub>63:
                #     whatSub=1
                if i>=len(terrain.subsets)-1:
                    print(len(terrain.subsets))
                    i=0
                terrain.genBlock(x,y,z,subset=i,gap=False,blockType='grass')
                    # print(whatSub)
        # Reset swirl engine.
        terrain.swirlEngine.reset(  subject.position.x,
                                    subject.position.z)
        for s in terrain.subsets:
            s.model.generate()

        # # Populate our familiar terrain variables
        # # with data from the saved file.
        # subject.position = copy(nd[0])
        # terrain.td = copy(nd[1])
        # terrain.vd = copy(nd[2])
        # tm = copy(nd[3])

        # """
        # # Alter vertex dictionary to single model...
        # # OK this doesn't work -- must be a mistake in here.
        # # tot=0
        # # for key in terrain.vd:
        # #     if terrain.vd[key] is not None:
        # #         terrain.vd[key][0]=0
        # #         terrain.vd[key][1]=tot+terrain.vd.get(key)[1]
        # #         tot += terrain.vd.get(key)[1]
        # #         print('assigned'+str(terrain.vd.get(key)))
        # """

        # # Build single mesh from saved data.
        # world = Entity(model=Mesh(
        #                     vertices=tm[0],
        #                     triangles=tm[1],
        #                     colors=tm[2],
        #                     uvs=tm[3]))
        # world.texture='texture_atlas_3.png'
        # world.texture_scale*=64/world.texture.width
        
        # terrain.subsets[0].model=copy(world.model)
        # terrain.swirlEngine.reset(0,0)
        # terrain.currentSubset=0

def save_world():
    import pickle, sys, os

    # Open main module directory for correct file.
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(path)
    with open('test_map.mm', 'wb') as f:
        
        # e=Entity()
        # e.model=Mesh()
        # for s in terrain.subsets:
        #     for v in s.model.vertices:
        #         e.model.vertices.append(v)
        #     for t in s.model.triangles:
        #         e.model.triangles.append(t)
        #     for c in s.model.colors:
        #         e.model.colors.append(c)
        #     for u in s.model.uvs:
        #         e.model.uvs.append(u)
        # # e.combine(auto_destroy=False)

        # terrain_model = [   e.model.vertices,
        #                     e.model.triangles,
        #                     e.model.colors,
        #                     e.model.uvs]
        # destroy(e)

        # new_data = [subject.position,
        #             terrain.td,
        #             terrain.vd,
        #             terrain_model]
        
        # OK, let's just try saving the terrain dictionary.
        # When loading, therefore, terrain must be
        # regenerated in order especially to repopulate
        # the vertex dictionary.
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
# load_world()
# Mobs deserve their own module :)
# ***
from mob_system import *

app.run()