import pygame


class Projectile():
    def __init__(self, game, image, width, height, position, speed_x, speed_y, negative_speed_x=False, negative_speed_y=False):
        self.game = game
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.negative_speed_x = negative_speed_x
        self.negative_speed_y = negative_speed_y

    def draw(self, surface):

        if self.negative_speed_x:
            surface.blit(pygame.transform.flip(
                self.image, True, False), self.rect)
        else:
            surface.blit(self.image, self.rect)

    def update(self):
        self.rect.x += self.game.level.screen_scroll
        if self.negative_speed_x:
            self.rect.x -= self.speed_x
        else:
            self.rect.x += self.speed_x
        self.rect.y += self.speed_y
