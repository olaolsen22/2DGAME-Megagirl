import pygame, math
from Player import Player
from Projectile import Projectile
from Enemies import Enemy
from random import randint
from Hud import Hud
from Levels import Level
pygame.mixer.init(44100, -16, 1, 512)
pygame.init()

resolution = (1280, 720)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Rockman Legends")
background = pygame.Surface(screen.get_size())
background = pygame.image.load('sprites/level/complet_1.png')
background = pygame.Surface.convert(background)
screen.blit(background, (0, 0))
pygame.mixer.Channel(0).play(pygame.mixer.Sound('sound/bg_music.ogg'))

clock = pygame.time.Clock()
keep_going = True
fps = 60
fps_count = 0

# Sprite Groups

all_sprites = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()
level_sprites = pygame.sprite.Group()
hud_sprites = pygame.sprite.Group()

hud = Hud(resolution, fps)
bullets = []
enemy_bullets = []
enemies = []

level = Level(resolution)
level_loading = True
player = Player(screen, 490, fps, level.image.get_height())
hud_sprites.add(hud)
all_sprites.add(player)

level_sprites.add(level)

player_stats_temp = [0]
enemy_count_1 = 2
enemy_count_2 = 1
spawn_enemies = True
enemy_total = 0
enemy_death_counter = 0
player_damage_cooldown = 0
enemy_shoot_counter = [0,0]

hud_choice_counter = 0

gameover_sound_temp = True


def enemy_randomizer():
    for i in range(0, randint(1, enemy_count_1)):
        enemy_spawn(0, True)
    for i in range(0, randint(1, enemy_count_2)):
        enemy_spawn(1, True)
    return False


def enemy_spawn(enemy_type, spawn):
    if spawn:
        enemies.append(Enemy(enemy_type, resolution, fps, level.image.get_height()))
    else:
        for enemy in enemies:
            enemy.update()
            all_sprites.add(enemy)


def enemy_shoot():
    for enemy in enemies:
        if enemy.enemy_type == 1:
            if enemy.shoot_count[0] == fps * 4:
                enemy.get_direction(player.rect.x, player.rect.y)
                enemy_bullets.append(Projectile(enemy.rect.x, enemy.rect.y - 20, enemy.direction - 5, True))
                enemy.shoot_count[0] = 0
            else:
                enemy.shoot_count[0] += 1

    for bullet in enemy_bullets:
        all_sprites.add(bullet)
        bullet.update_enemy()


def shoot(add_bullet, rapid_temp):
    now = pygame.time.get_ticks()
    if add_bullet and now - player.last >= 1000/player.rapid:#(fps / player.rapid) == rapid_temp:
        bullets.append(Projectile(player.rect.x, player.rect.y, player.direction, True))
        player.last = pygame.time.get_ticks()
    if (fps / player.rapid) == rapid_temp:
        rapid_temp = 0
    for bullet in bullets:
        if bullet.rect.x > resolution[0] or bullet.rect.x < -50 or bullet.rect.y < -50 or bullet.rect.y > resolution[1] - level.image.get_height():
            if bullet.rect.y > resolution[1] - level.image.get_height():
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

    if keys[pygame.K_ESCAPE]:
        keep_going = False

    if player.hit_points > 0:

        # Randomizes Level

        if level_loading:
            player.hit_points = 10
            spawn_enemies = enemy_randomizer()
            enemy_count_1 += 2
            enemy_count_2 += 1
            player.attack_level += 1
            player.rapid_level += .25
            player.update_stats(player.attack_level, player.rapid_level)
            level_loading = False

        if len(enemies) == 0:
            level_loading = True
            for bullet in bullets:
                bullets.pop(bullets.index(bullet))
                all_sprites.remove(bullet)
                all_sprites.draw(screen)

        enemy_shoot()
        hud.update(player.hit_points, player.score)
        fps_count += 1
        player.update(keys, mouse)

        if keys[pygame.K_a]:
            shoot(True, player_stats_temp[0])

        # Collision of player and enemy bullet

        if len(enemy_bullets) > 0:
            for bullet in enemy_bullets:
                if pygame.sprite.collide_rect(player, bullet):
                    player.hit_points -= 1
                    pygame.mixer.Channel(5).play(pygame.mixer.Sound('sound/player/sfx-hurt1.wav'))
                    enemy_bullets.pop(enemy_bullets.index(bullet))
                    all_sprites.remove(bullet)

        # Collision of player bullet and enemy

        for bullet in bullets:
            for enemy in enemies:
                if enemy.hit_points <= 0:
                    enemy.is_dead = True
                if pygame.sprite.collide_rect(bullet, enemy) and not enemy.is_dead:
                    player.score += enemy.score_hit
                    enemy.take_damage(player.attack, screen)
                    bullets.pop(bullets.index(bullet))
                    all_sprites.remove(bullet)
                    break
        # Death of enemy
        for enemy in enemies:
            if enemy.pop:
                player.score += enemy.score_kill
                enemy_death_counter = 0
                enemies.pop(enemies.index(enemy))
                all_sprites.remove(enemy)
                all_enemies.remove(enemy)

            # Player gets hurt when colliding with enemy

            if pygame.sprite.collide_rect(enemy, player):
                player.is_hurting = True
                player.player_hurt()

        # Timer before player can shoot again
        player_stats_temp[0] = shoot(False, player_stats_temp[0])
        enemy_spawn(0, False)

        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        all_enemies.draw(screen)
        level_sprites.draw(screen)
        hud_sprites.draw(screen)

    else:
        hud.update(player.hit_points, player.score)
        if gameover_sound_temp:
            pygame.mixer.stop()
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('sound/gameover.ogg'))
            gameover_sound_temp = False
        gameover_font = pygame.font.SysFont('arial', 75)
        gameover_help_font = pygame.font.SysFont('arial', 32)
        gameover_label = gameover_font.render('GAME OVER', 1, (255, 0, 0))
        screen.blit(gameover_label, (resolution[0] / 2 - (gameover_label.get_width() / 2), resolution[1] / 2 - gameover_label.get_height()))
        gameover_help_label = gameover_help_font.render('PRESS ESC KEY TO QUIT', 1, (255, 255, 255))
        screen.blit(gameover_help_label, (resolution[0] / 2 - (gameover_label.get_width() / 2) + 25, resolution[1] / 2 - gameover_label.get_height() + 100))

    pygame.display.update()

pygame.quit()
