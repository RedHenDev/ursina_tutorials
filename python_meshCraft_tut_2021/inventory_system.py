
from urllib.request import build_opener
from ursina import *
import random as ra
from config import mins,minerals


# Inventory hotbar.
hotbar = Entity(model='quad',parent=camera.ui)
# Set the size and position.
hotbar.scale_y=0.08
hotbar.scale_x=0.68
hotbar.y=-0.45 + (hotbar.scale_y*0.5)
# Appearance.
hotbar.color=color.dark_gray

class Hotspot(Entity):
    # Fix size of hospot to height of hotbar.
    scalar=hotbar.scale_y*0.9
    # How many hotspots to fit across hotbar?
    rowFit=9
    def __init__(this):
        super().__init__()
        this.model='quad'
        this.parent=camera.ui
        this.scale_y=Hotspot.scalar
        this.scale_x=this.scale_y
        this.color=color.white
        this.texture='white_box'

        this.onHotbar=False
        this.visible=False
        this.occupied=False
        # Pick a random block type.
        this.blockType=mins[ra.randint(0,len(mins)-1)]

class Item(Draggable):
    def __init__(this):
        super().__init__()
        this.model='quad'
        this.scale_x=Hotspot.scalar*0.9
        this.scale_y=this.scale_x
        this.color=color.white
        this.texture='texture_atlas_3.png'
        this.texture_scale*=64/this.texture.width

        # Pick a random block type.
        this.blockType=mins[ra.randint(0,len(mins)-1)]

        this.onHotbar=False
        this.visible=False

        this.set_texture()
        this.set_colour()
    
    def set_texture(this):
        # Use dictionary to access uv co-ords.
        uu=minerals[this.blockType][0]
        uv=minerals[this.blockType][1]
        basemod=load_model('block.obj')
        cb=copy(basemod.uvs)
        del cb[:-33]
        this.model.uvs = [Vec2(uu,uv) + u for u in cb]
        this.model.generate()
        this.rotation_z=180

    def set_colour(this):
        # Do we have a color element on the tuple?
        if len(minerals[this.blockType]) > 2:
            # Yes! Set color :)
            this.color=minerals[this.blockType][2]
    
    def fixPos(this):
        pass

    def drop(this):
        this.fixPos()

hotspots=[]
items=[]

# Hotspots for the hotbar.
for i in range(Hotspot.rowFit):
    bud=Hotspot()
    bud.onHotbar=True
    bud.visible=True
    bud.y=hotbar.y
    padding=(hotbar.scale_x-bud.scale_x*Hotspot.rowFit)*0.5
    bud.x=  (   hotbar.x-hotbar.scale_x*0.5 +
                bud.scale_x*0.5 +
                padding +
                i*bud.scale_x
            )
    hotspots.append(bud)

for i in range(9):
    bud=Item()
    bud.onHotbar=True
    bud.visible=True
    bud.x=ra.random()-0.5
    bud.y=ra.random()-0.5
    items.append(bud)

def inv_input(key,subject,mouse):
    # Pause and unpause, ready for inventory.
    if key=='e' and subject.enabled:
        subject.disable()
        mouse.locked=False
    elif key=='e' and not subject.enabled:
        subject.enable()
        mouse.locked=True