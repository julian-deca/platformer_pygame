import pygame
from classLevel import Level
from files import *
from classBackground import Background
from images import *
from classMenu import *


level_1_grid = read_csv("test\\assets\level_1_grid.csv")
level_2_grid = read_csv("test\\assets\level_2_grid.csv")
level_3_grid = read_csv("test\\assets\level_3_grid.csv")


class Game():
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.entering_name = False

        self.in_menu = True
        self.levels = {"LEVEL_1":
                       Level(self, self.screen, [
                           Background(self, level_1_background_1, self.width,
                                      self.height, (self.width/2, self.height/2), 0.2, 1),
                           Background(self, level_1_background_2, self.width,
                                      self.height, (self.width/2, self.height/2), 0.5, 2, True)
                       ],
                           level_1_grid, 400, level_1_floor_image, level_1_platform_image,
                           level_1_left_edge_image, level_1_right_edge_image, False, 120, True),

                       "LEVEL_2":
                       Level(self, self.screen, [
                           Background(self, level_2_background_1, self.width,
                                      self.height, (self.width/2, self.height/2), 0.2, 1),
                           Background(self, level_2_background_2, self.width,
                                      self.height, (self.width/2, self.height/2), 0.5, 1),
                           Background(self, level_2_background_3, self.width,
                                      self.height, (self.width/2, self.height/2), 0.7, 1),
                           Background(self, level_2_background_4, self.width,
                                      self.height, (self.width/2, self.height/2), 0.9, 1)
                       ],
                           level_2_grid, 400, level_2_floor_image, level_2_platform_image,
                           level_2_left_edge_image, level_2_right_edge_image, False, 120, True),

                       "LEVEL_3":
                       Level(self, self.screen, [
                           Background(self, level_3_background_1, self.width,
                                      self.height, (self.width/2, self.height/2), 0.5, 1),
                           Background(self, level_3_background_2, self.width,
                                      self.height, (self.width/2, self.height/2), 0.2, 1),
                       ],
                           level_3_grid, 400, level_3_floor_image, level_3_platform_image,
                           level_3_left_edge_image, level_3_right_edge_image, False, 60, False, False, level_3_left_wall_image,
                           level_3_right_wall_image, level_3_left_border_image, level_3_right_border_image,
                           level_3_top_border_image, level_3_top_left_border_image, level_3_top_right_border_image)

                       }
        self.level = None
        self.next_level = None
        self.menus = {
            "INITIAL": InitialMenu(
                self, menu_background_image, self.width, self.height, menu_sign_image),
            "ENTER_NAME": EnterNameMenu(self, menu_background_image, self.width,
                                        self.height, menu_sign_image),
            "LEVEL_SELECT": LevelSelectMenu(self, menu_background_image, self.width,
                                            self.height, menu_sign_image, menu_level_image, menu_locked_level_image),
            "PAUSE": PauseMenu(self, menu_background_image, self.width, self.height, menu_sign_image),
            "SCORES": ScoresMenu(self, menu_scores_image, self.width, self.height, menu_sign_image)
        }
        self.set_menu("INITIAL")
        self.total_points = 0
        self.player_name = ""

    def draw(self, screen):
        if self.in_menu:
            self.menu.draw(screen)
        else:
            self.level.draw(screen)

    def update(self, keys):
        if self.in_menu:
            self.menu.update()
        else:
            self.level.update(keys)

    def set_menu(self, menu):
        self.in_menu = True
        self.menu = self.menus[menu]
        self.menu.enter()

    def set_level(self, level):
        self.entering_name = False
        self.level = self.levels[level]
        self.level.enter()
        self.in_menu = False
        if level == "LEVEL_1":
            self.next_level = self.levels["LEVEL_2"]
        elif level == "LEVEL_2":
            self.next_level = self.levels["LEVEL_3"]

    def add_points(self):
        total = 0
        for level in self.levels:
            total += self.levels[level].points
        self.total_points = total
