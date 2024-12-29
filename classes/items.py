import pygame
import random
from .data_loader import load_fruit_data

class Fruit:
    def __init__(self, screen):
        self.screen = screen
        self.image = None
        self.surf = None
        self.rect = None
        self.fall_rate = 0
        self.pos = 0
        self.value = 0

    def draw(self):
        self.screen.blit(self.surf, self.rect)

class FruitProcessing:
    def __init__(self, screen):
        self.screen = screen

    def fruit_generator(self, interval):
        fruit_data_list = load_fruit_data()
        fruit_data = random.choice(list(fruit_data_list))
        fruit = Fruit(self.screen)
        fruit.fall_rate = fruit_data_list[fruit_data]["fall_rate"]
        fruit.image = fruit_data_list[fruit_data]["image"]
        fruit.value = fruit_data_list[fruit_data]["value"]
        fruit.surf = pygame.image.load(fruit.image)
        fruit.surf = pygame.transform.scale(fruit.surf, (30, 30))
        fruit.pos = random.randint(15, fruit.screen.get_size()[0]-15)
        fruit.rect = fruit.surf.get_rect(midbottom=(fruit.pos, 0))
        fruit.fruit_interval = pygame.USEREVENT + 1
        pygame.time.set_timer(fruit.fruit_interval, interval*1000)
        return fruit

    def fruit_falling(self, fruit_list):
        for fruit in fruit_list:
            for event in pygame.event.get():
                if event.type == fruit.fruit_interval:
                    if fruit.rect.top >= fruit.screen.get_size()[1]:
                        fruit_list.remove(fruit)
                    fruit.rect.bottom += fruit.fall_rate
            fruit.draw()
