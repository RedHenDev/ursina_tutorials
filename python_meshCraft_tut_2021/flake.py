"""
Snowflake module :)
Merry Christmas!
"""
from ursina import Entity, Vec3, time
from random import random

class Flake(Entity):
    def __init__(this,orig):
        super().__init__(   
            model='quad',
            texture='flake_1.png',
            position=orig,
            double_sided=True,
            scale=0.2
            )
        this.x+=random()*40-20
        this.z+=random()*40-20
        this.y+=random()*10+5

        minSpeed=1
        this.fallSpeed=random()*4+minSpeed
        minSpin=100
        this.spinSpeed=random()*40+minSpin
    
    def physics(this,subPos):
        this.y-=this.fallSpeed*time.dt

        this.rotation_y += this.spinSpeed * time.dt
        # Hit ground? If so, respawn above subject.
        if this.y<0:
            this.x=subPos.x+(random()*40-20)
            this.z+=subPos.z+(random()*40-20)
            this.y+=subPos.y+(random()*10+5)
            # Would be better to check if we've
            # actually hit a terrain block :|
        
