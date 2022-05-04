import random
import pygame
import os

WIDTH, HEIGHT = 480, 620

# Colors
PSEUDO_WHITE = tuple(random.randint(200, 255) for _ in range(3))
BLACK = (0, 0, 0)

random_color = lambda a, b: tuple(random.randint(a, b) for _ in range(3))

# Images dictionary
images_dict = {}
for folder in os.listdir("assets"):
    for image in os.listdir(f"assets/{folder}"):
        images_dict[image] = pygame.image.load(f"assets/{folder}/{image}")
