import sys
import pygame
from random import randint

from classes.Bullet import Bullet
from classes.Effect import Effect
from classes.Enemy import Enemy
from classes.Life import Life
from classes.Player import Player

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('music/phon.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

sound_shoot = pygame.mixer.Sound('music/shoot.mp3')
sound_kabum = pygame.mixer.Sound('music/effect.mp3')
sound_shoot.set_volume(0.3)
sound_kabum.set_volume(0.3)

SCREEN_W, SCREEN_H = 700, 500
window = pygame.display.set_mode((SCREEN_W, SCREEN_H))
background = pygame.transform.scale(pygame.image.load("images/kosmo.webp"), (SCREEN_W, SCREEN_H))
pygame.display.set_caption("Шутер")
fps = 60
clock = pygame.time.Clock()

player = Player('images/player.png', 207, 244, speed=6)
player.change_size_factor(0.5)
player.reset()

heal1 = Life('images/heal.png', 0, 0, 50, 50)
heal2 = Life('images/heal.png', 50, 0, 50, 50)
heal3 = Life('images/heal.png', 100, 0, 50, 50)

enemy_balls = Life('images/enemy.png', 500, 25, 100, 65)
font = pygame.font.SysFont('Arial', 32)
kill_balls = 0
enemy_balls_number = font.render(str(kill_balls), True, (255, 255, 255))

heals = pygame.sprite.Group(heal1, heal2, heal3)
enemies = pygame.sprite.Group()
effects = pygame.sprite.Group()
bullets = player.bullets

spawn_delay = 1000
spawn_last = 0
win = font.render('Победа!', True, (0, 255, 0))
lose = font.render('Поражение', True, (255, 0, 0))

while True:
    clock.tick(fps)


    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player.rect.top > 0:
        player.rect.y -= player.speed
    if keys[pygame.K_s] and player.rect.bottom < SCREEN_H:
        player.rect.y += player.speed
    if keys[pygame.K_a] and player.rect.left > 0:
        player.rect.x -= player.speed
        player.flip(True, False)
    if keys[pygame.K_d] and player.rect.right < SCREEN_W:
        player.rect.x += player.speed
        player.flip(False, False)
    if keys[pygame.K_SPACE]:
        if player.fire():
            sound_shoot.play()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print(event.pos)

    now = pygame.time.get_ticks()
    if now - spawn_last > spawn_delay:
        x = randint(0, SCREEN_W)
        enemy = Enemy('images/enemy.png', 900, 512, start_pos=(x, -200), end_pos=(x, 800))
        enemies.add(enemy)
        spawn_last = now
        enemy.change_size_factor(0.2)
        enemy.flip(False, True)

    player.update()
    enemies.update()
    effects.update()
    bullets.update()
    heals.update()

    hits1 = pygame.sprite.groupcollide(bullets, enemies, True, True)
    hits2 = pygame.sprite.spritecollide(player, enemies, True)

    for hit in hits1:
        kill_balls += 1
        enemy_balls_number = font.render(str(kill_balls), True, (255, 255, 255))
        effect = Effect("images/kabum.png", 43, 43, 1, 0)
        effect.change_size_factor(2)
        effect.rect.x = hit.rect.x
        effect.rect.y = hit.rect.y
        effects.add(effect)
        sound_kabum.play()

    for hit in hits2:
        effect = Effect("images/kabum.png", 43, 43, 1, 0)
        effect.change_size_factor(2)
        effect.rect.x = hit.rect.x
        effect.rect.y = hit.rect.y
        effects.add(effect)
        effect = Effect("images/kabum.png", 43, 43, 1, 0)
        effect.change_size_factor(2)
        effect.rect.x = player.rect.x
        effect.rect.y = player.rect.y
        effects.add(effect)
        pygame.mixer.find_channel().play(sound_kabum)
        if len(heals) > 0:
            remove_heal = heals.sprites()[-1]
            heals.remove(remove_heal)

    for enemy in enemies:
        if enemy.rect.y >= SCREEN_H:
            enemies.remove(enemy)
            if len(heals) > 0:
                remove_heal = heals.sprites()[-1]
                heals.remove(remove_heal)

    window.blit(background, (0, 0))
    window.blit(player.image, player.rect)

    enemies.draw(window)
    effects.draw(window)
    bullets.draw(window)
    heals.draw(window)

    window.blit(enemy_balls.image, enemy_balls.rect)
    window.blit(enemy_balls_number, (620, 25))

    if kill_balls >= 10:
        enemies.empty()
        window.blit(background, (0, 0))
        window.blit(player.image, player.rect)
        enemies.draw(window)
        effects.draw(window)
        bullets.draw(window)
        pygame.mixer.music.stop()
        pygame.mixer.music.load('music/phon_win.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        image_win = Life('images/win.png', 150, 50, 400, 350)
        window.blit(image_win.image, image_win.rect)
        break

    if len(heals) <= 0:
        enemies.empty()
        window.blit(background, (0, 0))
        window.blit(player.image, player.rect)
        enemies.draw(window)
        effects.draw(window)
        bullets.draw(window)
        pygame.mixer.music.stop()
        pygame.mixer.music.load('music/phon_lose.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        image_win = Life('images/lose.png', 150, 50, 400, 350)
        window.blit(image_win.image, image_win.rect)
        break

    pygame.display.flip()


while True:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()