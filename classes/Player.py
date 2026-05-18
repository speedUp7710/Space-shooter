import pygame

from classes.AnimSprite import AnimSprite
from classes.Bullet import Bullet


class Player(AnimSprite):
    def __init__(self, file_name, frame_width=None, frame_height=None, anim_speed=0, speed=2):
        super().__init__(file_name, frame_width, frame_height, anim_speed, speed)
        self.spawn_pos = (300, 370)
        self.reset()
        self.delay = 500
        self.last_shoot_time = 0
        self.bullets = pygame.sprite.Group()

    def reset(self):
        self.rect.topleft = self.spawn_pos

    def fire(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot_time > self.delay:
            bullet = Bullet('images/laser.png', self.rect.x, self.rect.y, 20, 60)
            self.bullets.add(bullet)
            self.last_shoot_time = now
            return True
        return False

