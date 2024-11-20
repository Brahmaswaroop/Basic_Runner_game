from .motion import Motion
import random
import pygame

class Enemy(Motion):
    def __init__(self, color, pos, ground):
        super().__init__(ground)
        self.speed = 7
        self.default_pos = pos
        self.direction = None
        self.jump_strength = 0
        self.jump_interval = 0
        try:
            self.surf = pygame.image.load("game_files/enemySkin1.png").convert_alpha()
        except FileNotFoundError:
            self.surf = pygame.Surface((50, 50))
            self.surf.fill(color)
        self.rect = self.surf.get_rect(midbottom=(self.default_pos, ground))

    def draw(self, screen):
        screen.blit(self.surf, self.rect)

def enemy_generator(num_enemies=1):
    enemy_colors = ['green', 'blue', 'red']
    enemy_direction = [(display_size[0], "left"), (0, "right")]
    enemies1 = []

    for enemy1 in range(num_enemies):
        ran_enemy_color = random.choice(enemy_colors)
        ran_enemy_direction = random.choice(enemy_direction)

        enemy1 = Enemy(ran_enemy_color, ran_enemy_direction[0], ground)
        enemy1.direction = ran_enemy_direction[1]
        enemy1.speed = random.randint(4, 15)
        enemy1.jump_strength = random.randint(10, 20)
        enemy1.jump_interval = random.uniform(1, 3)
        enemies1.append(enemy1)

    return enemies1

def enemy_processing(self, enemies):
    # Processing enemies
    for enemy in enemies:
        # Enemy movement and jumping
        enemy.move_horizontal(enemy.direction)
        enemy.apply_gravity(enemy.rect)
        enemy.jump(interval=enemy.jump_interval, jump_height=enemy.jump_strength)
        enemy.draw(screen)

        # Check for collisions
        if player1.rect.colliderect(enemy.rect):
            game_active = False

        # Recycle enemies if they leave the screen
        if (enemy.direction == 'right' and enemy.rect.left >= display_size[0]) or \
                (enemy.direction == 'left' and enemy.rect.right <= 0):
            enemies.remove(enemy)
            enemies.append(enemy_generator(1)[0])