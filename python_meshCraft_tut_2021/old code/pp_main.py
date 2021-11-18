from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrain import MeshTerrain

app = Ursina()

window.color = color.rgb(0,200,255)
indra = Sky()
indra.color=window.color
subject = FirstPersonController()
subject.gravity = 0.0

terrain = MeshTerrain() 

def update():
    step = 2
    height = 1.8
    foundBlock = False
    x = str(floor(subject.x+0.5))
    z = str(floor(subject.z+0.5))
    y = floor(subject.y+0.5)
    for i in range(-step,step):
        if terrain.td.get("x"+x+"y"+str(y+i)+"z"+z)=='t':
            foundBlock=True
            target = y+i+height
            break

    if foundBlock==False:
        # Gravity fall!
        subject.y -= 9.8 * time.dt
    else:
        # Step up or down :)
        subject.y = lerp(subject.y, target, 6 * time.dt)

    # updateTerrain()

terrain.genTerrain()

app.run()