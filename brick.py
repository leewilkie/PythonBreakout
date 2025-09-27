import pygame
from bricktype import BrickType

class Brick:
    def __init__(self, rect, brick_type: BrickType):
        self.rect = rect
        self.hits = brick_type.hits
        self.sprite_idx = brick_type.sprite_idx

    def hit(self):
        self.hits -= 1
        return self.hits <= 0
