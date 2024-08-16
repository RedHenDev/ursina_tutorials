
from ursina import *
import random as ra
from config import mins,minerals
import numpy as np

hotspots=[]
items=[]

import sys
window.fullscreen=False
if window.fullscreen==False and sys.platform.lower()=='darwin':
    #***
    pass
    # camera.ui.scale_x*=0.05*1/window.aspect_ratio
    # camera.ui.scale_y*=0.05

# Inventory hotbar.
hotbar = Entity(model='quad',parent=camera.ui)
# Set the size and position.
# hotbar.scale_y=0.08
# hotbar.scale_x=0.68
hot_cols=9
hot_wid=1/16 # Width of hotspot is 1 tenth of window height.
hb_wid=hot_wid*hot_cols # Hotbar width no. of cols times this.
hotbar.scale=Vec3(hb_wid,hot_wid,0)
# ui_cols=hotbar.scale[0]/9
hotbar.y=(-0.45 + (hotbar.scale_y*0.5))

# hotbar.y=-0.45 + (hotbar.scale_y*0.5)
# Appearance.
hotbar.color=color.dark_gray
# hotbar.render_queue=0
hotbar.z=0

# Inventory main panel.
iPan = Entity(model='quad',parent=camera.ui)
# Set the size and position.
iPan.rows=3
iPan.scale_y=hotbar.scale_y * iPan.rows
iPan.scale_x=hotbar.scale_x
iPan.basePosY=hotbar.y+(hotbar.scale_y*0.5)+(iPan.scale_y*0.5)
iPan.gap=hotbar.scale_y
iPan.y=iPan.basePosY+iPan.gap
# Appearance.
iPan.color=color.light_gray
# iPan.render_queue=0
iPan.z=0
iPan.visible=False

class Hotspot(Entity):
    # Fix size of hospot to height of hotbar.
    scalar=hotbar.scale_y*0.9
    # How many hotspots to fit across hotbar?
    rowFit=9
    def __init__(this):
        super().__init__()
        this.model=load_model('quad',use_deepcopy=True)
        this.parent=camera.ui
        this.scale_y=Hotspot.scalar
        this.scale_x=this.scale_y
        this.color=color.white
        this.texture='white_box'
        # this.render_queue=1
        this.z=-1

        this.onHotbar=False
        this.visible=False
        this.occupied=False
        # What item are we hosting?
        this.item=None
        # New stack system :)
        # Start with no items as default.
        this.stack=0
        # Text for number of blocks in stack.
        this.t = Text("",scale=1.5)
    
    @staticmethod
    def toggle():
        if iPan.visible:
            iPan.visible=False
        else:
            iPan.visible=True
        # Toggle non-hotbar hotspots and their items.   
        for h in hotspots:
            # Gameplay mode? I.e. not visible?
            if not h.visible and not h.onHotbar:
                # Inventory mode.
                h.visible=True
                h.t.visible=True
                if h.item:
                    h.item.visible=True
                    # Enable item?
            elif not h.onHotbar:
                # Gameplay mode.
                h.visible=False
                h.t.visible=False
                if h.item:
                    h.item.visible=False
                    # Disable item?


