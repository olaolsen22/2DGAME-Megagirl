import pygame
from random import randint

class Enemy(pygame.sprite.Sprite):

    def __init__(self, enemy_type, screen_size):
        pygame.sprite.Sprite.__init__(self)
        self.hit_points = 0
        self.enemy_type = 0
        self.image = pygame.image.load(self.get_enemy(enemy_type))
        self.image_damage = pygame.image.load('sprites/enemies/damage_taken_1.png')
        self.speed = .25
        self.rect = self.image.get_rect()
        self.rect.x = randint(screen_size[0] / 4, screen_size[0])
        self.rect.y = (screen_size[1] / 1.4)
        self.behavior_steps = randint(int(screen_size[0] / 6), int(screen_size[0] / 2))
        self.behavior_count = 0

    def get_enemy(self, enemy_type):
        if enemy_type == 0:
            self.hit_points = 100
            return 'sprites/enemies/basic_1.png'

    def take_damage(self, damage):
        if self.hit_points < 0:
            pass
        else:
            print(self.hit_points)
            self.hit_points -= damage

    def behavior(self):
        if self.enemy_type == 0:
            if self.rect.x <= self.behavior_steps:
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed

    def update(self, *args):
        self.behavior()

