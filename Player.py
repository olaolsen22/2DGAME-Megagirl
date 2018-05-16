import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, screen_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/player/stand_1.png')

        self.speed = 5
        self.rect = self.image.get_rect()
        self.rect.x = (screen_size.get_width() / 2) - (self.image.get_width() / 2)
        self.rect.y = (screen_size.get_height() / 2) - (self.image.get_height() / 2)
        self.attack = 10
        self.rapid = 4
        self.range = 0
        self.energy = 0

    def update(self, keys):
        if keys[pygame.K_LCTRL]:
            self.speed = 8
        else:
            self.speed = 5
        #if keys[pygame.K_w]:
            #self.rect.y -= self.speed
        #if keys[pygame.K_s]:
            #self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