class Item(Draggable):
    def __init__(this,_blockType):
        super().__init__()
        # *** for ursina update fix
        this.model=load_model('quad',use_deepcopy=True)
        this.scale_x=Hotspot.scalar*0.9
        this.scale_y=this.scale_x
        this.color=color.white
        this.texture='texture_atlas_3.png'
        this.texture_scale*=64/this.texture.width
        # this.render_queue=2
        this.z=-2

        # Pick a random block type.
        if _blockType==None:
            this.blockType=mins[ra.randint(0,len(mins)-1)]
        else:
            this.blockType=_blockType

        this.onHotbar=False
        this.visible=False
        this.currentSpot=None

        this.set_texture()
        this.set_colour()
    
    def set_texture(this):
        # Use dictionary to access uv co-ords.
        uu=minerals[this.blockType][0]
        uv=minerals[this.blockType][1]
        # *** - for ursina update fix
        basemod=load_model('block.obj',use_deepcopy=True)
        e=Empty(model=basemod)
        cb=copy(e.model.uvs)
        #del cb[:-33]
        cb = cb[-6:] #get last 6 uvs
        cb = cb[3:] + cb[:3] #reverse order
        this.model.uvs = [Vec2(uu,uv) + u for u in cb]
        this.model.generate()
        this.rotation_z=180

    def set_colour(this):
        # Do we have a color element on the tuple?
        if len(minerals[this.blockType]) > 2:
            # Yes! Set color :)
            this.color=minerals[this.blockType][2]
    
    def fixPos(this):
        # Look through all the hotspots.
        # Find the unoccupied hotspot that is closest.
        # If found, copy that hotspot's position.
        # Set previous hotspot host to unoccupied.
        # Download item's blocktype info etc. into
        # host hotspot -- so that subject can use item.
        # !?! Can't find an available hotspot?
        # Return to current host position.

        closest=-1
        closestHotty=None
        for h in hotspots:
            if h.occupied and h.item!=this: continue
            # Found a unoccupied hotspot :)
            # How close is it?
            dist=h.position-this.position
            # Find the magnitude - i.e. distance.
            dist=np.linalg.norm(dist)
            if dist < closest or closest == -1:
                # We have a new closest!
                closestHotty=h
                # Always remember to set current record!
                closest=dist
        # Finished iterating over hotspots.
        if closestHotty is not None:
            # We've found an available closest :)
            this.position=closestHotty.position
            # Update new host's information about item.
            closestHotty.occupied=True
            closestHotty.item=this
            closestHotty.stack=this.currentSpot.stack
            # Update previous host-spot's status.
            
            if this.currentSpot!=closestHotty:
                this.currentSpot.stack=0
                this.currentSpot.t.text = "     "
                this.currentSpot.occupied=False
                this.currentSpot.item=None
                # Finally, update current host spot.
                this.currentSpot=closestHotty
        elif this.currentSpot:
            # No hotspot available? Just move back.
            this.position=this.currentSpot.position

    def update_stack_text(this):
        # Display how many blocks in this hotspot's stack.
        stackNum = this.currentSpot.stack
        myText="<white><bold>"+str(stackNum)
        this.currentSpot.t.text = myText
        this.currentSpot.t.origin=(0,0)
        this.currentSpot.t.z=-3
        this.currentSpot.t.x=this.currentSpot.x
        this.currentSpot.t.y=this.currentSpot.y

    def drop(this):
        this.fixPos()
        this.update_stack_text()

    @staticmethod
    def stack_check(_blockType):
        for h in hotspots:
            if h.onHotbar==False: continue
            if h.occupied==False: continue
            # OK -- found an occupied hotbar hotspot.
            if h.item.blockType==_blockType:
                h.stack+=1
                # Also update the text on stack.
                h.item.update_stack_text()
                return True
        # No matching stacks.
        return False

    @staticmethod
    def new_item(_blockType):
        # First, check whether there is already
        # a stack of this blockType on the hotbar.
        # If yes, increment hotspot's stack.
        # If no, and space available on hotbar,
        # create a new stack of 1 of that item -
        # which means, creating a new Item.
        aStack = Item.stack_check(_blockType)
        if aStack==False:
            # Space available on hotbar?
            for h in hotspots:
                if not h.onHotbar or h.occupied: continue
                else:
                    # Creating a new stack :)
                    # On hotbar.
                    h.stack=1
                    b=Item(_blockType)
                    b.currentSpot=h
                    items.append(b)
                    # Refactor this later!
                    # Dedicated function please :)
                    h.item=b
                    h.occupied=True
                    b.onHotbar=True
                    b.visible=True
                    b.x = h.x
                    b.y = h.y
                    b.update_stack_text()
                    break
                    

# Hotspots for the hotbar.
for i in range(Hotspot.rowFit):
    bud=Hotspot()
    bud.onHotbar=True
    bud.visible=True
    bud.y=hotbar.y
    # padding=(hotbar.scale_x-bud.scale_x*Hotspot.rowFit)*0.5
    bud.x=  (   hotbar.x-hotbar.scale_x*0.5 +
                Hotspot.scalar*0.5 * 1.2 + 
                i*bud.scale_x * 1.1
            )
    hotspots.append(bud)

# Hotspots for the main inventory panel.
for i in range(Hotspot.rowFit):
    for j in range(iPan.rows):
        bud=Hotspot()
        bud.onHotbar=False
        bud.visible=False
        # Position.
        # padding_x=(iPan.scale_x-Hotspot.scalar*Hotspot.rowFit)*0.5
        # padding_y=(iPan.scale_y-Hotspot.scalar*iPan.rows)*0.5
        bud.y=  (   iPan.y+iPan.scale_y*0.5 -
                    Hotspot.scalar*0.5 * 1.2 -
                    Hotspot.scalar * j * 1.1
                )
        bud.x=  (   iPan.x-iPan.scale_x*0.5 +
                    Hotspot.scalar*0.5 * 1.2 +
                    i*Hotspot.scalar * 1.1
                )
        hotspots.append(bud)
# Main inventory panel items. 
# for i in range(8):
#     bud=Item()
#     bud.onHotbar=True
#     bud.visible=True
#     bud.x=ra.random()-0.5
#     bud.y=ra.random()-0.5
#     bud.fixPos()
#     items.append(bud)

# Make sure non-hotbar items are toggled off (invisible).
# Call this twice so that main inventory panel is
# invisible at the start, but that items inherit their
# non-hotbar status.
Hotspot.toggle()
Hotspot.toggle()    

# Where am I?
wai=Text(   '<black><bold>Nowhere',
            scale=2.4,position=(-.8,.5))


def inv_input(key,subject,mouse):
    # Since we may have moved, update location text.
    wai.text=f'<black><bold>east:{floor(subject.x)}, north:{floor(subject.z)}'
    try:
        wnum = int(key)
        if wnum > 0 and wnum < 10:
            # Make sure no hotspots are highlighted.
            for h in hotspots:
                h.color=color.white
            # Adjust wnum to list indexing (1=0).
            wnum-=1
            hotspots[wnum].color=color.black
            # Is this hotspot occupied with an item?
            if hotspots[wnum].occupied:
                # Set subject's new blocktype from this item.
                subject.blockType=hotspots[wnum].item.blockType
                
    except:
        pass
    # Pause and unpause, ready for inventory.
    if key=='e' and subject.enabled:
        # Inventory mode.
        Hotspot.toggle()
        subject.disable()
        mouse.locked=False
    elif key=='e' and not subject.enabled:
        # Gameplay mode.
        Hotspot.toggle()
        subject.enable()
        mouse.locked=True