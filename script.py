import pygame
from classSpriteSheet import SpriteSheet
from classPersona import Persona
from classGame import Game
W, H = 1500, 1000

pygame.init()
SCREEN = pygame.display.set_mode((W, H))

game = Game(SCREEN, W, H)

FPS = 60

clock = pygame.time.Clock()
frame = 0
flag = True


pygame.time.set_timer(pygame.USEREVENT, 1000)

while flag:
    clock.tick(FPS)
    SCREEN.fill((10, 10, 10))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False

        elif event.type == pygame.USEREVENT and not game.in_menu:
            if game.level.time > 0:
                game.level.time -= 1
            if game.level.player.buffs["CROWN"] > 0:
                game.level.player.buffs["CROWN"] -= 1
            if game.level.player.buffs["SHROOM"] > 0:
                game.level.player.buffs["SHROOM"] -= 1
            if game.level.player.buffs["MAGNET"] > 0:
                game.level.player.buffs["MAGNET"] -= 1
        elif event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            if game.entering_name:
                game.menu.check_name(key)

    keys = pygame.key.get_pressed()
    game.update(keys)
    game.draw(SCREEN)

    pygame.display.update()

pygame.quit()
