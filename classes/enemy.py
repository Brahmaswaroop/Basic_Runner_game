"""
This module is associated with the enemy of the game.

Features:
1. Enemy sprite creation handled by the Enemy class.
2. EnemyProcessing class provides:
   - Enemy generator to spawn a specified number of enemies.
   - Movement and behavior control for enemies, including gravity and jumping.
   - Collision detection to check interactions with the player.
   - Recycling mechanism to reuse enemies moving out of bounds.

Classes:
1. Enemy: Defines individual enemy attributes and rendering.
2. EnemyProcessing: Manages enemy creation, movement, and interactions.

Dependencies:
- pygame
- random
- motion (local module)
"""
import os

import pygame
import random
from .motion import Motion

class Enemy(Motion):
    def __init__(self, screen, character, spawn_position: tuple):
        super().__init__(spawn_position[1])
        self.screen = screen
        self.speed = 7
        self.default_pos = spawn_position
        self.direction = None
        self.jump_strength = 0
        self.jump_interval = 0
        self.character = character
        self.size = (70, 70)
        self.char_sprites = os.listdir(f"game_files/Enemy_skins/{character}")
        self.sprite_index = 0

        try:
            # Load the original image
            image_path = f"game_files/Enemy_skins/{self.character}/{self.char_sprites[-1]}"
            original_image = pygame.image.load(image_path).convert_alpha()
            self.surf = pygame.transform.scale(original_image, self.size)

        except FileNotFoundError:
            self.surf = pygame.Surface(self.size, pygame.SRCALPHA)  # Transparent placeholder
            self.surf.fill("black")

        # Set the rectangle position to align the enemy properly
        self.rect = self.surf.get_rect(midbottom=(self.default_pos[0], self.default_pos[1]))

    def draw(self):
        self.screen.blit(self.surf, self.rect)

class EnemyProcessing:
    def __init__(self, screen, ground_pos):
        self.screen = screen
        self.display_size = screen.get_size()
        self.ground_pos = ground_pos

    def enemy_generator(self, difficulty: dict, enemy_count_defined=0):
        enemy_skins = ['dog_1', 'bird_1']
        enemy_pos_direction = [(0, "right"), (self.display_size[0], "left")]
        enemy_list = []
        enemy_count = enemy_count_defined if enemy_count_defined else difficulty["enemy_count"]

        for enemy in range(enemy_count):
            character = random.choice(enemy_skins)
            ran_enemy_direction = random.choice(enemy_pos_direction)
            if 'bird' in character:
                ran_enemy_pos = random.randint(200, self.ground_pos-60)
                enemy = Enemy(self.screen, character, (ran_enemy_direction[0], ran_enemy_pos))
                enemy.jump_strength = -(random.randint(difficulty["enemy_jump_strength"]-5, difficulty[
                    "enemy_jump_strength"]))
            else:
                enemy = Enemy(self.screen, character, (ran_enemy_direction[0], self.ground_pos))

            enemy.direction = ran_enemy_direction[1]
            enemy.speed = random.randint(int(difficulty['enemy_max_speed'])-5, difficulty["enemy_max_speed"])

            enemy.jump_interval = random.uniform(0, difficulty["enemy_jump_rate"])
            enemy.jump_timer = pygame.USEREVENT + 1
            pygame.time.set_timer(enemy.jump_timer, int(enemy.jump_interval * 10000))
            enemy_list.append(enemy)
        return enemy_list

    def collision_detected(self, enemies: list, player_rect):
        """
        Process enemy collisions
                    enemies
        :param enemies : List of active enemy objects.
        :param player_rect : Player's rectangle for collision checking.:
        :return bool: False if a collision occurs with the player; True otherwise.
        """
        collision_detected = False
        for enemy in enemies:
            # Check for collisions with the player
            if player_rect.colliderect(enemy.rect):
                collision_detected = True
        return not collision_detected

    def enemy_movement(self, enemies: list, difficulty):

        """
        Processes enemy movement and recycling.

        Args:
            :param enemies:
            :param difficulty:

        """
        remaining_enemies = []  # To track enemies still on-screen

        for enemy in enemies:
            # Enemy actions: movement, gravity, jumping
            enemy.move_horizontal(enemy.direction)
            enemy.moving_animation(enemy.direction, entity="enemy")
            for event in pygame.event.get():
                if event.type == enemy.jump_timer:
                    enemy.jump(jump_height=enemy.jump_strength)

            enemy.apply_gravity()
            enemy.draw()

            # Recycle enemy if it leaves the screen; otherwise, keep it
            if (enemy.direction == 'right' and enemy.rect.left >= self.display_size[0]) or \
                    (enemy.direction == 'left' and enemy.rect.right <= 0):
                # Replace with a new enemy
                remaining_enemies.append(self.enemy_generator(difficulty, enemy_count_defined=1)[0])
            else:
                remaining_enemies.append(enemy)

        # Update the original enemy list
        enemies[:] = remaining_enemies
