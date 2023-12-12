import pygame
from classButton import *
import re
from sounds import *
from files import *


class Menu():
    def __init__(self, game, background_image, width, height, sign_image):
        self.game = game
        self.background_image = pygame.transform.scale(
            background_image, (width, height)).convert_alpha()
        self.rect = self.background_image.get_rect()
        self.sign_image = sign_image
        self.buttons = []
        self.font = pygame.font.SysFont("Consolas", 40, True)

    def draw(self, screen):
        screen.blit(self.background_image, self.rect)
        for button in self.buttons:
            button.draw(screen, self.font)

    def update(self):
        for button in self.buttons:
            button.update()

    def make_button(self, position, image, scale, text, color_text=0):

        self.buttons.append(
            Button(position, image, scale, text, color_text))

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


class InitialMenu(Menu):

    def __init__(self, game, background_image, width, height, sign_image):
        super().__init__(game, background_image, width, height, sign_image)
        self.make_button((self.rect.width/2 - 200,
                          self.rect.height/2), self.sign_image, 1, "PLAY", 0)
        self.make_button((self.rect.width/2 + 200,
                          self.rect.height/2), self.sign_image, 1, "SCORES", 0)

    def enter(self):
        self.game.entering_name = False
        if self.game.level != None:
            if len(self.game.player_name) > 0:
                load_score(self.game.player_name, self.game.total_points)
            self.game.player_name = ""
            self.game.total_points = 0
            self.game.level.reset()

    def draw(self, screen):
        super().draw(screen)

    def update(self):
        for button in self.buttons:

            if button.update():
                push_button_sound.play()

                if button.text == "PLAY":
                    self.game.set_menu("ENTER_NAME")
                elif button.text == "SCORES":
                    self.game.set_menu("SCORES")

    def make_button(self, position, image, scale, text, color_text=0):
        return super().make_button(position, image, scale, text, color_text)

    def print_text(self, surface, words, size, position, scale, image=None, color=0):
        return super().print_text(surface, words, size, position, scale, image, color)


class LevelSelectMenu(Menu):
    def __init__(self, game, background_image, width, height, sign_image, level_image, locked_level_image):
        self.level_image = level_image
        self.locked_level_image = locked_level_image
        super().__init__(game, background_image, width, height, sign_image)

        # for i in range(1, level_num+1):
        #     self.make_level_button((100, 200), ((self.rect.width/2)-((level_image.get_width()*i*2)),
        #                                         self.rect.height/3), self.level_image, 2, str(i), (255, 255, 255))
        self.level_buttons = []
        self.make_level_button(self.game.levels["LEVEL_1"], (self.rect.width/3,
                                                             self.rect.height/3), self.level_image, self.locked_level_image, 2, "1", (255, 255, 255))
        self.make_level_button(self.game.levels["LEVEL_2"], (self.rect.width/2,
                                                             self.rect.height/3), self.level_image, self.locked_level_image, 2, "2", (255, 255, 255))
        self.make_level_button(self.game.levels["LEVEL_3"], (self.rect.width/1.5,
                                                             self.rect.height/3), self.level_image, self.locked_level_image, 2, "3", (255, 255, 255))

        self.make_button((self.rect.width/2,
                          self.rect.height-200), self.sign_image, 1, "BACK", 0)
        self.level_selected = False
        self.start_level = False

    def enter(self):
        self.game.entering_name = False

        self.level_selected = False

    def draw(self, screen):
        super().draw(screen)
        for button in self.level_buttons:
            button.draw(screen, self.font)

    def update(self):
        if self.level_selected and self.start_level:
            match(self.level_selected):
                case "1":
                    self.game.set_level("LEVEL_1")
                case "2":
                    self.game.set_level("LEVEL_2")
                case "3":
                    self.game.set_level("LEVEL_3")

        for button in self.level_buttons:
            if button.update():
                push_button_sound.play()
                if len(self.buttons) == 1:
                    self.make_button((self.rect.width/2,
                                      self.rect.height-400), self.sign_image, 1, "CONTINUE", 0)
        for button in self.buttons:
            if button.update():
                push_button_sound.play()

                if button.text == "CONTINUE":
                    self.start_level = True
                if button.text == "BACK":
                    if len(self.buttons) == 2:
                        remove = self.buttons.pop(1)
                        del (remove)
                    self.game.set_menu("INITIAL")
                    break
            else:
                self.start_level = False

    def make_button(self, position, image, scale, text, color_text=0):
        return super().make_button(position, image, scale, text, color_text)

    def make_level_button(self, level, position, image, locked_level_image, scale, text, color_text=0):
        self.level_buttons.append(
            LevelButton(level, self, position, image, locked_level_image, scale, text, color_text))


