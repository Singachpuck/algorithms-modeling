import pygame

from Assets import Assets as assets

from utils import *

from entities.GameItem import GameItem
from entities.Tile import Tile
from entities.Button import Button


class TileSetting(GameItem):

    def __init__(self, parent, color, x_alignment, margin_x):
        super().__init__(parent,
                         size=(200, 250),
                         alignment_hor=x_alignment,
                         alignment_ver=Alignment.CENTER,
                         margin=(margin_x, 0))

        self.background_color = color
        self.left_arrow = Button(self.__shift_left,
                                 parent=self,
                                 asset=assets.images['arrow'],
                                 alignment_ver=Alignment.CENTER)
        self.right_arrow = Button(self.__shift_right,
                                  parent=self,
                                  asset=pygame.transform.flip(assets.images['arrow'], True, False),
                                  alignment_hor=Alignment.END,
                                  alignment_ver=Alignment.CENTER)
        self.rotate_button = Button(self.__rotate,
                                    parent=self,
                                    asset=assets.images['rotate'],
                                    alignment_hor=Alignment.CENTER,
                                    alignment_ver=Alignment.END)

        self.tiles_dict = dict((asset[:-5], value) for asset, value in assets.images.items() if asset.endswith('-tile'))
        self.tile_colors = list(self.tiles_dict.keys())
        if len(self.tiles_dict) == 0:
            raise IndexError('No tiles provided!')
        self.current_tile = 0
        self.rotated = False
        self.preview_tile = Tile(self,
                                 asset=self.tiles_dict[self.tile_colors[self.current_tile]],
                                 color=Tile.resolve_color(self.tile_colors[self.current_tile]),
                                 direction=Tile.VERTICAL if self.rotated else Tile.HORIZONTAL,
                                 alignment_ver=Alignment.CENTER,
                                 alignment_hor=Alignment.CENTER)

    def is_left_arrow_clicked(self, x, y):
        return self.left_arrow.is_clicked((x, y))

    def __shift_left(self):
        self.current_tile -= 1 if self.current_tile != 0 else 1 - len(self.tiles_dict)

    def is_right_arrow_clicked(self, x, y):
        return self.right_arrow.is_clicked((x, y))

    def __shift_right(self):
        self.current_tile += 1 if self.current_tile != len(self.tiles_dict) - 1 else 1 - len(self.tiles_dict)

    def is_rotate_button_clicked(self, x, y):
        return self.rotate_button.is_clicked((x, y))

    def __rotate(self):
        self.rotated = not self.rotated

    def get_tile(self, parent, coords):
        return Tile(parent,
                    asset=pygame.transform.rotate(self.tiles_dict[self.tile_colors[self.current_tile]],
                                                  90 if self.rotated else 0),
                    color=Tile.resolve_color(self.tile_colors[self.current_tile]),
                    direction=Tile.VERTICAL if self.rotated else Tile.HORIZONTAL,
                    margin=coords)

    def render(self):
        self.surface.fill(self.background_color)

        self.left_arrow.render()
        self.right_arrow.render()
        self.rotate_button.render()

        Tile(self,
             asset=pygame.transform.rotate(self.tiles_dict[self.tile_colors[self.current_tile]],
                                           90 if self.rotated else 0),
             color=Tile.resolve_color(self.tile_colors[self.current_tile]),
             direction=Tile.VERTICAL if self.rotated else Tile.HORIZONTAL,
             alignment_ver=Alignment.CENTER,
             alignment_hor=Alignment.CENTER).render()

        super(TileSetting, self).render()
