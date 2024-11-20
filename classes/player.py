from .motion import Motion
import pygame

class Player(Motion):
    def __init__(self, screen, ground):
        super().__init__(ground)
        self.speed = 7
        self.screen = screen
        try:
            self.surf = pygame.image.load("game_files/charSkin1.png").convert_alpha()
        except FileNotFoundError:
            self.surf = pygame.Surface((100, 100))
            self.surf.fill("black")

        self.rect = self.surf.get_rect(midbottom=(screen.get_size()[0]/2, ground))
        self.rect.move

    def draw(self):
        self.screen.blit(self.surf, self.rect)
