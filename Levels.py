import pygame
from random import randint


class Level(pygame.sprite.Sprite):
    def __init__(self, screen_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/level/floor_1.png')
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = self.image.get_rect().size[1] - screen_size[1]


class Platform(pygame.sprite.Sprite):
    def __init__(self, screen_size):
        pygame.sprite.Sprite.__init__(self)
        self.screen_size = screen_size
        self.image = pygame.image.load('sprites/level/platform.png')
        self.image = pygame.Surface.convert(self.image)
        self.rect = self.image.get_rect()
        self.rect.height = 200
        self.rect.x = randint(0,  self.screen_size[0] - self.image.get_width())
        self.rect.y = int(self.screen_size[1] / 1.75)

    def change(self, is_not_first):
        if is_not_first:
            self.rect.x = randint(0, self.screen_size[0] - self.image.get_width())
            self.rect.y = randint(int(self.screen_size[1] / 4), int(self.screen_size[1] / 1.75))



