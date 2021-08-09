"""
Our cave system :)
Used by genPerlin() function.
"""

class Caves:
    def __init__(this):
        this.caveDic = {}
        this.buildCaves()

    def buildCaves(this):
        # Dictionary of cave 'gaps'
        this.caveDic = { 
            'x9z9':'cave',
            'x10z9':'cave',
            'x11z9':'cave',
            'x9z10':'cave',
            'x9z11':'cave'}

    def checkCave(this, _x, _z):
        tempStr = this.caveDic.get( 'x'+str(int(_x))+
                                    'z'+str(int(_z)))
        if tempStr=='cave':
            return True
        else: return False 
    

