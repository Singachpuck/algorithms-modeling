import pygame

from utils import *

from entities.GameItem import GameItem


class Tile(GameItem):

    HORIZONTAL = 0
    VERTICAL = 1

    RED = 0
    BLUE = 1
    GREEN = 2
    YELLOW = 3

    def __init__(self, parent, *,
                 asset,
                 color,
                 direction,
                 alignment_hor=Alignment.START,
                 alignment_ver=Alignment.START,
                 margin=(0, 0)):
        super().__init__(parent,
                         surface=asset,
                         alignment_ver=alignment_ver,
                         alignment_hor=alignment_hor,
                         margin=margin)
        self.color = color
        self.direction = direction

    def shift_left_half_size(self):
        self.coords = (self.coords[0] - self.surface.get_width() / 2, self.coords[1])

    def shift_top_half_size(self):
        self.coords = (self.coords[0], self.coords[1] - self.surface.get_height() / 2)

    @staticmethod
    def resolve_color(color):
        if color == 'red':
            return Tile.RED
        elif color == 'green':
            return Tile.GREEN
        elif color == 'blue':
            return Tile.BLUE
        elif color == 'yellow':
            return Tile.YELLOW
        else:
            raise Exception('Unknown color!')
