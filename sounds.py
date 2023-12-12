import pygame
pygame.init()
fire_explosion_sound = pygame.mixer.Sound(
    "test\\assets\\04_Fire_explosion_04_medium.wav")
crate_sound = pygame.mixer.Sound("test\\assets\\03_crate_open_1.wav")
absorb_item_sound = pygame.mixer.Sound("test\\assets\\051_use_item_01.wav")
push_button_sound = pygame.mixer.Sound("test\\assets\\08_Step_rock_02.wav")
pause_sound = pygame.mixer.Sound("test\\assets\\092_Pause_04.wav")
unpause_sound = pygame.mixer.Sound("test\\assets\\098_Unpause_04.wav")
coin_sound = pygame.mixer.Sound("test\\assets\\079_Buy_sell_01.wav")
win_sound = pygame.mixer.Sound("test\\assets\Win sound.wav")
loose_sound = pygame.mixer.Sound("test\\assets\game_over_bad_chest.wav")
arrow_hit_sound = pygame.mixer.Sound("test\\assets\\08_Step_rock_02.wav")


player_death_audio = pygame.mixer.Sound("test\\assets\88_Teleport_02.wav")
player_roll_audio = pygame.mixer.Sound("test\\assets\\35_Miss_Evade_02.wav")
player_hit_sound = pygame.mixer.Sound("test\\assets\\77_flesh_02.wav")
player_jump_sound = pygame.mixer.Sound("test\\assets\\30_Jump_03.wav")
player_shoot_sound = pygame.mixer.Sound("test\\assets\\56_Attack_03.wav")


enemy_hit_sound = pygame.mixer.Sound("test\\assets\\03_Claw_03.wav")

boss_death_sound = pygame.mixer.Sound("test\\assets\\18_Thunder_02.wav")
boss_shoot_sound = pygame.mixer.Sound(
    "test\\assets\\12_human_jump_1.wav")
