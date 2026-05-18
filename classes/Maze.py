import pygame

from classes.Life import Wall


class Maze:
    def __init__(self, wall_image, size, screen_width, screen_height):
        self.image = wall_image
        self.size = size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.walls = pygame.sprite.Group()
        self.map = [
            '111111111111011',
            '110001000100011',
            '100100010001111',
            '101111111111111',
            '101011111011111',
            '100000000000001',
            '111111011111101',
            '111011111011101',
            '100000000000001',
            '101111111111111'
        ]
        self.build_maze()

    def build_maze(self):
        self.walls.empty()
        for row_idx, row in enumerate(self.map):
            if row_idx * self.size >= self.screen_height:
                break
            for col_idx, cell in enumerate(row):
                if col_idx * self.size >= self.screen_width:
                    break
                if cell == '1':
                    x = col_idx * self.size
                    y = row_idx * self.size
                    self.walls.add(Wall(self.image, x, y, self.size, self.size))

    def draw(self, surface):
        self.walls.draw(surface)

    def collide(self, sprite):
        return pygame.sprite.spritecollideany(sprite, self.walls)