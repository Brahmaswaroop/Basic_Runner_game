import pygame
import os
from .motion import Motion

class Player(Motion):
    def __init__(self, screen, ground, character: str):
        super().__init__(ground)
        self.direction = None
        self.speed = 8
        self.default_pos = (screen.get_size()[0]/2, ground)
        self.sprite_index = 0
        self.character = character
        self.size = (100, 150)
        self.char_sprites = os.listdir(f"game_files/Character_skins/{character}")
        self.screen = screen
        try:
            self.image = f"game_files/Character_skins/{character}/{self.char_sprites[-1]}"
            self.surf = pygame.image.load(self.image).convert_alpha()
            self.surf = pygame.transform.smoothscale(self.surf, self.size)
        except FileNotFoundError:
            self.surf = pygame.Surface(self.size)
            self.surf.fill("black")
        self.rect = self.surf.get_rect(midbottom=self.default_pos)

    def draw(self):
        self.screen.blit(self.surf, self.rect)
