import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, file_name, x, y, width, height, speed=5):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(file_name), (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()