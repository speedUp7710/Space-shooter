import pygame


class Life(pygame.sprite.Sprite):
    def __init__(self, file_name, x, y, width, height):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(file_name), (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))