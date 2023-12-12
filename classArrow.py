import pygame
from classProjectile import Projectile


class Arrow(Projectile):
    def __init__(self, game, image, width, height, position, speed_x,  negative_speed_x):
        super().__init__(game, image, width, height, position,
                         speed_x, 0, negative_speed_x)
        self.collisioned = False

    def update(self):
        self.rect.x += self.game.level.screen_scroll
        if not self.collisioned:
            if self.negative_speed_x:
                self.rect.x -= self.speed_x
            else:
                self.rect.x += self.speed_x

    def draw(self, surface):
        return super().draw(surface)
