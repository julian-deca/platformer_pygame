import pygame


class Item():
    def __init__(self, game, image, width, height, position, initial_speed_x, nature, animated=False, max_frame_x=None):
        self.game = game
        self.width = width
        self.height = height
        self.animated = animated
        if self.animated:
            self.sprite_sheet = pygame.transform.scale(
                image, (((width)*(max_frame_x+1)), height))
            self.image = pygame.Surface(
                (self.width, self.height)).convert_alpha()
            self.count = 0
            self.max_count = 5
            self.frame_x = 0
            self.max_frame_x = max_frame_x
        else:
            self.image = pygame.transform.scale(
                image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.gravity = 1
        self.on_ground = False
        self.speed_x = initial_speed_x
        self.speed_y = 20
        self.collided = False
        self.in_field = False
        self.nature = nature

    def draw(self, screen):
        if self.animated:
            self.image.fill(0)
            self.image.blit(self.sprite_sheet, (0, 0), ((self.frame_x*self.width),
                                                        0, self.width, self.height))
            self.image.set_colorkey(0)
            screen.blit(self.image, self.rect)
            if self.count == self.max_count:
                self.get_frame()
                self.count = 0

            else:
                self.count += 1
        else:
            screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)

    def update(self):
        self.rect.x += self.game.level.screen_scroll
        if not self.on_ground:
            self.speed_y += self.gravity

        if not self.in_field:
            for platform in self.game.level.platforms:
                if self.rect.colliderect(platform.rect):
                    if self.rect.colliderect(platform.right) or self.rect.colliderect(platform.left):
                        if not self.collided:
                            self.speed_x = -self.speed_x
                        self.collided = True
                    else:
                        self.collided = False
                    if self.rect.colliderect(platform.bottom) and not self.on_ground:
                        self.speed_y = 0
                        # self.rect.top = platform.rect.bottom + 5
                    if self.rect.colliderect(platform.top) and not self.on_ground:
                        self.on_ground = True
                        self.rect.bottom = platform.rect.top+1
                        if self.speed_y > 3:
                            self.speed_y = -self.speed_y/2
                        break

                else:
                    self.on_ground = False
            if self.speed_y > 3 or self.speed_y < -3:
                self.rect.y += self.speed_y
            if not self.collided:
                if self.speed_x > 0:
                    self.speed_x -= .1
                elif self.speed_x < 0:
                    self.speed_x += .1
        else:
            if self.rect.x < self.game.level.player.rect.center[0]:
                self.speed_x = 4
            elif self.rect.x > self.game.level.player.rect.center[0]:
                self.speed_x = -4
            if self.rect.y < self.game.level.player.rect.center[1]:
                self.rect.y += 4
            elif self.rect.y > self.game.level.player.rect.center[1]:
                self.rect.y -= 4
        self.rect.x += self.speed_x

    def get_frame(self):
        self.frame_x += 1
        if self.frame_x > self.max_frame_x:
            self.frame_x = 0
