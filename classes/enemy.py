from .motion import Motion
import random
import pygame

class _Enemy(Motion):
    def __init__(self, color, spawn_position:tuple):
        super().__init__(spawn_position[1])
        self.speed = 7
        self.default_pos = spawn_position
        self.direction = None
        self.jump_strength = 0
        self.jump_interval = 0
        try:
            self.surf = pygame.image.load("game_files/enemySkin1.png").convert_alpha()
        except FileNotFoundError:
            self.surf = pygame.Surface((50, 50))
            self.surf.fill(color)
        self.rect = self.surf.get_rect(midbottom=(self.default_pos[0], self.default_pos[1]))

    def draw(self, screen):
        screen.blit(self.surf, self.rect)

class Enemy_processing:
    def __init__(self, screen, display_size:tuple, ground_pos):
        self.screen = screen
        self.display_size = display_size
        self.ground_pos = ground_pos

    def enemy_generator(self, num_of_enemies):
        enemy_skins = ['green', 'blue', 'red']
        enemy_pos_direction = [(0, "right"), (self.display_size[0], "left")]
        enemy_list = []

        for enmy in range(num_of_enemies):
            ran_enemy_color = random.choice(enemy_skins)
            ran_enemy_direction = random.choice(enemy_pos_direction)

            enmy = _Enemy(ran_enemy_color, (ran_enemy_direction[0], self.ground_pos))
            enmy.direction = ran_enemy_direction[1]
            enmy.speed = random.randint(4, 15)
            enmy.jump_strength = random.randint(10, 20)
            enmy.jump_interval = random.uniform(1, 3)
            enemy_list.append(enmy)

        return enemy_list

    def enemy_movement(self, enemies:list, player_rect):
        # Processing enemies
        for enemy in enemies:
            # Enemy movement and jumping
            enemy.move_horizontal(enemy.direction)
            enemy.apply_gravity(enemy.rect)
            enemy.jump(interval=enemy.jump_interval, jump_height=enemy.jump_strength)
            enemy.draw(self.screen)

            # Recycle enemies if they leave the screen
            if (enemy.direction == 'right' and enemy.rect.left >= self.display_size[0]) or \
                    (enemy.direction == 'left' and enemy.rect.right <= 0):
                enemies.remove(enemy)
                enemies.append(self.enemy_generator(1)[0])

            # Check for collisions
            if player_rect.colliderect(enemy.rect):
                return False
        return True
    
    