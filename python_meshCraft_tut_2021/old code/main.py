from ursina import *

app = Ursina()

terrain = MeshTerrain()

def update():
    # terrain.paintTerrain()

terrain.paintTerrain()

app.run()