import time as tm
import pygame


class Motion:
    def __init__(self, ground):
        self.screen = None
        self.image = None
        self.surf = None
        self.rect = None
        self.character_folder = None
        self.character = None
        self.size = None
        self.char_sprites = None
        self.sprite_index = None
        self.direction = None
        self.vertical_displacement = 0  # For vertical (Y-axis) motion due to gravity or jump
        self.gravity_force = 0.7  # Gravity effect value
        self.speed = 0
        self.last_jump_time = 0
        self.ground = ground

    def apply_gravity(self):
        # Apply gravity effect on vertical displacement if player is in air
        if self.rect.bottom < self.ground:
            self.vertical_displacement -= self.gravity_force
            self.rect.bottom -= self.vertical_displacement
        # Ensure the player does not fall below ground level
        else:
            self.rect.bottom = self.ground
            self.vertical_displacement = 0

    def jump(self, interval=0, jump_height=16):
        # Check if player is on the ground and can jump
        if 'Character' in self.character:
            if self.rect.bottom == self.ground and tm.time() - self.last_jump_time >= interval:
                self.vertical_displacement = jump_height
                self.rect.bottom -= self.vertical_displacement
                self.last_jump_time = tm.time()
        else:
            if tm.time() - self.last_jump_time >= interval:
                self.vertical_displacement = jump_height
                self.rect.bottom -= self.vertical_displacement
                self.last_jump_time = tm.time()

    def move_horizontal(self, direction, border=False):
        # To prevent the rect to go beyond the window border
        if border:
            self.rect.clamp_ip(self.screen.get_rect())
        # Move left or right on the X-axis
        if direction == "left":
            self.rect.move_ip(-self.speed, 0)
        elif direction == "right":
            self.rect.move_ip(self.speed, 0)

    def moving_animation(self, direction="stand", entity="player"):
        if entity == "player":
            self.character_folder = "Character_skins"
            if self.sprite_index >= 3:
                self.sprite_index = 0

        elif entity == "enemy":
            self.character_folder = "Enemy_skins"
            if self.sprite_index >= 5:
                self.sprite_index = 0

        try:
            if direction == "stand":
                self.image = f"game_files/{self.character_folder}/{self.character}/{self.char_sprites[-1]}"
                self.sprite_index = 0
            else:
                self.direction = direction
                self.image = f"game_files/{self.character_folder}/{self.character}/{self.char_sprites[int(self.sprite_index)]}"
                self.sprite_index += 0.1 if entity == 'player' else 0.16

            if self.rect.bottom < self.ground and entity == 'player':
                self.image = f"game_files/{self.character_folder}/{self.character}/{self.char_sprites[1]}"

            self.surf = pygame.image.load(self.image).convert_alpha()
            if self.direction == "left":
                self.surf = pygame.transform.flip(self.surf, True, False)
            self.surf = pygame.transform.scale(self.surf, self.size)
            self.draw()

        except FileNotFoundError:
            print("FILE NOT FOUND!")
