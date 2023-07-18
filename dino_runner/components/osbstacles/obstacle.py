import pygame  # noqa: F401
from pygame.sprite import Sprite

from dino_runner.utils.constants import SCREEN_WIDTH


class Obstacle(Sprite):
    def __init__(self, image, type, static=True):
        self.image = image
        self.type = type
        self.static = static
        self.step_index = 0
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self, game_speed, obstacles):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

        if self.step_index >= 10:
            self.step_index = 0

    def draw(self, screen):
        if not self.static:
            self.step_index += 1
            if self.step_index < 5:
                screen.blit(self.image[0], (self.rect.x, self.rect.y))
            else:
                screen.blit(self.image[1], (self.rect.x, self.rect.y))
        else:
            screen.blit(self.image[self.type], (self.rect.x, self.rect.y))
