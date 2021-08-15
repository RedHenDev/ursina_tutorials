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
            'x9z9': -9,
            'x10z9': -9,
            'x11z9': -9,
            'x9z10': -9,
            'x9z11': -9}

    def checkCave(this, _x, _z):
        tempStr = this.caveDic.get( 'x'+str(int(_x))+
                                    'z'+str(int(_z)))
        return tempStr 

    def makeCave(this, _x, _z, _height):
        tempStr = ( 'x'+str(int(_x))+
                    'z'+str(int(_z)))
        this.caveDic[tempStr] = _height
    

