import pygame

def disp_score():
    # To show the score
    time = pygame.time.get_ticks() - st_time
    score_surf = score_font.render(f"Score: {time//1000}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    pygame.draw.rect(screen, (200, 230, 250), score_rect, 20)
    screen.blit(score_surf, score_rect)

class Motion:
    def __init__(self):
        self.vertical_displacement = 0  # For vertical (Y-axis) motion due to gravity or jump
        self.gravity_force = 0.7        # Gravity effect value
        self.jump_strength = 16         # Strength of the jump

    def apply_gravity(self, rect):
        # Apply gravity effect on vertical displacement
        self.vertical_displacement -= self.gravity_force
        rect.bottom -= self.vertical_displacement

        # Ensure the player does not fall below ground level
        if rect.bottom >= ground:
            rect.bottom = ground
            self.vertical_displacement = 0

    def jump(self, rect):
        # Apply upward force if player is on the ground
        if rect.bottom == ground:
            self.vertical_displacement = self.jump_strength

    def move_horizontal(self, rect, direction):
        # Move left or right on the X-axis
        if direction == "left":
            rect.left -= 7
        elif direction == "right":
            rect.left += 7

ground = 430

pygame.init()
display_size = (800, 600)
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

background_surf = pygame.image.load("game_files/back3.jpg").convert_alpha()
score_font = pygame.font.Font(None, 50)

enemy_surf = pygame.Surface((50, 50))
enemy_surf.fill("black")
enemy_rect = enemy_surf.get_rect(midbottom=(display_size[0], ground))

player_surf = pygame.image.load("game_files/char1-removebg-preview.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom=(100, ground))

player_stand = pygame.image.load("game_files/char1-removebg-preview.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 1.5)
player_stand_rect = player_stand.get_rect(center=(display_size[0]/2, display_size[1]/2))

st_time = pygame.time.get_ticks()
game_active = False
motion = Motion()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    key_states = pygame.key.get_pressed()
    # Game commands
    if game_active:
        if key_states[pygame.K_SPACE] or key_states[pygame.K_UP]:
            motion.jump(player_rect)
        elif key_states[pygame.K_LEFT]:
            motion.move_horizontal(player_rect, "left")
        elif key_states[pygame.K_RIGHT]:
            motion.move_horizontal(player_rect, "right")
    else:
        if key_states[pygame.K_SPACE]:
            game_active = True
            enemy_rect.left = display_size[0]
            player_rect.left = 100
            st_time = pygame.time.get_ticks()

    # When game is running
    if game_active:
        screen.blit(background_surf, (0, 0))
        motion.apply_gravity(player_rect)
        if player_rect.colliderect(enemy_rect):
            game_active = False
        motion.move_horizontal(enemy_rect, "left")
        screen.blit(enemy_surf, enemy_rect)
        screen.blit(player_surf, player_rect)
        disp_score()

    else:
        # The screen display when the game is not running
        screen.fill((124, 159, 192))
        screen.blit(player_stand, player_stand_rect)

    pygame.display.update()
    clock.tick(60)
