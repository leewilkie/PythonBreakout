import pygame

MID_BLUE = (0, 80, 200)

class Ball:
    def __init__(self, x, y, speed_x, speed_y, radius=6):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = speed_x
        self.speed_y = speed_y
    @property
    def rect(self):
        return pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)
