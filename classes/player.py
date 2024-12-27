import pygame
import os
from .motion import Motion

class Player(Motion):
    def __init__(self, screen, ground, character: str):
        super().__init__(ground)
        self.speed = 7
        self.sprite_index = 0
        self.character = character
        self.char_sprites = os.listdir(f"game_files/Character_skins/{character}")
        print(self.char_sprites)
        self.screen = screen
        try:
            self.image = f"game_files/Character_skins/{character}/{self.char_sprites[-1]}"
            self.surf = pygame.image.load(self.image).convert_alpha()
        except FileNotFoundError:
            self.surf = pygame.Surface((100, 100))
            self.surf.fill("black")
        self.surf = pygame.transform.scale(self.surf, (150, 200))
        self.rect = self.surf.get_rect(midbottom=(screen.get_size()[0]/2, ground))

    def draw(self):
        self.screen.blit(self.surf, self.rect)

    def animation(self, direction="stop"):
        try:
            if self.sprite_index >= 2:
                self.sprite_index = 0
            elif direction == "right":
                self.image = f"game_files/Character_skins/{self.character}/{self.char_sprites[int(self.sprite_index)]}"
                self.surf = pygame.image.load(self.image).convert_alpha()
                self.sprite_index += 0.2
            elif direction == "left":
                self.image = f"game_files/Character_skins/{self.character}/{self.char_sprites[int(self.sprite_index)]}"
                self.surf = pygame.image.load(self.image).convert_alpha()
                self.surf = pygame.transform.flip(self.surf, True, False)
                self.sprite_index += 0.2
            elif direction == "stop":
                self.image = f"game_files/Character_skins/{self.character}/{self.char_sprites[-1]}"
                self.surf = pygame.image.load(self.image).convert_alpha()
                self.sprite_index = 0
            if self.rect.bottom < self.ground:
                self.image = f"game_files/Character_skins/{self.character}/{self.char_sprites[1]}"
                self.surf = pygame.image.load(self.image).convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (150, 200))
            self.draw()
        except Exception:
            pass
