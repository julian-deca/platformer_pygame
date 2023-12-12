import pygame


class Background():
    def __init__(self, game, image, width, height, coords, distance_multiplier, scale, should_scale=False):
        self.game = game
        self.should_scale = should_scale
        if should_scale:
            self.image = pygame.transform.scale(
                image, (image.get_width()*scale, image.get_height()*scale)).convert_alpha()
        else:
            self.image = pygame.transform.scale(
                image, (width, height)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = coords
        self.distance_multiplier = distance_multiplier

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.image, (self.rect.x+self.rect.width,
                    self.rect.y, self.rect.width, self.rect.height))
        screen.blit(self.image, (self.rect.x-self.rect.width,
                    self.rect.y, self.rect.width, self.rect.height))
        if self.should_scale:
            screen.blit(self.image, (self.rect.x+self.rect.width*2,
                                     self.rect.y, self.rect.width, self.rect.height))
            screen.blit(self.image, (self.rect.x-self.rect.width*2,
                                     self.rect.y, self.rect.width, self.rect.height))

    def update(self):

        if self.rect.x < -self.rect.width:
            self.rect.x = 0
        else:
            self.rect.x += self.game.level.screen_scroll * self.distance_multiplier
