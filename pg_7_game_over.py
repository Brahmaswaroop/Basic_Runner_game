import pygame
import random
import time as tm

def disp_score():
    # To show the score
    time = pygame.time.get_ticks() - st_time
    score_surf = score_font.render(f"Score: {time//1000}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    pygame.draw.rect(screen, (200, 230, 250), score_rect, 20)
    screen.blit(score_surf, score_rect)

def enemy_generator():
    enemy_colors = ["pink", "black", "red", "blue", "green", "yellow", "orange"]
    enemy_positions = [display_size[0], 0]

    ran_enemy_color = random.choice(enemy_colors)
    ran_enemy_pos = random.choice(enemy_positions)

    enemy1 = Enemy(ran_enemy_color)
    enemy1.default_pos = ran_enemy_pos
    return enemy1


class Motion:
    def __init__(self):
        self.vertical_displacement = 0  # For vertical (Y-axis) motion due to gravity or jump
        self.gravity_force = 0.7        # Gravity effect value
        self.rect = None
        self.last_jump_time = 0

    def apply_gravity(self, rect):
        # Apply gravity effect on vertical displacement
        self.vertical_displacement -= self.gravity_force
        rect.bottom -= self.vertical_displacement

        # Ensure the player does not fall below ground level
        if rect.bottom >= ground:
            rect.bottom = ground
            self.vertical_displacement = 0

    def jump(self, interval=0, jump_height=16):
        current_time = tm.time()
        # Apply upward force if player is on the ground
        if self.rect.bottom == ground:
            if current_time - self.last_jump_time >= interval:
                self.vertical_displacement = jump_height
                self.last_jump_time = current_time

    def move_horizontal(self, direction):
        # Move left or right on the X-axis
        if direction == "left":
            self.rect.left -= 7
        elif direction == "right":
            self.rect.left += 7

class Enemy(Motion):
    def __init__(self, color):
        super().__init__()
        self.speed = 7
        self.default_pos = display_size[0]
        self.surf = pygame.Surface((50, 50))
        self.surf.fill(color)
        self.rect = self.surf.get_rect(midbottom=(self.default_pos, ground))

    def draw(self):
        screen.blit(self.surf, self.rect)

class Player(Motion):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("game_files/char1-removebg-preview.png").convert_alpha()
        self.rect = self.surf.get_rect(midbottom=(100, ground))

    def draw(self):
        screen.blit(self.surf, self.rect)

pygame.init()
display_size = (800, 600)
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

background_surf = pygame.image.load("game_files/back3.jpg").convert_alpha()
score_font = pygame.font.Font(None, 50)
ground = 430

player_stand = pygame.image.load("game_files/char1-removebg-preview.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 1.5)
player_stand_rect = player_stand.get_rect(center=(display_size[0]/2, display_size[1]/2))

st_time = pygame.time.get_ticks()
game_active = False

player1 = Player()


while True:
    # When game is running
    if game_active:
        screen.blit(background_surf, (0, 0))
        player1.draw()
        player1.apply_gravity(player1.rect)
        if player1.rect.colliderect(enemy_generator().rect):
            game_active = False
        else:
            enemy_generator().move_horizontal("left")
            enemy_generator().draw()
            disp_score()

    else:
        # The screen display when the game is not running
        screen.fill((124, 159, 192))
        screen.blit(player_stand, player_stand_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    key_states = pygame.key.get_pressed()
    # Game commands
    if game_active:
        if key_states[pygame.K_SPACE] or key_states[pygame.K_UP]:
            player1.jump(interval=3)
        elif key_states[pygame.K_LEFT]:
            player1.move_horizontal("left")
        elif key_states[pygame.K_RIGHT]:
            player1.move_horizontal("right")
    else:
        if key_states[pygame.K_SPACE]:
            game_active = True
            enemy_generator().rect.left = display_size[0]
            player1.rect.left = 100
            st_time = pygame.time.get_ticks()

    pygame.display.update()
    clock.tick(60)
