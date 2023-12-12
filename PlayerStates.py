import pygame
from classArrow import Arrow
from images import arrow_image
from sounds import *


class State():
    def __init__(self, state, game):
        self.game = game
        self.state = state


class Run(State):
    def __init__(self, game):
        super().__init__("RUN", game)

    def enter(self):
        self.game.level.player.invulnerable = False
        self.game.level.player.speed_x = 5
        self.game.level.player.frame_x = 0
        self.game.level.player.max_frame_x = 7
        self.game.level.player.frame_y = 0
        self.game.level.player.max_count = 5

    def handle_input(self, keys):
        if keys[pygame.K_SPACE] and self.game.level.player.on_ground:
            self.game.level.player.set_state("JUMP")
        elif keys[pygame.K_r]:
            self.game.level.player.set_state("ROLL")
        elif keys[pygame.K_c]:
            self.game.level.player.set_state("SHOOT")
        elif not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and not keys[pygame.K_d] and not keys[pygame.K_a]:
            self.game.level.player.set_state("IDLE")
        elif self.game.level.player.sliding:
            self.game.level.player.set_state("SLIDE")


class Die(State):
    def __init__(self, game):
        super().__init__("DIE", game)

    def enter(self):
        self.game.level.player.invulnerable = True
        self.game.level.player.speed_x = 0
        self.game.level.player.frame_x = 0
        self.game.level.player.max_frame_x = 7
        self.game.level.player.frame_y = 1
        self.game.level.player.max_count = 5
        player_death_audio.play()

    def handle_input(self, keys):
        if self.game.level.player.frame_x == self.game.level.player.max_frame_x and self.game.level.player.lives <= 0:
            self.game.level.player.dead = True
            self.game.level.lost = True


class Roll(State):
    def __init__(self, game):
        super().__init__("ROLL", game)

    def enter(self):
        self.game.level.player.invulnerable = True
        self.game.level.player.frame_x = 0
        self.game.level.player.max_frame_x = 6
        self.game.level.player.frame_y = 2
        self.game.level.player.speed_x = 0
        self.game.level.player.max_count = 6
        player_roll_audio.play()

    def handle_input(self, keys):
        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or keys[pygame.K_d] or keys[pygame.K_a]:
            self.game.level.player.speed_x = 5
        elif self.game.level.player.speed_x > 0:
            self.game.level.player.speed_x -= 1
        if not keys[pygame.K_r] and self.game.level.player.frame_x >= self.game.level.player.max_frame_x and self.game.level.player.speed_y <= 0:
            self.game.level.player.set_state("IDLE")
        elif self.game.level.player.frame_x >= self.game.level.player.max_frame_x and self.game.level.player.speed_y > 0:
            self.game.level.player.set_state("FALL")


class Shoot(State):
    def __init__(self, game):
        super().__init__("SHOOT", game)

    def enter(self):
        self.game.level.player.invulnerable = False
        self.game.level.player.frame_x = 0
        self.game.level.player.max_frame_x = 6
        self.game.level.player.frame_y = 3
        if self.game.level.player.on_ground:
            self.game.level.player.speed_x = 0
        if self.game.level.player.buffs["SHROOM"] > 0:
            self.game.level.player.max_count = 0
        else:
            self.game.level.player.max_count = 3

    def handle_input(self, keys):
        if self.game.level.player.frame_x == self.game.level.player.max_frame_x:
            self.game.level.arrows.append(Arrow(self.game,
                                                arrow_image, 62, 6, (self.game.level.player.rect.x+(self.game.level.player.rect.width)/2,
                                                                     self.game.level.player.rect.y+(self.game.level.player.rect.height/2)-6),
                                                10, not self.game.level.player.facing_right))
            player_shoot_sound.play()

        if not keys[pygame.K_c] and self.game.level.player.speed_y <= 0:
            self.game.level.player.set_state("IDLE")
        elif not keys[pygame.K_c] and self.game.level.player.speed_y >= 0:
            self.game.level.player.set_state("FALL")
        if self.game.level.player.frame_x >= self.game.level.player.max_frame_x and self.game.level.player.speed_y <= 0:
            self.game.level.player.set_state("IDLE")
        elif self.game.level.player.frame_x >= self.game.level.player.max_frame_x and self.game.level.player.speed_y >= 0:
            self.game.level.player.set_state("FALL")


class Slide(State):
    def __init__(self, game):
        super().__init__("SLIDE", game)

    def enter(self):
        self.game.level.player.invulnerable = False
        self.game.level.player.frame_x = 0
        self.game.level.player.max_frame_x = 5
        self.game.level.player.frame_y = 4
        self.game.level.player.max_count = 5

    def handle_input(self, keys):
        if not self.game.level.player.sliding and self.game.level.player.speed_y >= 0:
            self.game.level.player.set_state("FALL")
        if not self.game.level.player.sliding and self.game.level.player.speed_y < 0:
            self.game.level.player.set_state("IDLE")


