import pygame
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):

    def __init__(self, screen_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('SPRITE_FINAL/idle_1.png')
        self.speed = 5
        self.rect = self.image.get_rect()
        self.rect.x = (screen_size.get_width() / 2) - (self.image.get_width() / 2)
        self.rect.y = (screen_size.get_height() / 2) - (self.image.get_height() / 2)
        self.attack = 0
        self.rapid = 60
        self.range = 0
        self.isMoving = False
        self.energy = 0
        self.direction = "Right"
        self.run = [
            pygame.image.load("SPRITE_FINAL/run_1.png"), pygame.image.load("SPRITE_FINAL/run_2.png"),
            pygame.image.load("SPRITE_FINAL/run_3.png"), pygame.image.load("SPRITE_FINAL/run_4.png")
        ]
        self.counter = 0

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
            self.isMoving = True
            self.direction = "Left"
            self.image = self.run[self.counter]
            self.counter = (self.counter + 1) % len(self.run)
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect.x -= self.speed
        elif keys[pygame.K_d]:
            self.isMoving = True
            self.direction = "Right"
            self.rect.x += self.speed
            self.image = self.run[self.counter]
            self.counter = (self.counter + 1) % len(self.run)
        else:
            self.isMoving = False
            if self.direction == "Right":
                self.image = pygame.image.load('SPRITE_FINAL/idle_1.png')
            elif self.direction == "Left":
                self.image = pygame.image.load('SPRITE_FINAL/idle_1.png')
                self.image = pygame.transform.flip(self.image, True, False)




