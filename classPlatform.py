import pygame
from classSpriteSheet import SpriteSheet


class Platform():
    def __init__(self, game, x, y, width, height, image=None) -> None:
        self.game = game
        self.image = image
        if image:
            self.image = pygame.transform.scale(image, (width, height))

        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))

        self.surface.fill((255, 25, 5))

        self.rect = self.surface.get_rect()
        self.rect.center = (x + self.width/2, y + self.height/2)

        self.top = self.top_rect()
        self.bottom = self.bottom_rect()
        self.left = self.left_rect()
        self.right = self.right_rect()
        self.destructible = False
        self.invisible = False

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.surface, (self.rect.x, self.rect.y))

        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)

        # pygame.draw.rect(screen, (255, 255, 255), self.top_rect(), 1)
        # pygame.draw.rect(screen, (255, 255, 255), self.bottom_rect(), 1)
        # pygame.draw.rect(screen, (255, 255, 255), self.left_rect(), 1)
        # pygame.draw.rect(screen, (255, 255, 255), self.right_rect(), 1)

    def update(self):
        self.rect.x += self.game.level.screen_scroll
        self.top = self.top_rect()
        self.bottom = self.bottom_rect()
        self.left = self.left_rect()
        self.right = self.right_rect()

    def top_rect(self):
        top_rect = pygame.Rect(self.rect.x+5, self.rect.top, self.width-10, 30)
        return top_rect

    def bottom_rect(self):
        bottom_rect = pygame.Rect(
            self.rect.x+5, self.rect.bottom-20, self.width-10, 20)
        return bottom_rect

    def left_rect(self):
        left_rect = pygame.Rect(
            self.rect.left, self.rect.y+5, 20, self.height-5)
        return left_rect

    def right_rect(self):
        right_rect = pygame.Rect(
            self.rect.right-20, self.rect.y+5, 20, self.height-5)
        return right_rect


class DestructablePlatform(Platform):
    def __init__(self, game, x, y, width, height, max_frame_x, sprite_sheet=None):
        super().__init__(game, x, y, width, height)

        self.sprite_sheet = pygame.transform.scale(
            sprite_sheet, (((width)*(max_frame_x+1)), height))
        if sprite_sheet:
            self.sprite = sprite_sheet
        self.frame_x = 0
        self.max_frame_x = max_frame_x
        self.image = pygame.Surface(
            (self.width, self.height)).convert_alpha()
        self.destructible = True
        self.gravity = 3
        self.on_ground = True
        self.collisioned = False
        self.destroyed = False
        self.count = 0
        self.max_count = 2

    def update(self):
        super().update()
        if not self.on_ground:
            self.rect.y += self.gravity
            self.top = self.top_rect()
            self.bottom = self.bottom_rect()
            self.left = self.left_rect()
            self.right = self.right_rect()
        for platform in self.game.level.platforms:
            if self.rect.colliderect(platform.rect):
                if self.bottom.colliderect(platform.top):
                    self.on_ground = True
                    self.rect.bottom = platform.rect.top+1
                    break
                elif self.rect.bottom != platform.rect.top:
                    self.on_ground = False

    def draw(self, screen):
        self.image.fill(0)
        self.image.blit(self.sprite_sheet, (0, 0), ((self.frame_x*self.width),
                                                    0, self.width, self.height))
        self.image.set_colorkey(0)

        screen.blit(self.image, self.rect)
        if self.collisioned:
            if self.count == self.max_count:
                self.get_frame()
                self.count = 0

            else:
                self.count += 1

        if self.frame_x == self.max_frame_x:
            self.destroyed = True

        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)

        # pygame.draw.rect(screen, (255, 255, 255), self.top_rect(), 1)
        # pygame.draw.rect(screen, (255, 255, 255), self.bottom_rect(), 1)
        # pygame.draw.rect(screen, (255, 255, 255), self.left_rect(), 1)
        # pygame.draw.rect(screen, (255, 255, 255), self.right_rect(), 1)

    def get_frame(self):
        self.frame_x += 1
        if self.frame_x > self.max_frame_x:
            self.frame_x = 0

    def top_rect(self):
        return super().top_rect()

    def bottom_rect(self):
        return super().bottom_rect()

    def left_rect(self):
        return super().left_rect()

    def right_rect(self):
        return super().right_rect()


