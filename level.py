import json
import pygame
from brick import Brick

class Level:
    def __init__(self, bricks, background):
        self.bricks = bricks  # List of Brick objects
        self.background = background  # Filename of the background image
