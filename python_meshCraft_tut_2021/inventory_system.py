
from ursina import *

# Inventory hotbar.
hotbar = Entity(model='quad',parent=camera.ui)
# Set the size and position.
hotbar.scale_y=0.08
hotbar.scale_x=0.8
hotbar.y=-0.5 + (hotbar.scale_y*0.5)
# Appearance.
hotbar.color=color.dark_gray

def inv_input(key,subject,mouse):
    # Pause and unpause, ready for inventory.
    if key=='e' and subject.enabled:
        subject.disable()
        mouse.locked=False
    elif key=='e' and not subject.enabled:
        subject.enable()
        mouse.locked=True