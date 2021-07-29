from ursina import *
from combine_350 import combine_350
from combine_360 import combine_360

app = Ursina()

ghost=Entity(texture='33HU.gif',eternal=True,position=(0,0,0))
amlands=[]

def setup():
    global amlands
    amlands=[]  # Clear out our list.
    for i in range(12):
        petter=Entity(  model='cube',
                        color=color.rgb(0,i*7,i*7),
                        scale_x=0.9,
                        x=i-5.5)
        amlands.append(petter)
        amlands[-1].parent=scene

def moveup():
    global amlands
    for a in amlands:
        a.parent=scene
        a.y+=1

def reset():
    global ghost
    scene.clear()
    ghost.model=None
    setup()

def input(key):
    if key=='5':
        for a in amlands:
            a.parent=ghost
        combine_350(ghost,auto_destroy=False)
        # moveup()
    elif key=='6':
        for a in amlands:
            a.parent=ghost
        combine_360(ghost,auto_destroy=False)
        # moveup()
    elif key=='r' or key=='space':
        reset()
    elif key=='w': moveup()
    elif key=='s': ghost.y -= 1
    elif key=='escape':
        exit()

setup()

app.run()