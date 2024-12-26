import pygame
from classes.enemy import EnemyProcessing
from classes.player import Player
from classes.game_texts import disp_score
from classes.main_menu import build_main_menu
from classes.level_loader import load_level_data

pygame.init()
display_size = (1440, 720)
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
ground = 520

background_surf = pygame.image.load("game_files/Stage_backgrounds/back3.jpg").convert_alpha()
start_time = pygame.time.get_ticks()
game_active = False
alpha_val = 0

player1 = Player(screen, ground)
enemy_processor = EnemyProcessing(screen, ground)
enemies = enemy_processor.enemy_generator(load_level_data("easy"))

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    key_states = pygame.key.get_pressed()
    alpha_val, difficulty = build_main_menu(screen, display_size, game_active, alpha_val)

    # When game is running
    if game_active:
        # Drawing background and character
        screen.blit(background_surf, (0, 0))
        player1.draw()
        player1.apply_gravity()
        enemy_processor.enemy_movement(enemies, difficulty)
        game_active = enemy_processor.collision_detected(enemies, player1.rect)
        disp_score(screen, start_time)

    # Player controls when game is active
    if game_active:
        if key_states[pygame.K_SPACE] or key_states[pygame.K_UP]:
            player1.jump()
        elif key_states[pygame.K_LEFT]:
            player1.move_horizontal("left", border=True)
        elif key_states[pygame.K_RIGHT]:
            player1.move_horizontal("right", border=True)

    # Game over screen
    else:
        if key_states[pygame.K_SPACE]:
            game_active = True
            player1.rect.midbottom = (display_size[0]/2, ground)
            enemies = enemy_processor.enemy_generator(difficulty)
            start_time = pygame.time.get_ticks()

    pygame.display.update()
    clock.tick(60)
