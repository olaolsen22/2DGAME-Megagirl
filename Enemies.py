import pygame
from random import randint


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, screen_size, fps, floor_height):
        pygame.sprite.Sprite.__init__(self)
        self.screen_size = screen_size
        self.hit_points = 0
        self.damage = 0
        self.enemy_type = enemy_type
        self.image_animate = []
        self.image = pygame.image.load(self.get_enemy(enemy_type))
        self.speed = 2
        self.rect = self.image.get_rect()
        self.rect.x = randint(screen_size[0] / 4, screen_size[0])
        self.rect.y = (screen_size[1] -  self.image.get_height()) - floor_height
        self.behavior_steps = randint(int(screen_size[0] / 6), int(screen_size[0] / 2))
        self.behavior_count = 0
        self.go_left = True
        self.go_right = False
        self.fps = fps
        self.animation_counter = [0, randint(0, len(self.image_animate) - 1)]

    def get_enemy(self, enemy_type):
        if enemy_type == 0:
            self.hit_points = 50
            self.damage = 5
            self.image_animate.append(pygame.image.load('sprites/enemies/basic_1.png'))
            self.image_animate.append(pygame.image.load('sprites/enemies/basic_2.png'))
            self.image_animate.append(pygame.image.load('sprites/enemies/basic_3.png'))
            return 'sprites/enemies/basic_1.png'

    def animate_death(self):
        pass

    def take_damage(self, damage):
        if self.hit_points < 0:
            pass
        else:
            self.hit_points -= damage

    def behavior(self):
        if self.enemy_type == 0:
            if self.go_left:
                if self.fps / len(self.image_animate) == self.animation_counter[0]:
                    print((self.fps / len(self.image_animate)))
                    self.image = self.image_animate[self.animation_counter[1]]
                    self.animation_counter[1] += 1
                    self.animation_counter[0] = 0
                if self.rect.x <= self.behavior_steps + self.image.get_width():
                    self.go_right = True
                    self.go_left = False
                self.rect.x -= self.speed
                self.animation_counter[0] += 1
            elif self.go_right:
                if self.fps / len(self.image_animate) == self.animation_counter[0]:
                    print((self.fps / len(self.image_animate)))
                    self.image = self.image_animate[self.animation_counter[1]]
                    self.animation_counter[1] += 1
                    self.animation_counter[0] = 0
                if self.rect.x >= self.screen_size[0] - (self.image.get_width() * 2):
                    self.go_right = False
                    self.go_left = True
                self.rect.x += self.speed
                self.animation_counter[0] += 1

        if self.animation_counter[1] == len(self.image_animate):
            self.animation_counter[1] = 0

    def update(self, *args):
        self.behavior()

