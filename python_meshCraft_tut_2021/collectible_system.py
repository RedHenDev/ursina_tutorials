"""
Hello. This is our system for mined blocks
dropping collectable materials.
"""

# Collectible dictionary. Similar to td{}.
# It will store terrain position of a collectible :)
from ursina import Entity, Vec2, load_model, math
from config import minerals

# Our list of collectibles.
collectibles = []
# Dictionary to record where subject can pick up items.
cd={}

def drop_collectible(_blockType,_pos,_tex):
    c=Entity(   model=load_model('block.obj',use_deepcopy=True),
                texture=_tex)
    c.scale=0.33
    c.position=_pos
    cd[c.position]=_blockType
    print(cd.get(c.position))
    # Central position of mining site.
    c.y+=0.5-(c.scale_y*0.5)
    # Orig pos needed for sine bounce!
    c.original_y=c.y
    # Wrap texture from texture atlas.
    c.texture_scale*=64/c.texture.width
    # UV information for texture wrap.
    uu=minerals.get(_blockType)[0]
    uv=minerals.get(_blockType)[1]
    c.model.uvs=([Vec2(uu,uv) + u for u in c.model.uvs])
    c.model.generate()
    collectibles.append(c)

def collectible_bounce():
    for c in collectibles:
        c.rotation_y+=2
        # Add a little bounce ;)
        c.y = ( c.original_y + 
                math.sin(c.rotation_y/50)*c.scale_y)