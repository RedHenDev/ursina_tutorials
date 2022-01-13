"""
Snowflake module :)
Merry Christmas! 2021
"""
from ursina import Entity, time
from random import random

class Flake(Entity):
    sub = None

    @staticmethod
    def setSub(_subjectEntity):
        Flake.sub = _subjectEntity

    def __init__(this,orig):
        super().__init__(   
            model='quad',
            texture='flake_1.png',
            position=orig,
            double_sided=True,
            scale=0.2
            )
        this.x+=random()*20-10
        this.z+=random()*20-10
        this.y+=random()*10+5

        minSpeed=1
        this.fallSpeed=random()*4+minSpeed
        minSpin=100
        this.spinSpeed=random()*40+minSpin
    
    def update(this):
        this.physics()
    
    def physics(this):
        subPos=Flake.sub.position
        this.y-=this.fallSpeed*time.dt

        this.rotation_y += this.spinSpeed * time.dt
        # Hit ground? If so, respawn above subject.
        if this.y<0:
            this.x=subPos.x+(random()*20-10)
            this.z=subPos.z+(random()*20-10)
            this.y+=subPos.y+(random()*10+5)
            # Would be better to check if we've
            # actually hit a terrain block :|

class SnowFall():
    def __init__(this, _subref):
        this.flakes = []
        Flake.setSub(_subref)
        for i in range(128):
            e = Flake(_subref.position)
            this.flakes.append(e)