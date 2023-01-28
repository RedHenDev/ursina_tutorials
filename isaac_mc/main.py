from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrain import MeshTerrain

app = Ursina()

window.color = color.rgb(200,0,255)
subject = FirstPersonController()
subject.gravity = 0.0

terrain = MeshTerrain()

def update():
    pass

terrain.genTerrain()

app.run()