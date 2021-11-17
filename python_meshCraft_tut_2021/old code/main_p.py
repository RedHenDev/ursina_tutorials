from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrain import MeshTerrain

app = Ursina()

window.color = color.rgb(0,200,255)
heaven = Sky()
heaven.color = window.color
subject = FirstPersonController()
subject.gravity = 0.0

terrain = MeshTerrain() 

def update():
    foundBlock = False
    step = 3
    stepSpeed = 6
    height = 1.8
    x = floor(subject.x + 0.5)
    z = floor(subject.z + 0.5)
    y = floor(subject.y)
    for i in range(-step,step):
        if terrain.td.get(  'x'+str(x)+
                            'y'+str(y+i)+
                            'z'+str(z)) \
                    =='t':
                    foundBlock = True
                    target = y+i+height
                    break
    if foundBlock==False:
        subject.y -= 9.8 * time.dt
    else:
        subject.y = lerp(subject.y,target,stepSpeed*time.dt)

    # updateTerrain()

terrain.genTerrain()

app.run()