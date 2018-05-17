import pygame

pygame.font.init()


class Hud(pygame.sprite.Sprite):
    def __init__(self, screen_size, fps):
        pygame.sprite.Sprite.__init__(self)
        self.image_health = [pygame.image.load('sprites/hud/health_0.png'),
                             pygame.image.load('sprites/hud/health_1.png'),
                             pygame.image.load('sprites/hud/health_2.png'),
                             pygame.image.load('sprites/hud/health_3.png'),
                             pygame.image.load('sprites/hud/health_4.png'),
                             pygame.image.load('sprites/hud/health_5.png'),
                             pygame.image.load('sprites/hud/health_6.png'),
                             pygame.image.load('sprites/hud/health_7.png'),
                             pygame.image.load('sprites/hud/health_8.png'),
                             pygame.image.load('sprites/hud/health_9.png'),
                             pygame.image.load('sprites/hud/health_10.png')]
        self.image_stats = [pygame.image.load('sprites/hud/stat_1.png'),
                            pygame.image.load('sprites/hud/stat_2.png'),
                            pygame.image.load('sprites/hud/stat_3.png'),
                            pygame.image.load('sprites/hud/stat_4.png'),
                            pygame.image.load('sprites/hud/stat_5.png'),
                            pygame.image.load('sprites/hud/stat_6.png'),
                            pygame.image.load('sprites/hud/stat_7.png'),
                            pygame.image.load('sprites/hud/stat_8.png'),
                            pygame.image.load('sprites/hud/stat_9.png'),
                            pygame.image.load('sprites/hud/stat_10.png'),
                            ]
        self.image_selection = pygame.image.load('sprites/hud/selection.png')
        self.image_selection_hide = pygame.image.load('sprites/hud/selection_hide.png')
        self.image_pause = pygame.Surface.convert_alpha(pygame.image.load('sprites/hud/pause_bg.png'))
        self.image_score = pygame.image.load('sprites/hud/score.png')
        self.screen_size = screen_size
        self.image = pygame.Surface(screen_size, pygame.SRCALPHA, 32)
        self.image.blit(self.image_health[10], (0, 20))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.fps = fps
        self.pause_game = False
        self.pause_cooldown = 0
        self.choice = 0
        self.upgrade_temp= [0,0]
        self.upgrade = False
        self.screen_size = screen_size
        self.button_timer = 0
        self.button_timer_start = False

    def update(self, player_health, player_score):
        self.image = pygame.Surface(self.screen_size, pygame.SRCALPHA, 32)
        self.image.blit(self.image_health[player_health], (0, 20))
        self.image_score = pygame.image.load('sprites/hud/score.png')
        score_font = pygame.font.SysFont('arial', 24)
        score_label = score_font.render(str(player_score), 1, (255, 255, 255))
        self.image_score.blit(score_label, (65,-2))
        self.image.blit(self.image_score, (self.screen_size[0] - self.image_score.get_width(), 20))

    def clear_hud(self):
        self.image = pygame.Surface(self.screen_size, pygame.SRCALPHA, 32)

    def add_choice(self):
        self.choice += 1

    def pause_update(self, attack_level, rapid_level, keys):

        if self.choice == 0:
            self.upgrade_temp[0] = attack_level
            self.upgrade_temp[1] = rapid_level
            self.image_pause.blit(self.image_stats[attack_level - 1], (185, 282))
            self.image_pause.blit(self.image_stats[rapid_level - 1], (185, 318))
            self.image.blit(self.image_pause, (self.screen_size[0] / 2 - self.image_pause.get_width() / 2,
                                               self.screen_size[1] / 2 - self.image_pause.get_height() / 2))
            print('Pasok')
            self.choice = 1

        if self.choice == 1:
            if keys[pygame.K_RETURN]:
                self.pause_game = False
            self.image_pause.blit(self.image_selection, (85, 115))  # FIRST
            self.image_pause.blit(self.image_selection_hide, (45, 310))
        elif self.choice == 2 and level_load:  # UPGRADE ATTACK
            print('Pasok din')
            if keys[pygame.K_RETURN] and self.upgrade_temp[0] < 10 and not self.button_timer_start:
                self.pause_game = False
                self.button_timer_start = True
                self.upgrade_temp[0] += 1
            self.image_pause.blit(self.image_selection_hide, (85, 115))
            self.image_pause.blit(self.image_selection_hide, (45, 310))
            self.image_pause.blit(self.image_selection, (45, 280))  # SECOND
        elif self.choice == 3 and level_load:  # UPGRADE RAPID
            if keys[pygame.K_RETURN] and self.upgrade_temp[1] < 10 and not self.button_timer_start:
                self.button_timer_start = True
                self.pause_game = False
                self.upgrade_temp[1] += 1
            self.image_pause.blit(self.image_selection_hide, (45, 280))
            self.image_pause.blit(self.image_selection_hide, (85, 115))
            self.image_pause.blit(self.image_selection, (45, 310))  # THIRD
        elif self.choice == 4 and level_load:
            self.choice = 1
        self.image_pause.blit(self.image_stats[self.upgrade_temp[0] - 1], (185, 282))
        self.image_pause.blit(self.image_stats[self.upgrade_temp[1] - 1], (185, 318))
        self.image.blit(self.image_pause, (self.screen_size[0] / 2 - self.image_pause.get_width() / 2,
                                           self.screen_size[1] / 2 - self.image_pause.get_height() / 2))
        self.upgrade = True

        if self.button_timer_start and self.button_timer == int(self.fps / 8):
            self.button_timer =0
            self.button_timer_start = False
        elif self.button_timer_start:
            self.button_timer +=1

    def game_over(self, screen):
        screen.fill((0, 0, 0))  # At each main-loop fill the whole screen with black.



