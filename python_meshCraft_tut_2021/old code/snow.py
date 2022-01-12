"""Snowflake class and methods"""
from ursina import Entity, Mesh, load_model, Vec3, time, Vec4
from random import random
from math import sin, cos, radians, floor

class Snowfall(Entity):
    def __init__(this):
        super().__init__(
            model=Mesh(),
            texture='flake_1.png',
            double_sided=True
        )
        this.flakes=[]
        this.number=1024
        this.quad=load_model('quad')
        this.theta=0 # For rotation of flakes.
        this.fallRate=0.1

        this.generateFlakes()

    def update(this):
        this.theta+=10
        # Use polar co-ordinates to rotate flake's x and z.
        for v in range(len(this.model.vertices)):
            this.model.vertices[v][0] = this.flakes[v][0] + 2*cos(radians(this.theta))*time.dt
            this.model.vertices[v][2] = this.flakes[v][2] + 2*sin(radians(this.theta))*time.dt
            # Now control descent of flake.
            # v[1] -= this.fallRate*time.dt
        this.model.generate()
        # this.y-=this.fallRate*time.dt

    def generateFlakes(this):
        for i in range(this.number):
            x = random()*20-10
            z = random()*20-10
            y = random()*10-5
            this.model.vertices.extend([Vec3(x,y,z) + 
            v for v in this.quad.vertices])
            for j in range(6):
                this.flakes.append(this.model.vertices[-1])
            this.model.colors.extend( (Vec4(1,1,1,1),)*6)
            this.model.uvs = (this.quad.uvs) * (15 * 13)
        this.model.generate()