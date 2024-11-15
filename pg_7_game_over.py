import pygame
import random
import time as tm

def disp_score():
    # To show the score
    time = pygame.time.get_ticks() - st_time
    score_surf = score_font.render(f"Score: {time//1000}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    pygame.draw.rect(screen, (200, 230, 250), score_rect, 0)
    screen.blit(score_surf, score_rect)

def enemy_generator(num_enemies=2):
    enemy_colors = ['green', 'blue', 'red']
    enemy_direction = [(display_size[0], "left"), (0, "right")]
    enemies1 = []

    for enemy1 in range(num_enemies):
        ran_enemy_color = random.choice(enemy_colors)
        ran_enemy_direction = random.choice(enemy_direction)

        enemy1 = Enemy(ran_enemy_color, ran_enemy_direction[0])
        enemy1.direction = ran_enemy_direction[1]
        enemy1.speed = random.randint(4, 15)
        enemy1.jump_strength = random.randint(10, 20)
        enemy1.jump_interval = random.uniform(1, 3)
        enemies1.append(enemy1)

    return enemies1

class Motion:
    def __init__(self):
        self.vertical_displacement = 0  # For vertical (Y-axis) motion due to gravity or jump
        self.gravity_force = 0.7        # Gravity effect value
        self.rect = None
        self.speed = 5
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
            # check if the time passed after the last jump is more than the interval
            if current_time - self.last_jump_time >= interval:
                self.vertical_displacement = jump_height
                self.last_jump_time = current_time

    def move_horizontal(self, direction, border=False):
        # Move left or right on the X-axis
        if direction == "left":
            # To prevent the rect to go beyond the window border
            if border:
                if self.rect.left >= 0:
                    self.rect.left -= self.speed
            else:
                self.rect.left -= self.speed
        elif direction == "right":
            if border:
                if self.rect.right <= display_size[0]:
                    self.rect.right += self.speed
            else:
                self.rect.right += self.speed

class Enemy(Motion):
    def __init__(self, color, pos):
        super().__init__()
        self.speed = 7
        self.default_pos = pos
        self.direction = None
        self.jump_strength = 0
        self.jump_interval = 0
        self.surf = pygame.Surface((50, 50))
        self.surf.fill(color)
        self.rect = self.surf.get_rect(midbottom=(self.default_pos, ground))

    def draw(self):
        screen.blit(self.surf, self.rect)

class Player(Motion):
    def __init__(self):
        super().__init__()
        self.speed = 7
        self.surf = pygame.image.load("game_files/char1-removebg-preview.png").convert_alpha()
        self.rect = self.surf.get_rect(midbottom=(display_size[0]/2, ground))

    def draw(self):
        screen.blit(self.surf, self.rect)

pygame.init()
display_size = (1440, 720)
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

background_surf = pygame.image.load("game_files/back3.jpg").convert_alpha()
score_font = pygame.font.Font(None, 50)
ground = 520

player_stand = pygame.image.load("game_files/char1-removebg-preview.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 1.5)
player_stand_rect = player_stand.get_rect(center=(display_size[0]/2, display_size[1]/2))

st_time = pygame.time.get_ticks()
game_active = False

player1 = Player()
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
        player1.draw()
        player1.apply_gravity(player1.rect)

    # Processing enemies
        for enemy in enemies:
            # Enemy movement and jumping
            enemy.move_horizontal(enemy.direction)
            enemy.apply_gravity(enemy.rect)
            enemy.jump(interval=enemy.jump_interval, jump_height=enemy.jump_strength)
            enemy.draw()

            # Check for collisions
            if player1.rect.colliderect(enemy.rect):
                game_active = False

            # Recycle enemies if they leave the screen
            if (enemy.direction == 'right' and enemy.rect.left >= display_size[0]) or \
                    (enemy.direction == 'left' and enemy.rect.right <= 0):
                enemies.remove(enemy)
                enemies.append(enemy_generator(1)[0])

        disp_score()

    # Game over screen
    else:
        screen.fill((124, 159, 192))
        screen.blit(player_stand, player_stand_rect)

        if key_states[pygame.K_SPACE]:
            game_active = True
            enemies = enemy_generator()
            player1.rect.midbottom = (display_size[0]/2, ground)
            st_time = pygame.time.get_ticks()
            tm.sleep(0.3)

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
