from motion import Motion
import pygame

class Enemy(Motion):
    def __init__(self, color, pos, ground):
        super().__init__()
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
