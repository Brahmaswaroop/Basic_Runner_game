import pygame
import random
from classes.enemy import Enemy
from classes.player import Player

def disp_score():
    # To show the score
    time = pygame.time.get_ticks() - st_time
    score_surf = score_font.render(f"Score: {time//1000}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    pygame.draw.rect(screen, (0, 230, 250), score_rect, 0)
    screen.blit(score_surf, score_rect)

pygame.init()
screen = pygame.display.set_mode((400, 300), pygame.FULLSCREEN)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
ground = 520

background_surf = pygame.image.load("game_files/back3.jpg").convert_alpha()
score_font = pygame.font.Font(None, 50)

player_stand = pygame.image.load("game_files/charSkin1.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 1.5)
player_stand_rect = player_stand.get_rect(center=(display_size[0]/2, display_size[1]/2))

st_time = pygame.time.get_ticks()
game_active = False

player1 = Player(display_size, ground)
enemies = enemy_generator()

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    key_states = pygame.key.get_pressed()

    # When game is running
    if game_active:
        # Drawing background and character
        screen.blit(background_surf, (0, 0))
        player1.draw(screen)
        player1.apply_gravity(player1.rect)

        disp_score()

    # Game over screen
    else:
        screen.fill((124, 159, 192))
        screen.blit(player_stand, player_stand_rect)

        if key_states[pygame.K_SPACE]:
            game_active = True
            player1.rect.midbottom = (display_size[0]/2, ground)
            pygame.display.update()
            st_time = pygame.time.get_ticks()
            enemies = enemy_generator()

    # Player controls when game is active
    if game_active:
        if key_states[pygame.K_SPACE] or key_states[pygame.K_UP]:
            player1.jump()
        elif key_states[pygame.K_LEFT]:
            player1.move_horizontal("left", border=True)
        elif key_states[pygame.K_RIGHT]:
            player1.move_horizontal("right", border=True)

    pygame.display.update()
    clock.tick(60)
