import pygame
from classPersona import Persona
from classSpriteSheet import SpriteSheet
from classFireBall import FireBall
from images import *
from sounds import *
import math


class SkullBoss(Persona):
    def __init__(self, image, position, height, width, game, second_fase_image):
        self.frame_x = 0
        self.frame_y = 1
        self.max_frame_x = 7
        super().__init__(image, position, height, width, game)
        self.max_count = 7
        self.second_fase_image = SpriteSheet(second_fase_image)
        self.current_image = self.sprite.get_image(
            self.frame_x, self.frame_y, self.rect.width, self.rect.height, 2, (0, 0, 0))
        self.states = {"IDLE": SkullIdle(self.game, self), "ATTACK": SkullAtack(
            self.game, self), "HIT": SkullHit(self.game, self), "DIE": SkullDie(self.game, self)}
        self.lives = 20
        self.set_state("IDLE")
        self.attacking = False
        self.bouncing = True
        self.moving = False
        self.is_up = False
        self.first_position = position[1]
        self.second_position = position[1]-650
        self.angle = 0
        self.shot = False
        self.wave = True
        self.shots = 0
        self.second_fase = False
        self.changing_position = False
        self.wave_direction = False

    def update(self):
        self.current_state.handle_input()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.bouncing:
            if self.angle >= math.pi*2:
                self.angle = 0
                self.rect.y -= 2
                self.rect.x += 2

            self.speed_y = (-1 * math.sin(self.angle))*2
            self.speed_x = (-1 * math.cos(self.angle))*2

            self.angle += .1
        if self.moving:
            self.bounce = False
            if self.is_up:
                self.speed_y = 2
                if self.rect.y >= self.first_position - (self.rect.height/2+50):
                    self.is_up = False
                    self.moving = False
                    self.bounce = True

            else:
                self.speed_y = -2
                if self.rect.y <= self.second_position:
                    self.is_up = True
                    self.moving = False
                    self.bounce = True
        if (self.lives == 15 or self.lives == 10) and not self.changing_position:
            self.moving = True
            self.changing_position = True
        if self.lives <= 10 and not self.moving:
            self.second_fase = True
            self.sprite = self.second_fase_image

    def draw(self, surface):
        self.current_image = self.sprite.get_image(
            self.frame_x, self.frame_y, self.rect.width, self.rect.height, 2, (0, 0, 0))
        super().draw(surface)

    def get_frame(self):
        super().get_frame()

    def set_state(self, state):
        return super().set_state(state)

    def top_rect(self):
        return super().top_rect()

    def bottom_rect(self):
        return super().bottom_rect()

    def left_rect(self):
        return super().left_rect()

    def right_rect(self):
        return super().right_rect()


class SkullState():
    def __init__(self, state, game, skull):
        self.game = game
        self.state = state
        self.skull = skull


class SkullIdle(SkullState):
    def __init__(self, game, skull):
        super().__init__("IDLE", game, skull)

    def enter(self):
        self.skull.speed_x = 0
        self.skull.frame_x = 0
        self.skull.max_frame_x = 5
        self.skull.frame_y = 0
        self.skull.max_count = 7

    def handle_input(self):
        if self.skull.frame_x >= self.skull.max_frame_x and not self.skull.moving:
            self.skull.set_state("ATTACK")


class SkullAtack(SkullState):
    def __init__(self, game, skull):
        super().__init__("ATTACK", game, skull)

    def enter(self):
        self.skull.speed_x = 0
        self.skull.frame_x = 0
        self.skull.max_frame_x = 7
        self.skull.frame_y = 1
        self.skull.max_count = 7

    def handle_input(self):
        if self.skull.frame_x == 4 and not self.skull.shot:
            boss_shoot_sound.play()
            self.skull.shot = True
            self.skull.shots += 1
            self.skull.wave_direction = not self.skull.wave_direction
            if self.skull.second_fase:
                self.game.level.projectiles.append(FireBall(
                    self.game, blue_fire_ball_image, 32, 32, (self.skull.rect.x + self.skull.width/2,
                                                              self.skull.rect.y + self.skull.rect.height), 4, 0, blue_fire_ball_explosion_image, 3,
                    self.skull.wave, self.skull.wave_direction, True, False))
            else:
                self.game.level.projectiles.append(FireBall(
                    self.game, fire_ball_image, 32, 32, (self.skull.rect.x + self.skull.width/2,
                                                         self.skull.rect.y + self.skull.rect.height), 4, 0, fire_ball_explosion_image, 3,
                    self.skull.wave, self.skull.wave_direction, True, False))
        if self.skull.frame_x != 4:

            self.skull.shot = False
        if self.skull.shots >= 10 or self.skull.moving:
            self.skull.shots = 0
            self.skull.wave = not self.skull.wave
            self.skull.set_state("IDLE")


class SkullHit(SkullState):
    def __init__(self, game, skull):
        super().__init__("HIT", game, skull)

    def enter(self):
        self.skull.changing_position = False
        self.skull.speed_x = 0
        self.skull.frame_x = 0
        self.skull.max_frame_x = 1
        self.skull.frame_y = 2
        self.skull.max_count = 7
        self.skull.lives -= 1

    def handle_input(self):
        if self.skull.lives <= 0:
            self.skull.set_state("DIE")
        if self.skull.frame_x >= self.skull.max_frame_x:
            self.skull.set_state("IDLE")


class SkullDie(SkullState):
    def __init__(self, game, skull):
        super().__init__("DIE", game, skull)

    def enter(self):
        self.skull.bounce = False
        self.skull.speed_x = 0
        self.skull.frame_x = 0
        self.skull.max_frame_x = 10
        self.skull.frame_y = 3
        self.skull.max_count = 5
        boss_death_sound.play()

    def handle_input(self):
        if self.skull.frame_x >= self.skull.max_frame_x:
            self.skull.dead = True
