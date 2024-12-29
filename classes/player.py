import pygame
import os
from .motion import Motion

class Player(Motion):
    def __init__(self, screen, ground, character: str):
        super().__init__(ground)
        self.direction = None
        self.speed = 6
        self.sprite_index = 0
        self.character = character
        self.char_sprites = os.listdir(f"game_files/Character_skins/{character}")
        self.screen = screen
        try:
            self.image = f"game_files/Character_skins/{character}/{self.char_sprites[-1]}"
            self.surf = pygame.image.load(self.image).convert_alpha()
        except FileNotFoundError:
            self.surf = pygame.Surface((100, 100))
            self.surf.fill("black")
        self.surf = pygame.transform.scale(self.surf, (100, 150))
        self.rect = self.surf.get_rect(midbottom=(screen.get_size()[0]/2, ground))

    def draw(self):
        self.screen.blit(self.surf, self.rect)
