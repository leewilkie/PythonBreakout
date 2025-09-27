import pygame

class Bullet:
    def __init__(self, x, y, speed=14):
        self.x = x
        self.y = y
        self.width = 4
        self.height = 12
        self.speed = speed
    @property
    def rect(self):
        return pygame.Rect(int(self.x - self.width // 2), int(self.y - self.height), self.width, self.height)
