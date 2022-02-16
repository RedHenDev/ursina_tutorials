from ursina import *

# inventory=Panel()
inventory=Entity(model='quad',parent=camera.ui)
inventory.color=color.dark_gray
inventory.scale=0.1
inventory.scale_x*=9
inventory.origin=(0,4.5)

# g = Draggable(model='block.obj',parent=camera.ui)
# g = Entity(model='block.obj',parent=camera.ui)

# g.color=color.light_gray
# g.scale=0.08
# g.origin=(5.6,6.1)
# g.texture='texture_atlas_3.png'
# g.texture_scale*=(64/g.texture.width)
# uu=8
# uv=7
# g.model.uvs = [Vec2(uu,uv) + u for u in g.model.uvs]
# g.model.generate()

class iceCube(Entity):
    def __init__(this,blockType='grass'):
        super().__init__()
        this.model='block.obj'
        this.parent=camera.ui

        this.color=color.light_gray
        this.scale=0.08
        this.origin=(5.6,6.1)
        this.texture='texture_atlas_3.png'
        this.texture_scale*=(64/this.texture.width)
        # Grass.
        uu = 8
        uv = 7
        if blockType=='soil':
            uu = 10
            uv = 7
        elif blockType=='stone':
            uu = 8
            uv = 5
        elif blockType=='ice':
            uu = 9
            uv = 7
        elif blockType=='snow':
            uu = 8
            uv = 6
        
        this.uu=uu
        this.uv=uv 
            
        this.setup_texture(uu,uv)

    def setup_texture(this,_uu=8,_uv=7):
        this.model.uvs = [Vec2(_uu,_uv) + u for u in this.model.uvs]
        this.model.generate()

minerals =  {   'grass' : (8,7),
                'soil' : (10,7),
                'stone' : (8,5),
                'ice' : (9,7),
                'snow' : (8,6),
            }
gs = []
# Create iterable list from dictionary keys (not values).
mins = list(minerals.keys())
for i in range(1,11):
    e = iceCube(mins[i%len(mins)])
    e.origin_x = 6.05 + (1.1 * -i)

def inventory_input(key,mouse,subject):
    if key=='e' and not subject.enabled:
        subject.enable()
        mouse.locked=True
    elif key=='e' and subject.enabled:
        subject.disable()
        mouse.locked=False