class EdgeRight(Platform):
    def __init__(self, game, x, y, width, height, image=None):
        super().__init__(game, x, y, width, height, image)
        self.edge_rect = self.edge()

    def draw(self, screen):
        super().draw(screen)
        # pygame.draw.rect(screen, (255, 255, 255), self.edge_rect, 1)

    def update(self):
        super().update()
        self.edge_rect = self.edge()

    def top_rect(self):
        return super().top_rect()

    def bottom_rect(self):
        return super().bottom_rect()

    def left_rect(self):
        return super().left_rect()

    def right_rect(self):
        return super().right_rect()

    def edge(self):
        edge_rect = pygame.Rect(
            self.rect.right-10, self.rect.top - 10, 10, 10)

        return edge_rect


class EdgeLeft(Platform):
    def __init__(self, game, x, y, width, height, image=None):
        super().__init__(game, x, y, width, height, image)
        self.edge_rect = self.edge()

    def draw(self, screen):
        # pygame.draw.rect(screen, (255, 255, 255), self.edge_rect, 1)
        return super().draw(screen)

    def update(self):
        super().update()
        self.edge_rect = self.edge()

    def top_rect(self):
        return super().top_rect()

    def bottom_rect(self):
        return super().bottom_rect()

    def left_rect(self):
        return super().left_rect()

    def right_rect(self):
        return super().right_rect()

    def edge(self):
        edge_rect = pygame.Rect(self.rect.x, self.rect.top-10, 10, 10)
        return edge_rect


class InvisiblePlatform(Platform):
    def __init__(self, game, x, y, width, height):
        super().__init__(game, x, y, width, height)
        self.invisible = True

    def update(self):
        return super().update()

    def draw(self, screen):
        # pygame.draw.rect(screen, (255, 255, 255), self.edge_rect, 1)
        pass

    def top_rect(self):
        return super().top_rect()

    def bottom_rect(self):
        return super().bottom_rect()

    def left_rect(self):
        return super().left_rect()

    def right_rect(self):
        return super().right_rect()


class SawTrap(Platform):
    def __init__(self, game, x, y, width, height, sprite_sheet, max_frame_x):
        super().__init__(game, x, y, width, height, sprite_sheet)
        self.sprite_sheet = pygame.transform.scale(
            sprite_sheet, (((width)*(max_frame_x+1)), height))
        if sprite_sheet:
            self.sprite = sprite_sheet
        self.frame_x = 0
        self.max_frame_x = max_frame_x
        self.image = pygame.Surface(
            (self.width, self.height)).convert_alpha()
        self.count = 0
        self.max_count = 2

    def draw(self, screen):

        self.image.fill(0)
        self.image.blit(self.sprite_sheet, (0, 0), ((self.frame_x*self.width),
                                                    0, self.width, self.height))
        self.image.set_colorkey(0)
        self.image = pygame.transform.flip(self.image, True, True)
        screen.blit(self.image, self.rect)
        if self.count == self.max_count:
            self.get_frame()
            self.count = 0

        else:
            self.count += 1
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)
        # pygame.draw.rect(screen, (255, 255, 255), self.top, 1)
        # pygame.draw.rect(screen, (255, 255, 255), self.left, 1)
        # pygame.draw.rect(screen, (255, 255, 255), self.right, 1)

    def get_frame(self):
        self.frame_x += 1
        if self.frame_x > self.max_frame_x:
            self.frame_x = 0

    def top_rect(self):
        top_rect = pygame.Rect(
            self.rect.x+self.rect.width/3, self.rect.top+self.rect.height/2, self.width/2-10, 10)
        return top_rect

    def left_rect(self):
        left_rect = pygame.Rect(
            self.rect.left+self.rect.width/3-10, self.rect.y+self.rect.height/2+5, 10, self.height/2)
        return left_rect

    def right_rect(self):
        right_rect = pygame.Rect(
            self.rect.right-self.rect.width/3, self.rect.y+self.rect.height/2+5, 10, self.height/2)
        return right_rect
