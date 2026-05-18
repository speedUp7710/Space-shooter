from classes.AnimSprite import AnimSprite


class Effect(AnimSprite):
    def update(self):
        if self.current_frame >= len(self.base_frames) - 1:
            self.kill()
            return

        if len(self.base_frames) > 1 and self.anim_speed > 0:
            self.frame_index += self.anim_speed
            if self.frame_index >= len(self.base_frames):
                self.frame_index = 0.0
            self.current_frame = int(self.frame_index)
            self.get_actual_image()