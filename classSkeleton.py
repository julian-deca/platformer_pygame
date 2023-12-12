from classPersona import Persona
from sounds import *
import pygame


class Skeleton(Persona):
    def __init__(self, image, position, height, width, game, walk=False):
        self.frame_y = 3
        self.frame_x = 0
        self.max_frame_x = 3
        self.walk = walk
        self.reached_edge = False
        super().__init__(image, position, height, width, game)
        self.states = {
            "WALK": SkeletonWalk(self.game, self),
            "IDLE": SkeletonIdle(self.game, self),
            "ATTACK": SkeletonAttack(self.game, self),
            "HIT": SkeletonHit(self.game, self),
            "DIE": SkeletonDie(self.game, self)
        }
        self.current_state = self.states["IDLE"]
        self.attacking = False
        self.has_agro = False
        self.lives = 2
        self.dead = False
        # self.set_state("ATTACK")

    def draw(self, surface):
        self.current_image = self.sprite.get_image(
            self.frame_x, self.frame_y, self.rect.width, self.rect.height, 2, (0, 0, 0))
        # pygame.draw.rect(surface, (255, 255, 255), self.attack_rect(), 1)
        # pygame.draw.rect(surface, (255, 255, 255), self.agro_rect(), 1)

        return super().draw(surface)

    def get_frame(self):
        return super().get_frame()

    def set_state(self, state):
        return super().set_state(state)

    def update(self):

        self.rect.x += self.game.level.screen_scroll
        for edge in self.game.level.edges:
            if self.rect.colliderect(edge.edge_rect) and not self.reached_edge:
                self.reached_edge = True
                if self.left_rect().colliderect(edge.edge_rect) and not self.has_agro:
                    self.rect.left = edge.edge_rect.x + edge.edge_rect.width
                    break

                if self.right_rect().colliderect(edge.edge_rect) and not self.has_agro:
                    self.rect.right = edge.edge_rect.x
                    break

            else:
                self.reached_edge = False
        if not self.on_ground:
            if self.speed_y <= 20:
                self.speed_y += self.gravity
            self.rect.y += self.speed_y
            if self.current_state == self.states["WALK"]:
                self.set_state("IDLE")

        if self.facing_right:
            self.rect.x += self.speed_x

        else:
            self.rect.x -= self.speed_x

        for platform in self.game.level.platforms:
            if self.rect.colliderect(platform.rect):

                if self.left_rect().colliderect(platform.right) and self.speed_x > 0:

                    self.rect.left = platform.rect.right + 1
                    self.reached_edge = True

                if self.right_rect().colliderect(platform.left) and self.speed_x > 0:

                    self.rect.right = platform.rect.left - 1
                    self.reached_edge = True

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

        self.current_state.handle_input()
        if self.agro_rect().colliderect(self.game.level.player.rect) and not self.attack_rect().colliderect(self.game.level.player.rect):
            self.has_agro = True
            self.walk = True
            if self.game.level.player.left_rect() > self.right_rect():
                self.facing_right = True
            elif self.game.level.player.right_rect() < self.left_rect():
                self.facing_right = False
        else:
            self.has_agro = False
        if self.attack_rect().colliderect(self.game.level.player.rect) and not self.game.level.player.invulnerable:
            self.has_agro = False
            self.attacking = True

    def top_rect(self):
        return super().top_rect()

    def bottom_rect(self):
        return super().bottom_rect()

    def left_rect(self):
        return super().left_rect()

    def right_rect(self):
        return super().right_rect()

    def agro_rect(self):
        agro_rect = pygame.Rect(self.rect.x-200,
                                self.rect.y-30, 400+self.width/2, self.height+10)
        return agro_rect

    def attack_rect(self):
        if self.facing_right:
            attack_rect = pygame.Rect(self.rect.x,
                                      self.rect.y-10, self.width, self.height-10)
        else:
            attack_rect = pygame.Rect(self.rect.x,
                                      self.rect.y-10, self.width, self.height-10)
        return attack_rect


