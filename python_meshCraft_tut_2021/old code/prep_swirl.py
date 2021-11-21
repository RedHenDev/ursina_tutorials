from ursina.vec2 import Vec2

class SwirlEngine:
    def __init__(this, subWidth):

        this.subWidth = subWidth
        this.pos = Vec2(0,0)
        this.dir =  [   Vec2(0,1),
                        Vec2(1,0),
                        Vec2(0,-1),
                        Vec2(-1,0)]
        this.reset()
    
    def reset(this):
        this.currentDir = 0
        this.iteration = 1
        this.count = 0
        this.run = 1
    
    def newRun(this):
        # Reset count.
        this.count = 0
        #  Turn.
        this.currentDir+=1
        if this.currentDir>3:
            this.currentDir=0
            this.iteration+=1
        # Find length of run.
        if this.currentDir < 2:
            this.run = this.iteration * 2 - 1
        else:
            this.run = this.iteration * 2
        
    def move(this):
        this.pos.x += ( this.dir[this.currentDir].x * 
                        this.subWidth)
        this.pos.y += ( this.dir[this.currentDir].y * 
                        this.subWidth)
        this.count += 1
        if this.count==this.run:
            this.newRun()