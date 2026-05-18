import pygame


class AnimSprite(pygame.sprite.Sprite):
    """АНИМ спрайт"""
    def __init__(self, file_name:str, frame_width:int=None, frame_height:int=None, anim_speed:float=1, speed:float=0):
        super().__init__()
        sheet = pygame.image.load(file_name).convert_alpha()
        sw, sh = sheet.get_size()

        #Вроде работает
        if frame_width is None or frame_height is None or (sw <= frame_width and sh <= frame_height):
            frame_width, frame_height = sw, sh
            self._raw_frames = [sheet]
        else:
            # Нарэзка
            self._raw_frames = []
            for y in range(0, sh, frame_height):
                for x in range(0, sw, frame_width):
                    if x + frame_width <= sw and y + frame_height <= sh:
                        self._raw_frames.append(sheet.subsurface((x, y, frame_width, frame_height)))

            if not self._raw_frames:  # Если нарэзка не удалась
                self._raw_frames = [sheet]
                print('Нарэзка не удалась!')

        # Копии кадров стд кадров
        self.base_frames = [f.copy() for f in self._raw_frames]


        self.angle = 0
        self.flip_x = False
        self.flip_y = False


        self.frame_index = 0.0
        self.anim_speed = anim_speed
        self.current_frame = 0
        self.speed = speed


        self.image = self.base_frames[0]
        self.rect = self.image.get_rect()

    def get_actual_image(self):
        old_center = self.rect.center

        frame = self.base_frames[self.current_frame].copy()
        if self.flip_x or self.flip_y:
            frame = pygame.transform.flip(frame, self.flip_x, self.flip_y)

        if self.angle != 0:
            frame = pygame.transform.rotate(frame, self.angle)

        self.image = frame
        self.rect = self.image.get_rect(center=old_center)

    def update(self):
        """Перерассчёт позиций"""
        if len(self.base_frames) > 1 and self.anim_speed > 0:
            self.frame_index += self.anim_speed
            if self.frame_index >= len(self.base_frames):
                self.frame_index = 0.0
            self.current_frame = int(self.frame_index)
            self.get_actual_image()

    def rotate(self, angle):
        if self.angle != angle:
            self.angle = angle
            self.get_actual_image()

    def flip(self, flip_x, flip_y):
        if self.flip_x != flip_x or self.flip_y != flip_y:
            self.flip_x = flip_x
            self.flip_y = flip_y
            self.get_actual_image()

    def change_size(self, width, height):
        self.base_frames = [pygame.transform.scale(f, (width, height))
            for f in self._raw_frames]
        self.get_actual_image()

    def change_size_factor(self, factor):
        self.base_frames = [
            pygame.transform.scale(
                f,
                (int(f.get_width() * factor), int(f.get_height() * factor))
            )
            for f in self._raw_frames
        ]
        self.get_actual_image()