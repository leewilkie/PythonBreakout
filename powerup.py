import pygame
import random

class Powerup:
    LASER = 1
    MULTIBALL = 2
    WIDEBAT = 3
    POWERBALL = 4
    TYPES = [LASER, MULTIBALL, WIDEBAT, POWERBALL]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 12
        self.type = random.choice(Powerup.TYPES)
        if self.type == Powerup.LASER:
            self.colour = (255, 0, 0)
        elif self.type == Powerup.MULTIBALL:
            self.colour = (0, 120, 255)
        elif self.type == Powerup.WIDEBAT:
            self.colour = (128, 128, 128)
        elif self.type == Powerup.POWERBALL:
            self.colour = (0, 0, 0)
        else:
            self.colour = (255, 0, 0)
    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