class Idle(State):
    def __init__(self, game):
        super().__init__("IDLE", game)

    def enter(self):
        self.game.level.player.invulnerable = False
        self.game.level.player.speed_x = 0
        self.game.level.player.frame_x = 0
        self.game.level.player.max_frame_x = 3
        self.game.level.player.frame_y = 5
        self.game.level.player.max_count = 5

    def handle_input(self, keys):
        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or keys[pygame.K_d] or keys[pygame.K_a]:
            self.game.level.player.set_state("RUN")
        elif keys[pygame.K_SPACE] and self.game.level.player.on_ground:
            self.game.level.player.set_state("JUMP")
        elif keys[pygame.K_r]:
            self.game.level.player.set_state("ROLL")
        elif keys[pygame.K_c]:
            self.game.level.player.set_state("SHOOT")
        elif self.game.level.player.sliding:
            self.game.level.player.set_state("SLIDE")


class DoubleJump(State):
    def __init__(self, game):
        super().__init__("DOUBLEJUMP", game)

    def enter(self):
        self.game.level.player.invulnerable = False
        self.game.level.player.speed_y = -15
        self.game.level.player.frame_x = 0
        self.game.level.player.max_frame_x = 3
        self.game.level.player.frame_y = 6
        self.game.level.player.double_jumped = True
        self.game.level.player.max_count = 5

    def handle_input(self, keys):
        if self.game.level.player.frame_x >= self.game.level.player.max_frame_x:
            self.game.level.player.set_state("JUMP")


class Jump(State):
    def __init__(self, game):
        super().__init__("JUMP", game)

    def enter(self):
        self.game.level.player.invulnerable = False
        if not self.game.level.player.double_jumped:
            self.game.level.player.speed_y -= 15
        self.game.level.player.on_ground = False
        self.game.level.player.frame_x = 0
        self.game.level.player.max_frame_x = 0
        self.game.level.player.frame_y = 7
        self.game.level.player.pressed_space = True
        self.game.level.player.max_count = 5
        player_jump_sound.play()

    def handle_input(self, keys):
        if not keys[pygame.K_SPACE]:
            self.game.level.player.pressed_space = False

        if keys[pygame.K_SPACE] and not self.game.level.player.double_jumped and not self.game.level.player.pressed_space:
            self.game.level.player.set_state("DOUBLEJUMP")
        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or keys[pygame.K_d] or keys[pygame.K_a]:
            self.game.level.player.speed_x = 5
        elif self.game.level.player.speed_x > 0:
            self.game.level.player.speed_x -= 1
        if self.game.level.player.speed_y >= 0:
            self.game.level.player.set_state("FALL")
        elif self.game.level.player.sliding:
            self.game.level.player.set_state("SLIDE")
        if keys[pygame.K_c]:
            self.game.level.player.set_state("SHOOT")
        if keys[pygame.K_r]:
            self.game.level.player.set_state("ROLL")


class Fall(State):
    def __init__(self, game):
        super().__init__("FALL", game)

    def enter(self):
        self.game.level.player.invulnerable = False
        self.game.level.player.frame_x = 1
        self.game.level.player.max_frame_x = 1
        self.game.level.player.frame_y = 7
        self.game.level.player.max_count = 5

    def handle_input(self, keys):
        self.game.level.player.frame_x = 0
        if not keys[pygame.K_SPACE]:
            self.game.level.player.pressed_space = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or keys[pygame.K_d] or keys[pygame.K_a]:
            self.game.level.player.speed_x = 5
        elif self.game.level.player.speed_x > 0:
            self.game.level.player.speed_x -= 1
        if self.game.level.player.on_ground or self.game.level.player.speed_y < 0:
            self.game.level.player.set_state("IDLE")
        if keys[pygame.K_SPACE] and not self.game.level.player.double_jumped and not self.game.level.player.pressed_space:
            self.game.level.player.set_state("DOUBLEJUMP")
        if self.game.level.player.sliding:
            self.game.level.player.set_state("SLIDE")
        if keys[pygame.K_c]:
            self.game.level.player.set_state("SHOOT")
        if keys[pygame.K_r]:
            self.game.level.player.set_state("ROLL")


class Hit(State):
    def __init__(self, game):
        super().__init__("HIT", game)

    def enter(self):
        self.game.level.player.invulnerable = True
        self.game.level.player.speed_x = 0
        self.game.level.player.frame_x = 0
        self.game.level.player.max_frame_x = 4
        self.game.level.player.frame_y = 8
        self.game.level.player.max_count = 5
        if self.game.level.player.lives > 0:
            self.game.level.player.lives -= 1
        player_hit_sound.play()

    def handle_input(self, keys):
        if self.game.level.player.lives <= 0:
            self.game.level.player.set_state("DIE")
        elif self.game.level.player.frame_x >= self.game.level.player.max_frame_x:
            self.game.level.player.set_state("IDLE")
