"""
This module is associated with the enemy of the game.
It includes:

Enemy sprite creation is done using the Enemy class.

Enemy processing class have functions to interact with the enemy rect like:
Enemy generator to generate n number of enemies.
Enemy Movement is used to make the rect move.
"""

import pygame
import random
from .motion import Motion

class _Enemy(Motion):
    def __init__(self, screen, color, spawn_position: tuple):
        super().__init__(spawn_position[1])
        self.screen = screen
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

    def draw(self):
        self.screen.blit(self.surf, self.rect)


class EnemyProcessing:
    def __init__(self, screen, ground_pos):
        self.screen = screen
        self.display_size = screen.get_size()
        self.ground_pos = ground_pos

    def enemy_generator(self, difficulty: dict, enemy_count_defined=0):
        enemy_skins = ['green', 'blue', 'red']
        enemy_pos_direction = [(0, "right"), (self.display_size[0], "left")]
        enemy_list = []
        enemy_count = enemy_count_defined if enemy_count_defined else difficulty["enemy_count"]

        for enemy in range(enemy_count):
            ran_enemy_color = random.choice(enemy_skins)
            ran_enemy_direction = random.choice(enemy_pos_direction)
            enemy = _Enemy(self.screen, ran_enemy_color, (ran_enemy_direction[0], self.ground_pos))
            enemy.direction = ran_enemy_direction[1]
            enemy.speed = random.randint(int(difficulty['enemy_max_speed'])-5, difficulty["enemy_max_speed"])
            enemy.jump_strength = random.randint(difficulty["enemy_jump_strength"]-5, difficulty[
                "enemy_jump_strength"])
            enemy.jump_interval = random.uniform(1, difficulty["enemy_jump_rate"])
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
            enemies (list): List of active enemy objects.

        """
        remaining_enemies = []  # To track enemies still on-screen

        for enemy in enemies:
            # Enemy actions: movement, gravity, jumping
            enemy.move_horizontal(enemy.direction)
            enemy.apply_gravity()
            enemy.jump(interval=enemy.jump_interval, jump_height=enemy.jump_strength)
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
