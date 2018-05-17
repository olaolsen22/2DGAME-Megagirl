import pygame
from random import randint
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, screen_size, fps, floor_height):
        pygame.sprite.Sprite.__init__(self)
        self.screen_size = screen_size
        self.hit_points = 0
        self.damage = 0
        self.enemy_type = enemy_type
        self.image_animate = []
        self.score_hit = 0
        self.score_kill = 0
        self.image = pygame.image.load(self.get_enemy(enemy_type))
        self.image_death = [pygame.Surface.convert_alpha(pygame.image.load('sprites/enemies/death.png')),
                            pygame.Surface.convert_alpha(pygame.image.load('sprites/enemies/death_1.png')),
                            pygame.Surface.convert_alpha(pygame.image.load('sprites/enemies/death_2.png')),
                            pygame.Surface.convert_alpha(pygame.image.load('sprites/enemies/death_3.png')),
                            pygame.Surface.convert_alpha(pygame.image.load('sprites/enemies/death_4.png'))]
        self.speed = 2

        self.rect = self.image.get_rect()
        self.rect.x = randint(screen_size[0] / 4, screen_size[0])
        self.rect.y = (screen_size[1] - self.image.get_height()) - floor_height
        self.behavior_steps = randint(int(screen_size[0] / 6), int(screen_size[0] / 2))
        self.behavior_count = 0
        self.go_left = True
        self.go_right = False
        self.fps = fps
        self.animation_counter = [0, randint(0, len(self.image_animate) - 1)]
        self.death_counter = [0, 0]
        self.is_dead = False
        self.pop = False
        self.shoot_count = [0, 0]
        self.direction = '0'

    def get_direction(self, player_x, player_y):
        self.direction = (-math.degrees(math.atan2(player_x - self.rect.x, player_y - self.rect.y)) + 90)

    def get_enemy(self, enemy_type):
        if enemy_type == 0:
            self.hit_points = 50
            self.score_hit = 1
            self.score_kill = 10
            self.image_animate.append(pygame.Surface.convert_alpha(pygame.image.load('sprites/enemies/basic_1.png')))
            self.image_animate.append(pygame.Surface.convert_alpha(pygame.image.load('sprites/enemies/basic_2.png')))
            self.image_animate.append(pygame.Surface.convert_alpha(pygame.image.load('sprites/enemies/basic_3.png')))
            return 'sprites/enemies/basic_1.png'
        elif enemy_type == 1:
            self.hit_points = 50
            self.score_hit = 2
            self.score_kill = 20
            self.image_animate.append(pygame.Surface.convert_alpha(pygame.image.load('sprites/enemies/ranged_1.png')))
            return'sprites/enemies/ranged_1.png'

    def take_damage(self, damage, screen):
        if not self.hit_points <= 0:
            pygame.mixer.Channel(4).play(pygame.mixer.Sound('sound/enemy/sfx-reaverhurt1.wav'))
            self.hit_points -= damage

    def behavior(self):
        if not self.is_dead:
            if self.enemy_type == 0:
                if self.go_left:
                    if self.fps / len(self.image_animate) == self.animation_counter[0]:
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
        if not self.is_dead:
            self.behavior()
        if self.is_dead:
            if self.death_counter[1] == 0:
                pygame.mixer.Channel(4).play(pygame.mixer.Sound('sound/enemy/sfx-reaverhurt1.wav'))
            if self.death_counter[0] == (self.fps / len(self.image_death)):
                if self.death_counter[1] == len(self.image_death):
                    self.death_counter[1] = 0
                    self.pop = True
                self.image = self.image_death[self.death_counter[1]]
                self.death_counter[1] += 1
                self.death_counter[0] = 0

            self.death_counter[0] += 1
