""" Tutorial for a solar system using Ursina """

from ursina import *

app = Ursina()

def input(key):
    if key == 'escape' or key == 'q':
        quit()
    if key == 'space':
        simon.scale *= 2

def update():
    simon.rotation_y += 1
    simon.rotation_x += 1

simon = Entity(model='cube',texture='texy')

EditorCamera()
app.run()

