import pygame

from utils import *


class GameItem:

    def __init__(self, parent, *,
                 surface=None,
                 size=None,
                 alignment_hor=Alignment.START,
                 alignment_ver=Alignment.START,
                 margin=(0, 0),
                 copy_surface=True):
        self.parent = parent
        if surface is None and size is None:
            raise ValueError('Wrong arguments!')
        self.surface = pygame.Surface(size, pygame.SRCALPHA, 32) if surface is None else pygame.Surface.copy(
            surface) if copy_surface else surface
        self.__alignment_hor = alignment_hor
        self.__alignment_ver = alignment_ver
        self.__margin = margin
        self.coords = self.__get_coords()
        self.absolute_coords = tuple(map(lambda coord_pair: int(coord_pair[0] + coord_pair[1]),
                                         zip(self.coords, parent.coords))) \
            if parent is not None else self.coords

    def is_clicked(self, click_coords):
        return pygame.Rect(self.absolute_coords, self.surface.get_size()).collidepoint(click_coords)

    def __get_coords(self):
        x, y = 0, 0

        if self.__alignment_hor == Alignment.START:
            x = self.__margin[0]
        elif self.__alignment_hor == Alignment.END:
            x = self.parent.surface.get_width() - self.surface.get_width() - self.__margin[0]
        elif self.__alignment_hor == Alignment.CENTER:
            x = get_axis_center_coords(self.parent.surface.get_width(), self.surface.get_width())

        if self.__alignment_ver == Alignment.START:
            y = self.__margin[1]
        elif self.__alignment_ver == Alignment.END:
            y = self.parent.surface.get_height() - self.surface.get_height() - self.__margin[1]
        elif self.__alignment_ver == Alignment.CENTER:
            y = get_axis_center_coords(self.parent.surface.get_height(), self.surface.get_height())

        return x, y

    def render(self):
        self.parent.surface.blit(self.surface, self.coords)
