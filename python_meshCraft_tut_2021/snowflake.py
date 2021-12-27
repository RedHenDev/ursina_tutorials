"""Snowflake"""
from builtins import staticmethod
from random import random
from ursina import Entity

class Snowflake(Entity):
    def __init__(this):
        super().__init__(
            model='quad',
            double_sided=True,
            texture='flake_1.png',
            scale=5
        )
        this.x = random()*20-10
        this.z = random()*20-10
        this.y = random()*10-5

    @staticmethod
    def populate():
        for i in range(128):
            e=Snowflake()