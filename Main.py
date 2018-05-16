import pygame
from Player import Player
from Projectile import Projectile
from Enemies import Enemy
from random import randint

resolution = (1280, 720)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Megagirl")
background = pygame.Surface(screen.get_size())
background.fill((0, 0, 0))
screen.blit(background, (0, 0))

clock = pygame.time.Clock()
keep_going = True
fps = 60
fps_count = 0

all_sprites = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()

player = Player(screen)
bullets = []
enemies = []
all_sprites.add(player)

player_stats_temp = [0]  # Holds counter for animation or when can you shoot or what??? (rapid)
enemy_count = 5
spawn_enemies = True


def enemy_randomizer():
    for i in range(0, randint(2, enemy_count)):
        enemy_spawn(0, True)
    return False


def enemy_spawn(enemy_type, spawn):
    if spawn:
        enemies.append(Enemy(enemy_type, resolution))
    else:
        for enemy in enemies:
            enemy.update()
            all_sprites.add(enemy)


def shoot(add_bullet, rapid_temp):
    if add_bullet and (fps / player.rapid) == rapid_temp:
        bullets.append(Projectile(player.rect.x, player.rect.y, pygame.mouse.get_pos()))
    if (fps / player.rapid) == rapid_temp:
        rapid_temp = 0
    for bullet in bullets:
        if bullet.rect.x > resolution[0] or bullet.rect.x < -50 or bullet.rect.y < -50 or bullet.rect.y > resolution[1]:
            bullets.pop(bullets.index(bullet))
            all_sprites.remove(bullet)
            print('popped')
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

    if spawn_enemies:
        spawn_enemies = enemy_randomizer()

    if keys[pygame.K_ESCAPE]:
        keep_going = False
    if keys[pygame.K_SPACE]:
        shoot(True, player_stats_temp[0])

    for bullet in bullets:
        for enemy in enemies:
            if enemy.hit_points <= 0:
                enemies.pop(enemies.index(enemy))
                all_sprites.remove(enemy)
                all_enemies.remove(enemy)
            if pygame.sprite.collide_rect(bullet, enemy):
                enemy.take_damage(player.attack)
                bullets.pop(bullets.index(bullet))
                all_sprites.remove(bullet)
                break

    player_stats_temp[0] = shoot(False, player_stats_temp[0])
    enemy_spawn(0, False)
    player.update(keys)
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    all_enemies.draw(screen)
    pygame.display.update()

pygame.quit()
