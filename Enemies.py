import pygame
from random import randint

class Enemy(pygame.sprite.Sprite):

    def __init__(self, enemy_type, screen_size):
        self.image = pygame.image.load(self.get_enemy(enemy_type))
        self.speed = 5
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, screen_size[0])
        self.rect.y = 250

    def get_enemy(self, enemy_type):
        if enemy_type == 0:
            return 'sprites/enemies/basic_1.png'

    def update(self, *args):
        self.x -= self.speed