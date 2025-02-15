import pygame

from random import randint

from dino_runner.components.osbstacles.cactus import Cactus
from dino_runner.components.osbstacles.bird import Bird
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD


class ObstacleManager:
    # [ ] Corrigir a lógica para ficar orientada a objeto corretamente
    def __init__(self):
        self.obstacles = []
        self.alternate_append_index = 0

    def update(self, game):
        if len(self.obstacles) == 0:
            self.alternate_append_index = randint(0, 2)
            if self.alternate_append_index == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS))
            elif self.alternate_append_index == 1:
                self.obstacles.append(Bird(BIRD))
            else:
                self.obstacles.append(Cactus(LARGE_CACTUS))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.has_power_up:
                    pygame.time.delay(1000)
                    game.playing = False
                    game.death_count += 1
                    break
                elif game.player.type == "shield":
                    pass
                elif game.player.type == "hammer":
                    self.obstacles.remove(obstacle)
                elif game.player.type == "heart":
                    pygame.time.delay(500)
                    self.obstacles.remove(obstacle)
                    game.player.has_power_up = False

    def draw(self, screen):
        for obstacles in self.obstacles:
            obstacles.draw(screen)

    def reset_obstacle(self):
        self.obstacles = []
