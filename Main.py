import pygame
from Player import Player
from Projectile import Projectile
from Enemies import Enemy

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

player = Player(screen)
bullets = []
enemies = []
all_sprites.add(player)

player_stats_temp = [0] # Holds counter for animation or when can you shoot or what??? (rapid)


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
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_going = False

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    fps_count += 1

    if keys[pygame.K_ESCAPE]:
        keep_going = False
    if keys[pygame.K_SPACE]:
        shoot(True, player_stats_temp[0])

    player_stats_temp[0] = shoot(False, player_stats_temp[0])
    player.update(keys)
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()
