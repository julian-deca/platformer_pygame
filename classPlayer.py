from classPersona import Persona
from PlayerStates import *
from sounds import *
import pygame


class Player(Persona):
    def __init__(self, image, position, height, width, game, scrolling, time):
        self.frame_y = 5
        self.frame_x = 0
        self.max_frame_x = 3
        super().__init__(image, position, height, width, game)
        self.states = {
            "RUN": Run(self.game),
            "DIE": Die(self.game),
            "ROLL": Roll(self.game),
            "SHOOT": Shoot(self.game),
            "SLIDE": Slide(self.game),
            "IDLE": Idle(self.game),
            "DOUBLEJUMP": DoubleJump(self.game),
            "JUMP": Jump(self.game),
            "FALL": Fall(self.game),
            "HIT": Hit(self.game)
        }
        self.current_state = self.states["IDLE"]
        self.double_jumped = False
        self.sliding = False
        self.pressed_space = False
        self.invulnerable = False
        self.scrolling = scrolling
        self.lives = 7
        self.dead = False
        self.field_size = 250
        self.pocket = 50
        self.luck = 1
        self.previus_time = time
        self.buffs = {"CROWN": 0, "SHROOM": 0, "MAGNET": 0}

    def draw(self, surface):

        self.current_image = self.sprite.get_image(
            self.frame_x, self.frame_y, self.rect.width, self.rect.height, 2, (0, 0, 0))

        super().draw(surface)
        # pygame.draw.rect(surface, (255, 255, 255), self.pocket_rect(), 1)
        # pygame.draw.rect(surface, (255, 255, 255), self.item_field(), 1)

    def get_frame(self):
        return super().get_frame()

    def set_state(self, state):
        return super().set_state(state)

    def update(self, keys, time):
        self.current_state.handle_input(keys)

        if self.scrolling:
            if (self.rect.right > self.game.width - self.game.level.scroll_threshold and self.facing_right)\
                    or (self.rect.left < self.game.level.scroll_threshold and not self.facing_right):
                if self.facing_right:
                    self.rect.x -= self.speed_x
                    self.game.level.screen_scroll = -self.speed_x
                else:
                    self.rect.x += self.speed_x
                    self.game.level.screen_scroll = self.speed_x
            else:
                self.game.level.screen_scroll = 0

        if self.buffs["CROWN"] > 0:
            self.luck = 3
        else:
            self.luck = 1

        if self.buffs["MAGNET"] > 0:
            self.field_size = 1000
        else:
            self.field_size = 250

        if self.speed_y > 0 and not self.on_ground and not self.current_state == self.states["SHOOT"]\
                and not self.current_state == self.states["ROLL"]\
                and not self.current_state == self.states["HIT"]\
                and not self.current_state == self.states["DIE"]:
            self.set_state("FALL")
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.facing_right = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.facing_right = False

        if self.rect.y >= self.game.height + 100:
            self.dead = True
            self.game.level.lost = True

        return super().update()

    def top_rect(self):
        return super().top_rect()

    def bottom_rect(self):
        return super().bottom_rect()

    def left_rect(self):
        return super().left_rect()

    def right_rect(self):
        return super().right_rect()

    def item_field(self):
        item_field = pygame.Rect(self.rect.center[0]-self.field_size/2, self.rect.center[1] -
                                 self.field_size/2, self.field_size, self.field_size)
        return item_field

    def pocket_rect(self):
        pocket_rect = pygame.Rect(self.rect.center[0]-self.pocket/2, self.rect.center[1] -
                                  self.pocket/2, self.pocket, self.pocket)
        return pocket_rect

    def reset(self):
        self.rect.center = self.position
        self.dead = False
        self.speed_x = 0
        self.speed_y = 0
        self.lives = 7
        self.field_size = 250
        self.luck = 1
        self.buffs = {"CROWN": 0, "SHROOM": 0, "MAGNET": 0}
        self.set_state("IDLE")
