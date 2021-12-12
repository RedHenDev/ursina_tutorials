from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from pd_mesh_terrain import MeshTerrain

app = Ursina()

window.color = color.rgb(0,200,255)
indra = Sky()
indra.color = window.color
subject = FirstPersonController()
subject.gravity = 0.0
subject.cursor.visible=False
window.fullscreen=False

terrain = MeshTerrain() 

pX = subject.x
pZ = subject.z

def input(key):
    terrain.input(key)

count = 0
def update():
    global count, pX, pZ

    count+=1
    if count == 2:
        
        count=0
        # Generate terrain at current swirl position.
        terrain.genTerrain()
        # Highlight terrain block for mining/building...
        terrain.update(subject.position,camera)

    # Change subset position based on subject position.
    if abs(subject.x-pX)>6 or abs(subject.z-pZ)>6:
        pX=subject.x
        pZ=subject.z 
        terrain.swirlEngine.reset(pX,pZ)

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