from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrain import MeshTerrain

app = Ursina()

window.color = color.rgb(0,200,255)
indra = Sky()
indra.color = window.color
subject = FirstPersonController()
subject.gravity = 0.0

terrain = MeshTerrain() 

def update():
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

    # updateTerrain()

terrain.genTerrain()

app.run()