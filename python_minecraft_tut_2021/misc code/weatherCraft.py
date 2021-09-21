"""
Weather functions.
"""
from ursina import color, window, time
from nMap import nMap

class Weather:
    def __init__(this, rate=1):
        this.red = 0
        this.green = 200
        this.blue = 211

        this.darkling = 0

        this.rate = rate

        this.towardsNight = 1

    def setSky(this):
        r = nMap(this.darkling,0,100,0,this.red)
        g = nMap(this.darkling,0,100,0,this.green)
        b = nMap(this.darkling,0,100,0,this.blue)
        window.color = color.rgb(r,g,b)

    def update(this):
        this.darkling -= (  this.rate * 
                            this.towardsNight *
                            time.dt)
        if this.darkling < 0:
            this.towardsNight *= -1
            this.darkling = 0
        
        this.setSky()
