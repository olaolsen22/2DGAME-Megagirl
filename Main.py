import pygame
from Player import Player
from Projectile import Projectile
from Enemies import Enemy
from random import randint
pygame.mixer.init(44100, -16, 1, 512)
pygame.init()


class Floor(pygame.sprite.Sprite):
    def __init__(self, screen_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/level/floor_1.png')
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = self.image.get_rect().size[1] - screen_size[1]


resolution = (1280, 720)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Megagirl")
background = pygame.Surface(screen.get_size())
background = pygame.image.load('sprites/level/complet_1.png')
screen.blit(background, (0, 0))
pygame.mixer.Channel(0).play(pygame.mixer.Sound('sound/bg_music.ogg'))

clock = pygame.time.Clock()
keep_going = True
fps = 60
fps_count = 0

all_sprites = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()
level_sprites = pygame.sprite.Group()

bullets = []
enemies = []
floor = Floor(resolution)
player = Player(screen, 490, fps, floor.image.get_height())
all_sprites.add(player)
level_sprites.add(floor)

player_stats_temp = [0]  # Holds counter for animation or when can you shoot or what??? (rapid)
enemy_count = 4
spawn_enemies = True
enemy_death_counter = 0
player_damage_cooldown = 0


def enemy_randomizer():
    for i in range(0, randint(2, enemy_count)):
        enemy_spawn(0, True)
    return False


def enemy_spawn(enemy_type, spawn):
    if spawn:
        enemies.append(Enemy(enemy_type, resolution, fps, floor.image.get_height()))
    else:
        for enemy in enemies:
            enemy.update()
            all_sprites.add(enemy)


def shoot(add_bullet, rapid_temp):
    if add_bullet and (fps / player.rapid) == rapid_temp:
        bullets.append(Projectile(player.rect.x, player.rect.y, player.direction))
    if (fps / player.rapid) == rapid_temp:
        rapid_temp = 0
    for bullet in bullets:
        if bullet.rect.x > resolution[0] or bullet.rect.x < -50 or bullet.rect.y < -50 or bullet.rect.y > resolution[1] - floor.image.get_height():
            if bullet.rect.y > resolution[1] - floor.image.get_height():
                bullet.miss()
            bullets.pop(bullets.index(bullet))
            all_sprites.remove(bullet)
        else:
            bullet.update()
            all_sprites.add(bullet)
    rapid_temp += 1
    return rapid_temp


while keep_going:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_going = False

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    fps_count += 1
    player.update(keys, mouse)

    if spawn_enemies:
        spawn_enemies = enemy_randomizer()

    if keys[pygame.K_ESCAPE]:
        keep_going = False
    if keys[pygame.K_a]:
        shoot(True, player_stats_temp[0])

    for bullet in bullets:
        for enemy in enemies:
            if enemy.hit_points <= 0:
                    enemy.is_dead = True
            if pygame.sprite.collide_rect(bullet, enemy):
                enemy.take_damage(player.attack, screen)
                bullets.pop(bullets.index(bullet))
                all_sprites.remove(bullet)
                break
    for enemy in enemies:
        if enemy.pop:
            enemy_death_counter = 0
            enemies.pop(enemies.index(enemy))
            all_sprites.remove(enemy)
            all_enemies.remove(enemy)
        if pygame.sprite.collide_rect(enemy, player):
            player.is_hurting = True

    player_stats_temp[0] = shoot(False, player_stats_temp[0])
    enemy_spawn(0, False)

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    all_enemies.draw(screen)
    level_sprites.draw(screen)
    pygame.display.update()

pygame.quit()
