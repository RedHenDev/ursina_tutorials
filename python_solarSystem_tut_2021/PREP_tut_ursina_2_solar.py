""" Tutorial for a solar system using Ursina """

""" Currently this is prep and experimental for tut 3 """

from ursina import *
#from ursina.prefabs.first_person_controller import FirstPersonController
import random as ra


app = Ursina()

def input(key):
    if key == 'escape' or key == 'q':
        quit()
    if key == 'space':
        sun.scale *= 2

def update():
    sun.rotation_y += 1
    sun.rotation_x += 1

class Planet:
    def __init__(this):
        randS = ra.randint(3,24)
        r = ra.randint(100,255)
        g = ra.randint(100,255)
        b = ra.randint(100,255)
        a = ra.randint(164,255)
        this.ent = Entity(model='sphere',scale=randS,color=color.rgba(r,g,b,a),texture='assets/2k_moon')

sun = Entity(model='sphere',texture='assets/texy',scale=64)

# Our list of planets.
planets = []

for p in range(100):
    baby = Planet()
    baby.ent.x = (p - 50) * 20
    baby.ent.z = -80
    planets.append(baby)

EditorCamera()

#subject = FirstPersonController()
app.run()











