import pygame


class Button():
    def __init__(self, position, image, scale, text, color_text=0):
        self.position = position
        self.image = pygame.transform.scale(
            image, (image.get_width()*scale, image.get_height() * scale))
        self.hover_image = pygame.transform.scale(
            self.image, (image.get_width()*(scale+.2), image.get_height() * (scale+.2)))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.text = text
        self.color_text = color_text
        self.clicked = False
        self.hover = False
        self.selected = False

    def draw(self, surface, font):
        text = font.render(self.text, False, self.color_text)

        if self.hover or self.selected:
            surface.blit(self.hover_image, self.rect)
            self.rect = self.hover_image.get_rect()

        else:
            surface.blit(self.image, self.rect)
            self.rect = self.image.get_rect()

        self.rect.center = self.position
        surface.blit(text, text.get_rect(center=(self.rect.center)))

    def update(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.hover = True
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        else:
            self.hover = False
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return action


class LevelButton(Button):
    def __init__(self, level, menu, position, image, locked_image, scale, text, color_text=0):
        self.menu = menu
        self.locked_image = pygame.transform.scale(
            locked_image, (locked_image.get_width()*scale, locked_image.get_height() * scale))
        self.level = level

        super().__init__(position, image, scale, text, color_text)

    def draw(self, surface, font):
        if self.selected:
            pass
        if self.level.locked:
            text = font.render(self.text, False, self.color_text)
            surface.blit(self.locked_image, self.rect)
            self.rect = self.locked_image.get_rect()
            self.rect.center = self.position
            surface.blit(text, text.get_rect(center=(self.rect.center)))
        else:
            return super().draw(surface, font)

    def update(self):
        if not self.level.locked:
            if not self.selected and self.menu.level_selected == self.text:
                self.menu.level_selected = False

            action = False
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                self.hover = True
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    action = True
                    self.selected = True
                    self.menu.level_selected = self.text
            elif pygame.mouse.get_pressed()[0] == 1:
                self.selected = False
            elif not self.selected:
                self.hover = False
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            return action
