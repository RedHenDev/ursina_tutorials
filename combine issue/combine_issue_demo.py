from ursina import *
from combine_350 import combine_350
from combine_360 import combine_360
from math import floor
from random import random

app = Ursina()

subsets=[]
subset=Entity(texture='block_texture')
subsets.append(subset)
cubes=[]
currentSubset=0
for i in range(36):
    petter=Entity(  model='block',
                    color=color.rgb(0,i*7,i*7),
                    scale_x=0.9,
                    scale_z=0.9,
                    y=random()-2.5,
                    x=floor(i/6-3),
                    z=floor(i%6-3),
                    parent=subsets[currentSubset])
    cubes.append(petter)

def moveup():
    for a in cubes:
        a.y+=1

def input(key):
    global currentSubset
    if key=='5':
        for a in cubes:
            a.parent=subsets[currentSubset]
        combine_350(subsets[currentSubset],auto_destroy=False)
        e=Entity(texture='block_texture')
        subsets.append(e)
        currentSubset+=1
        moveup()
    elif key=='6':
        for a in cubes:
            a.parent=subsets[currentSubset]
        combine_360(subsets[currentSubset],auto_destroy=False)
        e=Entity(texture='block_texture')
        subsets.append(e)
        currentSubset+=1
        moveup()
    elif key=='w': moveup()
    elif key=='d': subsets[-2].x += 1
    elif key=='a': subsets[-2].x -= 1
    elif key=='escape':
        exit()

EditorCamera()

app.run()