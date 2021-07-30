""" Tutorial for a solar system using Ursina """

from ursina import *
#from ursina.prefabs.first_person_controller import FirstPersonController
import random as ra
import numpy as np

app = Ursina()

window.color = color.black # color.rgb(0,0,0)

# Our list of planets.
planets = []

def input(key):
    if key == 'escape' or key == 'q':
        quit()
    if key == 'space':
        sun.scale *= 2

def update():
    sun.rotation_y += 1
    sun.rotation_x += 1

    for p in planets:
        p.orbit()

# Our Planet class -- for making planets.
class Planet:
    def __init__(this):
        randS = ra.randint(3,24)
        this.name = 'default'
        this.orbitalTheta = ra.randint(0,360)
        this.orbitalVel = 0.01
        this.solarDist = 100
        this.ent = Entity(model='sphere',scale=randS,
                          color=color.gray,texture='assets/2k_moon')

    def orbit(this):
        this.ent.x = this.solarDist * np.cos(this.orbitalTheta)
        this.ent.z = this.solarDist * np.sin(this.orbitalTheta)
        this.orbitalTheta += this.orbitalVel

# The sun (centre of the solar system -> )
sun = Entity(model='sphere',
             texture='assets/texy',scale=64,
             position=Vec3(0,-32,32))


# Birth our planets in a loop. Add/append them to the planets[] list.
for p in range(9):
    baby = Planet()
    baby.solarDist = (p * 80) + 80
    baby.ent.y = -32
    planets.append(baby)

EditorCamera()
#jessie = Sky()
#jessie.texture = 'assets/spaceTex'

#subject = FirstPersonController()
app.run()











