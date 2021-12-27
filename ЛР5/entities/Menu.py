import pygame

from Assets import Assets as assets

from entities.GameItem import GameItem
from entities.Option import Option
from utils import *


class Menu(GameItem):
    select_border_size = 5
    select_border_color = assets.colors['dark_brown']

    def __init__(self, parent, *,
                 options,
                 size=None,
                 alignment_hor=Alignment.START,
                 alignment_ver=Alignment.START,
                 margin=(0, 0)):
        super().__init__(parent,
                         size=size,
                         alignment_hor=alignment_hor,
                         alignment_ver=alignment_ver,
                         margin=margin)

        tile_size = 75
        margin_bottom = 15

        self.options = [Option(self, options[i], tile_size, (tile_size + margin_bottom) * i)
                        for i in range(len(options))]

        self.current_option = 0

        self.border_surf = pygame.Surface((self.options[self.current_option].surface.get_width()
                                           + Menu.select_border_size * 2,
                                           self.options[self.current_option].surface.get_height()
                                           + Menu.select_border_size * 2))

        self.border_surf.fill(Menu.select_border_color)

    def render(self):
        self.parent.surface.blit(self.border_surf, (self.options[self.current_option].absolute_coords[0]
                                                    - Menu.select_border_size,
                                                    self.options[self.current_option].absolute_coords[1]
                                                    - Menu.select_border_size))

        for option in self.options:
            option.render()

        super().render()
