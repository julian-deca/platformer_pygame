import pygame
from classProjectile import Projectile
from classSpriteSheet import SpriteSheet
import math


class FireBall(Projectile):
    def __init__(self, game, image, width, height, position, speed_x, speed_y, explosion_image, max_frame_x, wave=False, direction=-1, negative_speed_x=False, negative_speed_y=False):
        super().__init__(game, image, width, height, position,
                         speed_x, speed_y, negative_speed_x, negative_speed_y)
        self.explosion_image = SpriteSheet(explosion_image)
        self.image = SpriteSheet(image)
        self.frame_x = 0
        self.max_frame_x = max_frame_x
        self.current_image = self.image.get_image(
            self.frame_x, 0, self.rect.width, self.rect.height, 2, (0, 0, 0))
        self.count = 0
        self.max_count = 5
        self.wave = wave
        self.angle = 0
        self.collisioned = False
        self.destroyed = False
        self.direction = direction
        if not self.direction and self.wave:
            self.rect.center = (position[0], position[1]-100)
        if self.negative_speed_x:
            self.speed_x = - speed_x
        if self.negative_speed_y:
            self.speed_y = - speed_y

    def draw(self, screen):

        self.current_image = self.image.get_image(
            self.frame_x, 0, self.rect.width, self.rect.height, 2, (0, 0, 0))
        if not self.negative_speed_x:
            screen.blit(pygame.transform.flip(
                self.current_image, True, False).convert_alpha(), (self.rect.x-self.rect.width/2, self.rect.y-self.rect.height/2, self.rect.width, self.rect.height))
        else:
            screen.blit(self.current_image, (self.rect.x-self.rect.width/2,
                                             self.rect.y-self.rect.height/2, self.rect.width, self.rect.height))
        if self.count >= self.max_count:
            self.get_frame()
            self.count = 0
        else:
            self.count += 1
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)

    def update(self):
        if not self.collisioned:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
        if self.wave:
            if self.angle >= math.pi*2:
                self.angle = 0
                self.rect.y += 1
            if self.direction:
                self.speed_y = (-1 * math.sin(self.angle))*10
            else:
                self.speed_y = ((-1*math.cos(self.angle))*10)

            self.angle += .1
        if self.collisioned:
            self.image = self.explosion_image
            if self.frame_x >= self.max_frame_x:
                self.destroyed = True

    def get_frame(self):
        self.frame_x += 1
        if self.frame_x > self.max_frame_x:
            self.frame_x = 0
