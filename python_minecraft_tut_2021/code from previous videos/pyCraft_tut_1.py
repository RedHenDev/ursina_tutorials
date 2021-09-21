"""
Minecraft in Python tut 1
"""

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor
from perlin_noise import PerlinNoise  

app = Ursina()

window.color = color.rgb(0,200,211)
window.exit_button.visible = False

scene.fog_color = color.rgb(255,0,0)
scene.fog_density = 0.04

grassStrokeTex = load_texture('grass_14.png')

def input(key):
    if key == 'q' or key == 'escape':
        quit()

def update():
    pass

terrain = Entity(model=None,collider=None)
noise = PerlinNoise(octaves=2,seed=2021)
amp = 6
freq = 24

terrainWidth = 32
for i in range(terrainWidth*terrainWidth):
    bud = Entity(model='cube',color=color.green)
    bud.x = floor(i/terrainWidth)
    bud.z = floor(i%terrainWidth)
    bud.y = floor((noise([bud.x/freq,bud.z/freq]))*amp)
    bud.parent = terrain

terrain.combine()
terrain.collider = 'mesh'
terrain.texture = grassStrokeTex

subject = FirstPersonController()
subject.cursor.visible = False
subject.gravity = 0.5
subject.x = subject.z = 5
subject.y = 12

app.run()