class Sprite:
    def __init__(self, x, y, width, height):
        import pygame
        self.rect = pygame.Rect(x, y, width, height)
