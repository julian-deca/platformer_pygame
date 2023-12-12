import pygame
from classPlayer import Player
from classSkeleton import Skeleton
from classPlatform import *
from classBackground import Background
from images import *
from sounds import *
from classButton import Button
from classItem import Item
from classCoin import Coin
from classSkullBoss import SkullBoss
from classFireBall import FireBall
import random


class Level():
    def __init__(self, game, screen, backgrounds, grid, scroll_threshold, floor_image,
                 platform_image, left_edge_image, right_edge_image, locked, time, has_skeletons, scrolling=True,
                 left_wall_image=None, right_wall_image=None, left_border_image=None,
                 right_border_image=None, top_border_image=None, top_left_border_image=None,
                 top_right_border_image=None) -> None:
        self.game = game
        self.screen = screen
        self.grid = grid

        self.projectiles = []
        self.arrows = []
        self.platforms = []
        self.edges = []
        self.skeletons = []
        self.coins = []
        self.bosses = []
        self.items = []
        self.traps = []

        self.scroll_threshold = scroll_threshold
        self.screen_scroll = 0

        self.backgrounds = backgrounds
        self.floor_image = floor_image
        self.platform_image = platform_image
        self.left_edge_image = left_edge_image
        self.right_edge_image = right_edge_image
        self.left_wall_image = left_wall_image
        self.right_wall_image = right_wall_image
        self.left_border_image = left_border_image
        self.right_border_image = right_border_image
        self.top_border_image = top_border_image
        self.top_left_border_image = top_left_border_image
        self.top_right_border_image = top_right_border_image

        self.locked = locked

        self.font = pygame.font.SysFont("Consolas", 20, True)
        self.pause_button = self.make_button(
            (self.game.width-200, menu_sign_image.get_height()/2), menu_sign_image, .5, "PAUSE")
        self.continue_button = self.make_button(
            (self.game.width/2, 700), menu_sign_image, .7, "CONTINUE")

        self.win = False
        self.lost = False
        self.timer = time
        self.time = time
        self.points = 0
        self.has_skeletons = has_skeletons
        self.player = Player(
            player_image, (500, self.game.height-64*2), 64, 64, self.game, scrolling, self.time)
        self.made_sound = False

    def transform_grid(self):
        size = int(self.game.height / (len(self.grid)-1))

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):

                if self.grid[i][j] == "1":
                    self.platforms.append(
                        Platform(self.game, j * size, (i-1) * size, size, size, self.floor_image))

                elif self.grid[i][j] == "2":
                    self.platforms.append(
                        Platform(self.game, j * size, (i-1) * size, size, size, self.platform_image))

                elif self.grid[i][j] == "3":
                    edge = EdgeRight(self.game, j * size, (i-1) *
                                     size, size, size, self.right_edge_image)
                    self.platforms.append(edge)
                    self.edges.append(edge)

                elif self.grid[i][j] == "4":
                    edge = EdgeLeft(self.game, j * size, (i-1) *
                                    size, size, size, self.left_edge_image)
                    self.platforms.append(edge)
                    self.edges.append(edge)

                elif self.grid[i][j] == "5":
                    self.platforms.append(
                        Platform(self.game, j * size, (i-1) * size, size, size, self.left_wall_image))

                elif self.grid[i][j] == "6":
                    self.platforms.append(
                        Platform(self.game, j * size, (i-1) * size, size, size, self.right_wall_image))

                elif self.grid[i][j] == "7":
                    self.platforms.append(
                        Platform(self.game, j * size, (i-1) * size, size, size, self.left_border_image))

                elif self.grid[i][j] == "8":
                    self.platforms.append(
                        Platform(self.game, j * size, (i-1) * size, size, size, self.right_border_image))

                elif self.grid[i][j] == "9":
                    self.platforms.append(
                        Platform(self.game, j * size, (i-1) * size, size, size, self.top_border_image))

                elif self.grid[i][j] == "10":
                    self.platforms.append(
                        Platform(self.game, j * size, (i-1) * size, size, size, self.top_left_border_image))

                elif self.grid[i][j] == "11":
                    self.platforms.append(
                        Platform(self.game, j * size, (i-1) * size, size, size, self.top_right_border_image))

                elif self.grid[i][j] == "12":
                    self.platforms.append(
                        DestructablePlatform(self.game, j * size, (i-1) * size, size, size, 4, crate_sprite))

                elif self.grid[i][j] == "13":
                    self.skeletons.append(
                        Skeleton(skeleton_image, ((j * size)+64/2, ((i-1)*size)+64/2), 64, 64, self.game))

                elif self.grid[i][j] == "14":
                    self.skeletons.append(
                        Skeleton(skeleton_image, ((j * size)+64/2, ((i-1)*size)+64/2), 64, 64, self.game, True))
                if self.grid[i][j] == "15":
                    self.platforms.append(
                        InvisiblePlatform(self.game, j * size, (i-1) * size, size, size))
                if self.grid[i][j] == "16":
                    self.bosses.append(SkullBoss(skull_boss_image, ((
                        j * size)+240/6, ((i-1)*size)+240/6), 240, 240, self.game, skull_boss_image_fase_2))
                if self.grid[i][j] == "17":
                    self.traps.append(
                        SawTrap(self.game, (j * size)+size, ((i-1) * size)-size, size*2, size*2, saw_trap_image, 15))

    def check_collision(self):
        for platform in self.platforms:
            for arrow in self.arrows:
                if not arrow.collisioned and not platform.invisible:
                    if arrow.rect.colliderect(platform.rect):
                        if platform.destructible:
                            crate_sound.play()
                            self.arrows.remove(arrow)
                            platform.collisioned = True
                            del (arrow)
                            break
                        else:
                            arrow.collisioned = True
                            arrow_hit_sound.play()
            for projectile in self.projectiles:
                if projectile.rect.colliderect(platform.right) or projectile.rect.colliderect(platform.left):
                    projectile.collisioned = True
                    if platform.destructible:
                        platform.collisioned = True

            if platform.destructible and platform.destroyed:
                self.spawn_coins(platform.rect.center, 3)
                self.spawn_random_item(platform.rect.center)

                self.platforms.remove(platform)
                del (platform)
                break

        for skeleton in self.skeletons:
            for arrow in self.arrows:
                if arrow.rect.colliderect(skeleton.rect) and skeleton.current_state != skeleton.states["DIE"]:
                    skeleton.set_state("HIT")
                    enemy_hit_sound.play()
                    self.arrows.remove(arrow)
                    del (arrow)
                    break

            if skeleton.rect.y > self.game.height + 100:
                skeleton.dead = True
            if skeleton.dead:
                self.skeletons.remove(skeleton)
                del (skeleton)
                break
        for arrow in self.arrows:
            if arrow.rect.x < -self.game.width or arrow.rect.x > self.game.width*2:
                self.arrows.remove(arrow)
                del (arrow)
                break
        for coin in self.coins:
            if self.player.item_field().colliderect(coin.rect):
                coin.in_field = True
            else:
                coin.in_field = False
            if self.player.pocket_rect().colliderect(coin.rect):
                coin_sound.play()

                self.points += coin.value
                self.coins.remove(coin)
                del coin
                break
        for item in self.items:
            if self.player.item_field().colliderect(item.rect):
                item.in_field = True
            else:
                item.in_field = False
            if self.player.pocket_rect().colliderect(item.rect):
                absorb_item_sound.play()
                match(item.nature):
                    case "HEART":
                        self.player.lives += 1
                    case "CROWN":
                        self.player.buffs["CROWN"] += 10
                    case "SHROOM":
                        self.player.buffs["CROWN"] += 5
                    case "MAGNET":
                        self.player.buffs["MAGNET"] += 15
                    case "SKULL_KEY":
                        self.points += 100
                        self.player.set_state("JUMP")
                        self.win = True

                self.items.remove(item)
                del item
                break
        for boss in self.bosses:
            if boss.dead:
                self.spawn_item(skull_key_image, "SKULL_KEY", boss.rect.center)
                self.bosses.remove(boss)
                del (boss)
                break
            for arrow in self.arrows:
                if arrow.rect.colliderect(boss.rect) and boss.current_state != boss.states["DIE"]:
                    boss.set_state("HIT")

                    enemy_hit_sound.play()
                    self.arrows.remove(arrow)
                    del (arrow)
                    break
        for projectile in self.projectiles:
            if projectile.rect.colliderect(self.player.rect) and self.player.current_state.state != "HIT"\
                    and not projectile.collisioned and not self.player.invulnerable\
                    and self.player.current_state.state != "DIE":
                fire_explosion_sound.play()
                self.player.set_state("HIT")
                projectile.collisioned = True
            if projectile.destroyed:
                self.projectiles.remove(projectile)
                del projectile
                break
        for trap in self.traps:
            if self.player.rect.colliderect(trap.rect) and self.player.current_state != "HIT"\
                    and self.player.current_state != "DIE"\
                    and not self.player.invulnerable:

                if self.player.rect.colliderect(trap.right):
                    self.player.rect.left = trap.right.right + 20
                    self.player.set_state("HIT")
                    break

                if self.player.rect.colliderect(trap.left):
                    self.player.rect.right = trap.left.left - 20
                    self.player.set_state("HIT")
                    break

                if self.player.rect.colliderect(trap.top):
                    self.player.rect.bottom = trap.top.top - 20
                    self.player.speed_y = -10
                    self.player.set_state("HIT")
                    break

    def update(self, keys):
        self.game.add_points()
        if self.time <= 0:
            self.lost = True
        if not self.win and not self.lost:
            for background in self.backgrounds:
                background.update()
            for arrow in self.arrows:
                arrow.update()
            for skeleton in self.skeletons:
                skeleton.update()
            for platform in self.platforms:
                platform.update()
            for trap in self.traps:
                trap.update()
            for coin in self.coins:
                coin.update()
            for boss in self.bosses:
                boss.update()
            for projectile in self.projectiles:
                projectile.update()
            for item in self.items:
                item.update()
            self.player.update(keys, self.time)
            self.check_collision()
            if len(self.arrows) > 5:
                arrow = self.arrows.pop(0)
                del (arrow)
            if len(self.skeletons) == 0 and self.has_skeletons:
                self.player.set_state("JUMP")
                self.win = True
        else:
            if self.continue_button.update():
                if self.game.next_level and self.win:
                    self.game.next_level.locked = False
                self.reset()
                self.game.set_menu("LEVEL_SELECT")
        if self.pause_button.update():
            pause_sound.play()
            self.game.set_menu("PAUSE")

    def draw(self, screen):
        for background in self.backgrounds:
            background.draw(screen)
        for arrow in self.arrows:
            arrow.draw(screen)
        for platform in self.platforms:
            platform.draw(screen)
        for trap in self.traps:
            trap.draw(screen)
        for skeleton in self.skeletons:
            skeleton.draw(screen)
        for coin in self.coins:
            coin.draw(screen)
        for boss in self.bosses:
            boss.draw(screen)
        for projectile in self.projectiles:
            projectile.draw(screen)
        for item in self.items:
            item.draw(screen)
        self.player.draw(screen)
        self.pause_button.draw(screen, self.font)
        self.print_text(screen, "Lives: " + str(self.player.lives), 20,
                        (200, menu_sign_image.get_height()/2), .5, menu_sign_image)
        self.print_text(screen, "Points: " + str(self.game.total_points), 20,
                        (400, menu_sign_image.get_height()/2), .5, menu_sign_image)
        if self.time <= 10:
            self.print_text(screen, "Time: " + str(self.time), 20,
                            (self.game.width/2, menu_sign_image.get_height()/2), .5, menu_sign_image, (255, 0, 0))
        else:
            self.print_text(screen, "Time: " + str(self.time), 20,
                            (self.game.width/2, menu_sign_image.get_height()/2), .5, menu_sign_image)
        if self.win:
            self.print_text(screen, "YOU WIN", 50,
                            (self.game.width/2, 400), 1, menu_sign_image)
            self.continue_button.draw(
                screen, pygame.font.SysFont("Consolas", 30, True))
            if not self.made_sound:
                self.points += self.time
                win_sound.play()
                self.made_sound = True
        elif self.lost:
            self.print_text(screen, "GAME OVER", 50,
                            (self.game.width/2, 400), 1, menu_sign_image)
            self.continue_button.draw(
                screen, pygame.font.SysFont("Consolas", 30, True))
            if not self.made_sound:
                loose_sound.play()
                self.made_sound = True

    def make_button(self, position, image, scale, text, color_text=0):

        return Button(position, image, scale, text, color_text)

    def reset(self):
        del self.skeletons[:]
        del self.platforms[:]
        del self.arrows[:]
        del self.projectiles[:]
        del self.coins[:]
        del self.edges[:]
        del self.bosses[:]
        del self.items[:]
        del self.traps[:]

        for background in self.backgrounds:
            background.rect.x = 0
        self.screen_scroll = 0
        self.made_sound = False
        self.time = self.timer
        self.win = False
        self.lost = False

        self.player.reset()

    def enter(self):
        self.points = 0
        self.transform_grid()

    def print_text(self, surface, words, size, position, scale, image=None, color=0):
        font = pygame.font.SysFont("Consolas", size, True)
        text = font.render(words, False, color)
        center = text.get_rect(
            center=(position))

        if image:
            image = pygame.transform.scale(
                image, (scale*image.get_width(), scale*image.get_height()))
            rect = image.get_rect()
            rect.center = position
            surface.blit(image, rect)
            surface.blit(text, text.get_rect(center=rect.center))
        else:
            surface.blit(text, center)

    def spawn_coins(self, position, max_coins):
        ammount = int(random.randint(1, max_coins)*self.player.luck)
        for i in range(0, ammount):
            speed = random.randint(-5, 5)
            self.coins.append(Coin(self.game, coin_sheet,
                              16, 16, position, 1, speed))

    def spawn_random_item(self, position):
        spawn_chance = random.randint(1, 10)+self.player.luck
        if spawn_chance >= 10:
            spawn_seed = random.randint(1, 4)
            match(spawn_seed):
                case 1:
                    self.spawn_item(heart_sheet, "HEART", position, True, 5)
                case 2:
                    self.spawn_item(crown_image, "CROWN", position)
                case 3:
                    self.spawn_item(magnet_image, "MAGNET", position)
                case 4:
                    self.spawn_item(shroom_image, "SHROOM", position)

    def spawn_item(self, image, nature, position, animate=False, max_frame=None):
        speed = random.randint(-5, 5)
        self.items.append(Item(self.game, image,
                               32, 32, position, speed, nature, animate, max_frame))
