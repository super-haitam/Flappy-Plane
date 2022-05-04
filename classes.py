from settings import *
import random
import pygame


class Bg:
    def __init__(self, x):
        self.image = pygame.transform.scale(images_dict["background.png"],
                                            (images_dict["background.png"].get_width(), HEIGHT))
        self.rect = self.image.get_rect(topleft=(x, 0))

    def manage_pos(self):
        self.rect.x -= 10
        if self.rect.x <= -1 * self.rect.w:
            self.rect.x = self.rect.w

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Ground:
    def __init__(self, x):
        self.image = images_dict["ground.png"]
        self.rect = self.image.get_rect(topleft=(x, HEIGHT-self.image.get_height()))

    def manage_pos(self):
        self.rect.x -= 10
        if self.rect.x <= -1 * self.rect.w:
            self.rect.x = self.rect.w

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Plane:
    def __init__(self):
        factor = 0.7
        width, height = images_dict[f"red0.png"].get_width() * factor, images_dict[f"red0.png"].get_height() * factor
        self.images = [pygame.transform.scale(images_dict[f"red{i}.png"], (width, height)) for i in range(3)]

        self.origin_y = HEIGHT/2

        self.image = self.images[0]
        self.image_count = 0
        self.rect = self.image.get_rect(centerx=WIDTH/4, centery=self.origin_y)

        self.reset()

        self.score = 0
        self.high_score = 0

    def reset(self):
        self.angle = 0
        self.gravity = 0

        self.is_jump = False
        self.reset_jump_count()

    def reset_jump_count(self):
        self.jump_count = -10

    def jump(self):
        self.is_jump = True
        self.reset_jump_count()
        self.angle = 0

    def handle_movement(self):
        if self.is_jump:
            self.rect.y += self.jump_count
            self.jump_count += 1
            self.gravity = 0
            self.angle += 1
        else:
            self.angle -= 1

        self.apply_gravity()

        if self.jump_count == 0:
            self.is_jump = False
            self.reset_jump_count()

        self.image_count += .5
        if self.image_count == 3:
            self.image_count = 0
        self.image = self.images[int(self.image_count)]

        self.image = pygame.transform.rotate(self.image, self.angle)

    def apply_gravity(self):
        self.gravity += .2
        self.rect.y += self.gravity

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Obstacle:
    def __init__(self, x):
        self.images = [images_dict[f"{i}.png"] for i in range(2)]
        self.x = x

        self.select_rand_image()

    def select_rand_image(self):
        self.image = pygame.transform.rotate(self.images[random.randint(0, 1)], 180)
        reverse = random.choice([True, False])
        if not reverse:
            self.rect = self.image.get_rect(x=self.x, y=0)
        else:
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_rect(x=self.x, y=0)
            self.rect.y = HEIGHT - self.rect.h

    def manage_pos(self):
        self.rect.x -= 10
        if self.rect.x <= -1 * self.rect.w:
            self.select_rand_image()
            self.rect.x = WIDTH

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
