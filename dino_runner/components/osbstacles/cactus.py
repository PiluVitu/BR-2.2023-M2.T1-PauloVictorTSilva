from random import randint

from dino_runner.components.osbstacles.obstacle import Obstacle


class Cactus(Obstacle):
    def __init__(self, image):
        self.type = randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325
