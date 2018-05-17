import pygame, math


class Projectile(pygame.sprite.Sprite):

    def __init__(self, x, y, direction, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/player/projectiles/1.png')
        self.speed = 5
        self.rect = self.image.get_rect()
        self.rect.x = x + 40
        self.rect.y = y + 40
        self.speed = 8
        self.direction = direction
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('sound/projectile/fire.wav'))

    # def get_direction(self, mouse_pos):
        # return -math.degrees(math.atan2(mouse_pos[0]-self.rect.x, mouse_pos[1]-self.rect.y))+90

    def miss(self):
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('sound/projectile/miss.wav'))

    def update(self):
            if self.direction == 'Right':
                self.rect.x += self.speed
            elif self.direction == 'Left':
                self.rect.x -= self.speed

    def update_enemy(self):
        self.speed = 3
        self.image = pygame.Surface.convert_alpha(pygame.image.load('sprites/enemies/projectiles/ranged.png'))
        self.rect.x += math.cos(math.radians(self.direction)) * self.speed
        self.rect.y += math.sin(math.radians(self.direction)) * self.speed

