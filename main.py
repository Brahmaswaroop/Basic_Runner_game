import pygame
from classes.enemy import EnemyProcessing
from classes.player import Player
from classes.game_texts import disp_score, countdown_timer
from classes.start_menu import build_main_menu
from classes.data_loader import load_level_data
from classes.items import FruitProcessing

pygame.init()
display_size = (1440, 720)
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

ground = 520
start_time = pygame.time.get_ticks()
game_active = False
game_start = False
game_paused = False
alpha_val = 0

background_surf = pygame.image.load("game_files/Stage_backgrounds/back3.jpg").convert_alpha()
player1 = Player(screen, ground, "Character1")
enemy_processor = EnemyProcessing(screen, ground)
fruit_list = []

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    key_states = pygame.key.get_pressed()
    alpha_val, difficulty = build_main_menu(screen, game_active, alpha_val)

    if game_start:
        player1.rect.midbottom = (display_size[0]/2, ground)
        enemies = enemy_processor.enemy_generator(difficulty)
        # countdown_timer(screen, background_surf, 3)
        start_time = pygame.time.get_ticks()
        game_start = False
        continue

    # elif game_paused:
    #     game_paused_menu()

    # When game is running
    if game_active:
        # Drawing background and character
        screen.blit(background_surf, (0, 0))
        player1.draw()
        player1.apply_gravity()
        # fruit_list.append(FruitProcessing(screen).fruit_generator(2))
        # FruitProcessing(screen).fruit_falling(fruit_list)
        enemy_processor.enemy_movement(enemies, difficulty)
        game_active = enemy_processor.collision_detected(enemies, player1.rect)
        score = disp_score(screen, start_time)

    # Player controls when game is active
        if key_states[pygame.K_SPACE] or key_states[pygame.K_UP]:
            player1.jump()
            player1.moving_animation()
        elif key_states[pygame.K_LEFT]:
            player1.move_horizontal("left", border=True)
            player1.moving_animation(direction="left")
        elif key_states[pygame.K_RIGHT]:
            player1.move_horizontal("right", border=True)
            player1.moving_animation(direction="right")
        else:
            player1.moving_animation()

    # Game over screen
    else:
        if key_states[pygame.K_RETURN]:
            game_active = game_start = True

    pygame.display.update()
    clock.tick(60)
