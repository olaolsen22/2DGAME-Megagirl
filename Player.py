import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, screen_size, y, fps, floor_height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/player/idle_1.png')
        self.image_idle = pygame.image.load('sprites/player/idle_1.png')
        self.speed = 5
        self.screen_size = screen_size
        self.floor_height = floor_height
        self.rect = self.image.get_rect()
        self.rect.x = (screen_size.get_width() / 16)
        self.rect.y = y
        self.original_y = y
        self.hit_points = 10
        self.score = 0

        self.attack_level = 1
        self.rapid_level = 1
        self.attack = 5
        self.rapid = 2

        self.last = 0
        self.isMoving = False
        self.direction = "Right"
        self.images_run = [pygame.Surface.convert_alpha(pygame.image.load("sprites/player/run_1.png")),
                           pygame.Surface.convert_alpha(pygame.image.load("sprites/player/run_2.png")),
                           pygame.Surface.convert_alpha(pygame.image.load("sprites/player/run_3.png")),
                           pygame.Surface.convert_alpha(pygame.image.load("sprites/player/run_4.png"))]
        self.images_run_attack = [pygame.Surface.convert_alpha(pygame.image.load("sprites/player/runAttack_1.png")),
                                  pygame.Surface.convert_alpha(pygame.image.load("sprites/player/runAttack_2.png")),
                                  pygame.Surface.convert_alpha(pygame.image.load("sprites/player/runAttack_3.png")),
                                  pygame.Surface.convert_alpha(pygame.image.load("sprites/player/runAttack_4.png"))]
        self.image_idle_attack = pygame.Surface.convert_alpha(pygame.image.load("sprites/player/idle_2.png"))
        self.image_jump = [pygame.Surface.convert_alpha(pygame.image.load("sprites/player/jump_1.png")),
                           pygame.Surface.convert_alpha(pygame.image.load("sprites/player/jump_2.png"))]
        self.image_jump_attack = [pygame.Surface.convert_alpha(pygame.image.load("sprites/player/jumpAttack_1.png")),
                                  pygame.Surface.convert_alpha(pygame.image.load("sprites/player/jumpAttack_2.png"))]
        self.frame = 0
        self.run_counter = [0, 0]
        self.fps = fps
        self.jumping = False
        self.jump_direction = 'Up'
        self.jump_fight = 0
        self.jump_audio_playing = False
        self.not_moving = False
        self.is_hurting = False
        self.hurt_cooldown = 0

    def update_stats(self, attack, rapid):
        self.attack_level = attack
        self.rapid_level = rapid
        self.attack = attack * 2
        self.rapid = rapid * 2

    def player_hurt(self):
        if self.hurt_cooldown == 0:
            pygame.mixer.Channel(5).play(pygame.mixer.Sound('sound/player/sfx-hurt1.wav'))
            self.hit_points -= 1
            self.hurt_cooldown += 1
        else:
            image_temp = self.image.copy()
            sprite_temp = pygame.PixelArray(image_temp)
            sprite_temp.replace((3, 104, 216), (255, 255, 255), 0.1)
            sprite_temp.replace((40, 64, 132), (255, 255, 255), 0.1)
            sprite_temp.replace((132, 224, 248), (255, 255, 255), 0.1)
            sprite_temp.replace((124, 128, 124), (255, 255, 255), 0.1)
            sprite_temp.replace((244, 172, 128), (255, 255, 255), 0.1)
            sprite_temp.replace((108, 73, 66), (255, 255, 255), 0.1)
            sprite_temp.replace((208, 160, 104), (255, 255, 255), 0.1)

            self.image = image_temp
            if self.hurt_cooldown == self.fps * 2:
                self.is_hurting = False
                self.hurt_cooldown = 0
            else:
                self.hurt_cooldown += 1

    def jump(self, keys):
        if not self.jump_audio_playing:
            pygame.mixer.Channel(2).play(pygame.mixer.Sound('sound/player/sfx-jump1.wav'))
            self.jump_audio_playing = True

        if self.not_moving:
            if self.jump_direction == 'Up':
                if keys[pygame.K_a]:
                    self.image = self.image_jump_attack[0]
                else:
                    self.image = self.image_jump[0]
                if self.rect.y <= self.screen_size.get_height() / 2.5:
                    self.jump_direction = 'Down'
                self.rect.y -= self.speed
            elif self.jump_direction == 'Down':
                if keys[pygame.K_a]:
                    self.image = self.image_jump_attack[1]
                else:
                    self.image = self.image_jump[1]
                if self.rect.y == self.original_y:
                    self.image = self.image_idle
                    self.rect.y = self.original_y
                    self.jumping = False
                    self.jump_direction = 'Up'
                    pygame.mixer.Channel(3).play(pygame.mixer.Sound('sound/player/sfx-land1.wav'))
                else:
                    self.rect.y += self.speed
        elif self.direction == 'Right':
            if self.jump_direction == 'Up':
                if keys[pygame.K_a]:
                    self.image = self.image_jump_attack[0]
                else:
                    self.image = self.image_jump[0]
                if self.rect.y <= self.screen_size.get_height() / 2.5:
                    self.jump_direction = 'Down'
                if self.rect.x < self.screen_size.get_width() - self.image.get_width():
                    self.rect.x += self.speed
                self.rect.y -= self.speed
            elif self.jump_direction == 'Down':
                if keys[pygame.K_a]:
                    self.image = self.image_jump_attack[1]
                else:
                    self.image = self.image_jump[1]
                if self.rect.y == self.original_y:
                    self.rect.y = self.original_y
                    self.jumping = False
                    self.jump_direction = 'Up'
                    pygame.mixer.Channel(3).play(pygame.mixer.Sound('sound/player/sfx-land1.wav'))
                else:
                    if self.rect.x < self.screen_size.get_width() - self.image.get_width():
                        self.rect.x += self.speed
                    self.rect.y += self.speed
        elif self.direction == 'Left':
            if self.jump_direction == 'Up':
                if keys[pygame.K_a]:
                    self.image = pygame.transform.flip(self.image_jump_attack[0], True, False)
                else:
                    self.image = pygame.transform.flip(self.image_jump[0], True, False)
                if self.rect.y <= self.screen_size.get_height() / 2.5:
                    self.jump_direction = 'Down'
                if self.rect.x > 0:
                    self.rect.x -= self.speed
                self.rect.y -= self.speed
            elif self.jump_direction == 'Down':
                if keys[pygame.K_a]:
                    self.image = pygame.transform.flip(self.image_jump_attack[1], True, False)
                else:
                    self.image = pygame.transform.flip(self.image_jump[1], True, False)
                if self.rect.y == self.original_y:
                    self.rect.y = self.original_y
                    self.jumping = False
                    self.jump_direction = 'Up'
                    pygame.mixer.Channel(3).play(pygame.mixer.Sound('sound/player/sfx-land1.wav'))
                else:
                    if self.rect.x > 0:
                        self.rect.x -= self.speed
                    self.rect.y += self.speed

    def update(self, keys, mouse):

        if self.is_hurting:
            self.player_hurt()

        if keys[pygame.K_LCTRL]:
            self.speed = 8
        else:
            self.speed = 5
        if not self.jumping:
            if keys[pygame.K_LEFT] and self.rect.x > 0:
                if self.fps / len(self.images_run) == self.run_counter[0]:
                    if keys[pygame.K_a]:
                        self.image = pygame.transform.flip(self.images_run_attack[self.run_counter[1]], True, False)
                    else:
                        self.image = pygame.transform.flip(self.images_run[self.run_counter[1]], True, False)
                    if self.run_counter[1] % 2 == 0:
                        pygame.mixer.Channel(2).play(pygame.mixer.Sound('sound/player/sfx-walk1.wav'))
                    if self.run_counter[1] >= len(self.images_run) - 1:
                        self.run_counter[1] = 0
                    else:
                        self.run_counter[1] += 1
                    self.run_counter[0] = 0
                self.direction = 'Left'
                self.rect.x -= self.speed
                self.run_counter[0] += 3
                self.not_moving = False
            elif keys[pygame.K_RIGHT] and self.rect.x < self.screen_size.get_width() - self.image.get_width():
                if self.fps / len(self.images_run) == self.run_counter[0]:
                    if self.run_counter[1] % 2 == 0:
                        pygame.mixer.Channel(2).play(pygame.mixer.Sound('sound/player/sfx-walk1.wav'))
                    if keys[pygame.K_a]:
                        self.image = self.images_run_attack[self.run_counter[1]]
                    else:
                        self.image = self.images_run[self.run_counter[1]]
                    if self.run_counter[1] >= len(self.images_run) - 1:
                        self.run_counter[1] = 0
                    else:
                        self.run_counter[1] += 1
                    self.run_counter[0] = 0
                self.direction = 'Right'
                self.rect.x += self.speed
                self.run_counter[0] += 3
                self.not_moving = False
            else:
                self.not_moving = True
                self.run_counter[1] = 0
                self.run_counter[0] = 0
                if self.direction == 'Left':
                    if keys[pygame.K_a]:
                        self.image = pygame.transform.flip(self.image_idle_attack, True, False)
                    else:
                        self.image = pygame.transform.flip(self.image_idle, True, False)
                elif self.direction == 'Right':
                    if keys[pygame.K_a]:
                        self.image = self.image_idle_attack
                    else:
                        self.image = self.image_idle
            if keys[pygame.K_SPACE]:
                self.jumping = True
                self.jump_audio_playing = False

        # JUMPING MECHANIC

        elif self.jumping:
            self.jump(keys)
