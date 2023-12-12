import pygame
from PlayerStates import Run, Die, Roll, Shoot, Slide, Idle, DoubleJump, Jump, Fall
from classSpriteSheet import SpriteSheet


class Persona():
    def __init__(self, image, position, height, width, game):
        self.game = game
        self.sprite = SpriteSheet(image)
        self.surface = pygame.Surface((height, width))
        self.rect = self.surface.get_rect()
        self.rect.center = position
        self.height = height
        self.width = width
        self.position = position
        self.dead = False
        self.current_image = self.sprite.get_image(
            self.frame_x, self.frame_y, self.rect.width, self.rect.height, 2, (0, 0, 0))
        self.count = 0
        self.max_count = 5

        self.speed_x = 0
        self.speed_y = 0
        self.gravity = 0.5
        self.facing_right = True
        self.falling = False

        self.on_ground = False

    def draw(self, surface):

        # surface.blit(self.surface, self.rect)

        if self.facing_right:
            surface.blit(self.current_image, (self.rect.x-self.width/2,
                         self.rect.y-self.height/2, self.width, self.height))
        else:
            surface.blit(pygame.transform.flip(
                self.current_image, True, False).convert_alpha(), (self.rect.x-self.width/2, self.rect.y-self.height/2, self.width, self.height))
        if not self.dead:
            if self.count >= self.max_count:
                self.get_frame()
                self.count = 0
            else:
                self.count += 1
        # pygame.draw.rect(surface, (255, 255, 255), self.top_rect(), 1)
        # pygame.draw.rect(surface, (255, 255, 255), self.bottom_rect(), 1)
        # pygame.draw.rect(surface, (255, 255, 255), self.left_rect(), 1)
        # pygame.draw.rect(surface, (255, 255, 255), self.right_rect(), 1)
        # pygame.draw.rect(surface, (255, 255, 255), self.rect, 1)

        # pygame.draw.rect(surface, (255, 255, 255),
        #                  self.current_image.get_rect(), 1)

    def get_frame(self):
        self.frame_x += 1
        if self.frame_x > self.max_frame_x:
            self.frame_x = 0

    def set_state(self, state):
        self.current_state = self.states[state]
        self.current_state.enter()

    def update(self):
        if not self.on_ground:
            if self.speed_y <= 20:
                self.speed_y += self.gravity
            self.rect.y += self.speed_y

        if self.facing_right:
            self.rect.x += self.speed_x

        else:
            self.rect.x -= self.speed_x

        for platform in self.game.level.platforms:
            if self.rect.colliderect(platform.rect):

                if self.left_rect().colliderect(platform.right) and self.speed_x > 0:
                    self.rect.left = platform.rect.right + 1

                if self.right_rect().colliderect(platform.left) and self.speed_x > 0:
                    self.rect.right = platform.rect.left - 1

                if self.top_rect().colliderect(platform.bottom):
                    self.speed_y = 0
                    self.rect.top = platform.rect.bottom + 1

                if self.bottom_rect().colliderect(platform.top):
                    self.on_ground = True
                    self.speed_y = 0
                    self.rect.bottom = platform.rect.top+2
                    self.double_jumped = False
                    self.sliding = False
                    break
            elif self.rect.bottom != platform.rect.top:
                self.on_ground = False

        for arrow in self.game.level.arrows:
            if self.rect.colliderect(arrow.rect):
                if self.bottom_rect().colliderect(arrow):
                    self.on_ground = True
                    self.speed_y = 0
                    self.rect.bottom = arrow.rect.top
                    self.double_jumped = False
                    self.sliding = False
                    break

    def top_rect(self):
        top_rect = pygame.Rect(
            self.rect.x, self.rect.top, self.width, 10)
        return top_rect

    def bottom_rect(self):
        bottom_rect = pygame.Rect(
            self.rect.x, self.rect.bottom-10, self.width, 10)
        return bottom_rect

    def left_rect(self):
        left_rect = pygame.Rect(self.rect.left-1,
                                self.rect.y+5, 10, self.height-10)
        return left_rect

    def right_rect(self):
        right_rect = pygame.Rect(
            self.rect.right-9, self.rect.y+5, 10, self.height-10)
        return right_rect
