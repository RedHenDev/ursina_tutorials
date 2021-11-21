from ursina import Vec2

class SwirlEngine:
    def __init__(this,subWidth):

        this.subWidth = subWidth

        # Tracks position of terrain subset being generated.
        this.pos = Vec2(0,0)

        this.reset(0,0)

        this.dir = [Vec2(0,1),
                    Vec2(1,0),
                    Vec2(0,-1),
                    Vec2(-1,0)]

    def changeDir(this):
        if this.cd < 3:
            this.cd+=1
        else:
            this.cd = 0
            this.iteration+=1
        
        if this.cd < 2:
            this.run = (this.iteration * 2) - 1
        else:
            this.run = (this.iteration * 2)
        
    def move(this):
        if this.count < this.run:
            this.pos.x += this.dir[this.cd].x*this.subWidth
            this.pos.y += this.dir[this.cd].y*this.subWidth
            this.count+=1
        else:
            # Time to change direction :)
            this.count=0
            this.changeDir()
            this.move()

    def reset(this,x,z):
        this.pos.x = x
        this.pos.y = z
        this.run = 1
        this.iteration = 1
        this.count = 0
        this.cd = 0 # Current direction (0-3).