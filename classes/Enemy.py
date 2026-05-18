import math
import time
from classes.AnimSprite import AnimSprite


class Enemy(AnimSprite):
    def __init__(self, file_name, frame_width=None, frame_height=None,
                 anim_speed=0, speed=2, start_pos=(0, 0), end_pos=(100, 100)):
        super().__init__(file_name, frame_width, frame_height, anim_speed, speed)

        self.start_pos = start_pos
        self.end_pos = end_pos
        self.current_target = self.end_pos
        self.rect.center = self.start_pos
        self.pause_duration = 1
        self.is_paused = False
        self.start_time = 0

    def update(self):
        current_time = time.time()
        if self.is_paused:
            if current_time - self.start_time >= self.pause_duration:
                self.is_paused = False
                if self.current_target == self.end_pos:
                    self.current_target = self.start_pos
                else:
                    self.current_target = self.end_pos
            else:
                super().update()
                return

        dx = self.current_target[0] - self.rect.centerx
        dy = self.current_target[1] - self.rect.centery
        distance = math.hypot(dx, dy)

        if distance < self.speed:
            self.is_paused = True
            self.start_time = time.time()
            self.rect.center = self.current_target
        else:
            self.rect.centerx += round(dx / distance * self.speed)
            self.rect.centery += round(dy / distance * self.speed)

        super().update()