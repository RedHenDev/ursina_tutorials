from ursina import *

# inventory=Panel()
inventory=Entity(model='quad',parent=camera.ui)
inventory.color=color.dark_gray
inventory.scale=0.1
inventory.scale_x*=9
inventory.origin=(0,4.5)

hLighter=Entity(model='quad',parent=camera.ui)
hLighter.color=color.black
hLighter.scale=0.088
hLighter.origin=(4.5,5.1)

# g = Draggable(model='block.obj')

minerals =  {   'grass' : (8,7),
                'soil' : (10,7),
                'stone' : (8,5),
                'ice' : (9,7),
                'snow' : (8,6),
            }
# Create iterable list from dictionary keys (not values).
mins = list(minerals.keys())

class iceCube(Entity):
    def __init__(this,blockType='grass'):
        super().__init__()
        this.model='block.obj'
        this.parent=camera.ui
        this.blockType=blockType

        this.color=color.white
        this.scale=0.08
        this.origin=(5.6,6.1)
        this.texture='texture_atlas_3.png'
        this.texture_scale*=(64/this.texture.width) 
            
        this.setup_texture()

    def setup_texture(this):
        uu=minerals[this.blockType][0]
        uv=minerals[this.blockType][1]
        this.model.uvs = [Vec2(uu,uv) + u for u in this.model.uvs]
        this.model.generate()

gs = []
for i in range(10):
    e = iceCube(mins[i%len(mins)])
    e.origin_x = 4.95 + (1.1 * -i)

def inventory_input(key,mouse,subject):
    if key=='e' and not subject.enabled:
        subject.enable()
        mouse.locked=True
    elif key=='e' and subject.enabled:
        subject.disable()
        mouse.locked=False
    
    if key=='r': 
        hLighter.origin_x-=1
        if hLighter.origin_x<-4.5:
            hLighter.origin_x=4.5
        subject.blockTnum=(subject.blockTnum+1)%len(mins)