class SkeletonState():
    def __init__(self, state, game, skeleton):
        self.game = game
        self.state = state
        self.skeleton = skeleton


class SkeletonWalk(SkeletonState):
    def __init__(self, game, skeleton):
        super().__init__("WALK", game, skeleton)

    def enter(self):
        self.skeleton.speed_x = 2
        self.skeleton.frame_x = 0
        self.skeleton.max_frame_x = 11
        self.skeleton.frame_y = 2
        self.skeleton.max_count = 7

    def handle_input(self):
        if self.skeleton.attacking:
            self.skeleton.set_state("ATTACK")
        if self.skeleton.reached_edge and not self.skeleton.has_agro:
            self.skeleton.set_state("IDLE")


class SkeletonIdle(SkeletonState):
    def __init__(self, game, skeleton):
        super().__init__("IDLE", game, skeleton)

    def enter(self):
        self.skeleton.speed_x = 0
        self.skeleton.frame_x = 0
        self.skeleton.max_frame_x = 3
        self.skeleton.frame_y = 3
        self.skeleton.max_count = 10

    def handle_input(self):
        if self.skeleton.attacking:
            self.skeleton.set_state("ATTACK")
        elif self.skeleton.has_agro and not self.skeleton.reached_edge:
            self.skeleton.set_state("WALK")

        elif self.skeleton.walk and self.skeleton.frame_x >= self.skeleton.max_frame_x:
            self.skeleton.facing_right = not self.skeleton.facing_right
            self.skeleton.set_state("WALK")


class SkeletonAttack(SkeletonState):
    def __init__(self, game, skeleton):
        super().__init__("ATTACK", game, skeleton)

    def enter(self):
        self.skeleton.speed_x = 0
        self.skeleton.frame_x = 0
        self.skeleton.max_frame_x = 12
        self.skeleton.frame_y = 0
        self.skeleton.max_count = 5

    def handle_input(self):
        if self.skeleton.attack_rect().colliderect(self.game.level.player.rect) and\
            self.skeleton.frame_x >= 4 and self.skeleton.frame_x <= 10 and\
            not self.game.level.player.invulnerable and\
                self.game.level.player.current_state != self.game.level.player.states["HIT"] and\
                self.game.level.player.current_state != self.game.level.player.states["DIE"]:
            self.game.level.player.set_state("HIT")
        elif not self.skeleton.attack_rect().colliderect(self.game.level.player.rect) and self.skeleton.frame_x >= self.skeleton.max_frame_x:
            self.skeleton.attacking = False
            self.skeleton.set_state("IDLE")


class SkeletonHit(SkeletonState):
    def __init__(self, game, skeleton):
        super().__init__("HIT", game, skeleton)

    def enter(self):
        self.skeleton.speed_x = 0
        self.skeleton.frame_x = 0
        self.skeleton.max_frame_x = 2
        self.skeleton.frame_y = 4
        self.skeleton.max_count = 6
        self.skeleton.lives -= 1

    def handle_input(self):
        if self.skeleton.lives <= 0:
            self.game.level.spawn_coins(self.skeleton.rect.center, 3)
            self.skeleton.set_state("DIE")
        if self.skeleton.frame_x >= self.skeleton.max_frame_x:
            self.skeleton.set_state("IDLE")


class SkeletonDie(SkeletonState):
    def __init__(self, game, skeleton):
        super().__init__("DIE", game, skeleton)

    def enter(self):
        self.skeleton.speed_x = 0
        self.skeleton.frame_x = 0
        self.skeleton.max_frame_x = 12
        self.skeleton.frame_y = 1
        self.skeleton.max_count = 6

    def handle_input(self):
        if self.skeleton.frame_x >= self.skeleton.max_frame_x:
            self.skeleton.dead = True