class PauseMenu(Menu):
    def __init__(self, game, background_image, width, height, sign_image):
        super().__init__(game, background_image, width, height, sign_image)
        self.make_button((self.rect.width/2,
                          self.rect.height/1.5), self.sign_image, 1, "LEVEL SELECT", 0)
        self.make_button((self.rect.width/2,
                          self.rect.height/1.5+(self.sign_image.get_height()*1.5)), self.sign_image, 1, "MAIN MENU", 0)
        self.make_button((self.rect.width/2,
                          self.rect.height/3), self.sign_image, 1, "RETURN", 0)

    def draw(self, screen):
        return super().draw(screen)

    def enter(self):
        self.game.entering_name = False

    def update(self):
        for button in self.buttons:
            if button.update():
                if button.text == "MAIN MENU":
                    push_button_sound.play()
                    self.game.set_menu("INITIAL")
                elif button.text == "LEVEL SELECT":
                    push_button_sound.play()
                    self.game.level.reset()
                    self.game.set_menu("LEVEL_SELECT")
                elif button.text == "RETURN":
                    unpause_sound.play()
                    self.game.in_menu = False

    def make_button(self, position, image, scale, text, color_text=0):
        return super().make_button(position, image, scale, text, color_text)


class EnterNameMenu(Menu):
    def __init__(self, game, background_image, width, height, sign_image):
        super().__init__(game, background_image, width, height, sign_image)
        self.make_button((self.rect.width/2,
                          self.rect.height/1.5+(self.sign_image.get_height()*1.5)), self.sign_image, 1, "MAIN MENU", 0)
        self.make_button((self.rect.width/2,
                          self.rect.height/1.5), self.sign_image, 1, "CONTINUE", 0)

    def draw(self, screen):
        super().draw(screen)
        self.print_text(screen, self.game.player_name, 40,
                        (self.game.width/2, 400), 1, self.sign_image)

    def enter(self):
        self.game.entering_name = True

    def update(self):
        for button in self.buttons:
            if button.update():
                push_button_sound.play()

                if button.text == "MAIN MENU":
                    self.game.set_menu("INITIAL")
                if button.text == "CONTINUE" and len(self.game.player_name) > 0:
                    self.game.set_menu("LEVEL_SELECT")

    def check_name(self, key):
        if len(self.game.player_name) <= 9 and len(key) == 1:
            try:
                self.game.player_name += key.upper()
            except ValueError:
                self.game.player_name += key
        elif key == "backspace" and len(self.game.player_name) > 0:
            self.game.player_name = re.sub(r".$", "", self.game.player_name)
        elif key == "return" and len(self.game.player_name) > 0:
            self.game.set_menu("LEVEL_SELECT")

    def make_button(self, position, image, scale, text, color_text=0):
        return super().make_button(position, image, scale, text, color_text)

    def print_text(self, surface, words, size, position, scale, image=None, color=0):
        return super().print_text(surface, words, size, position, scale, image, color)


class ScoresMenu(Menu):

    def __init__(self, game, background_image, width, height, sign_image):
        super().__init__(game, background_image, width, height, sign_image)
        self.make_button((self.rect.width/2,
                          800), self.sign_image, 1, "BACK", 0)
        self.scores = []

    def enter(self):
        self.game.entering_name = False
        scores = get_scores()
        if scores:
            self.scores = sorted(
                scores, key=lambda x: x["points"], reverse=True)

    def draw(self, screen):
        super().draw(screen)
        for i in range(len(self.scores)):
            self.print_text(
                screen, self.scores[i]["name"], 40, (550, 200+(100*i)), 1)
            self.print_text(
                screen, str(self.scores[i]["points"]), 40, (950, 200+(100*i)), 1)

    def update(self):
        for button in self.buttons:
            if button.update():
                push_button_sound.play()

                self.game.set_menu("INITIAL")

    def make_button(self, position, image, scale, text, color_text=0):
        return super().make_button(position, image, scale, text, color_text)

    def print_text(self, surface, words, size, position, scale, image=None, color=0):
        return super().print_text(surface, words, size, position, scale, image, color)
