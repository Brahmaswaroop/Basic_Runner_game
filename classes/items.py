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
        self.value = 0

    def draw(self):
        self.screen.blit(self.surf, self.rect)

class FruitProcessing:
    def __init__(self, screen):
        self.screen = screen

    def fruit_generator(self):
        fruit_data_list = load_fruit_data()
        fruit_data = random.choice(list(fruit_data_list))
        fruit = Fruit(self.screen)
        fruit.fall_rate = fruit_data_list[fruit_data]["fall_rate"]
        fruit.image = fruit_data_list[fruit_data]["image"]
        fruit.value = fruit_data_list[fruit_data]["value"]

        # Load and scale fruit image
        fruit.surf = pygame.image.load(fruit.image)
        fruit.surf = pygame.transform.scale(fruit.surf, (30, 30))

        fruit.fall_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(fruit.fall_timer, int(fruit.fall_rate * 500))

        # Initial position
        fruit.rect = fruit.surf.get_rect(midbottom=(random.randint(15, fruit.screen.get_size()[0] - 15), 0))
        return [fruit]

    def fruit_score(self, fruit_list, player_rect):
        for fruit in fruit_list:
            if player_rect.colliderect(fruit.rect):
                fruit_list.remove(fruit)
                fruit_list.append(self.fruit_generator()[0])
                return fruit.value
            else:
                return 0

    def fruit_falling(self, fruit_list):
        """Updates fruit positions and removes off-screen fruits."""
        remaining_fruits = []

        for fruit in fruit_list:
            fruit.rect.move_ip(0, fruit.fall_rate)
            fruit.draw()

            # Draw fruit if it is still on-screen
            if fruit.rect.top > fruit.screen.get_size()[1]:
                remaining_fruits.append(self.fruit_generator()[0])
            else:
                remaining_fruits.append(fruit)

        # Update the fruit list
        fruit_list[:] = remaining_fruits
