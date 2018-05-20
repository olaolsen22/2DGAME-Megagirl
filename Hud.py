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
        self.image_score = pygame.Surface.convert_alpha(pygame.image.load('sprites/hud/score.png'))
        self.image_level = pygame.Surface.convert_alpha(pygame.image.load('sprites/hud/level.png'))
        self.image_enemies = pygame.Surface.convert_alpha(pygame.image.load('sprites/hud/enemies.png'))
        self.screen_size = screen_size
        self.image = pygame.Surface(screen_size, pygame.SRCALPHA, 32)
        self.image.blit(self.image_health[10], (0, 20))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.fps = fps
        self.pause_game = False
        self.upgrade = False
        self.screen_size = screen_size

    def update(self, player_health, player_score, level, enemies):
        self.image = pygame.Surface(self.screen_size, pygame.SRCALPHA, 32)
        self.image.blit(self.image_health[player_health], (0, 20))


        self.image_score = pygame.Surface.convert_alpha(pygame.image.load('sprites/hud/score.png'))
        stats_font = pygame.font.SysFont('arial', 24)
        stats_label = stats_font.render(str(player_score), 1, (255, 255, 255))
        self.image_score.blit(stats_label, (65,-2))
        self.image.blit(self.image_score, (self.screen_size[0] - self.image_score.get_width(), 20))


        self.image_level = pygame.Surface.convert_alpha(pygame.image.load('sprites/hud/level.png'))
        stats_label = stats_font.render(str(level), 1, (255, 255, 255))
        self.image_level.blit(stats_label, (65, -2))
        self.image.blit(self.image_level, (self.screen_size[0] - self.image_score.get_width(), 50))

        self.image_enemies = pygame.Surface.convert_alpha(pygame.image.load('sprites/hud/enemies.png'))
        stats_label = stats_font.render(str(enemies), 1, (255, 255, 255))
        self.image_enemies.blit(stats_label, (65, -2))
        self.image.blit(self.image_enemies, (self.screen_size[0] - self.image_score.get_width(), 80))

    def clear_hud(self):
        self.image = pygame.Surface(self.screen_size, pygame.SRCALPHA, 32)

    def game_over(self, screen):
        screen.fill((0, 0, 0))  # At each main-loop fill the whole screen with black.



