from motion import Motion
import pygame

class Player(Motion):
    def __init__(self, display_size, ground):
        super().__init__()
        self.speed = 7
        try:
            self.surf = pygame.image.load("game_files/charSkin1.png").convert_alpha()
        except FileNotFoundError:
            self.surf = pygame.Surface((100, 100))
            self.surf.fill("black")
        self.rect = self.surf.get_rect(midbottom=(display_size[0]/2, ground))

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
