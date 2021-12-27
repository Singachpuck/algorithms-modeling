import pygame

from utils import *
from Assets import Assets as assets

from entities.GameItem import GameItem


class EnemyBoard(GameItem):

    def __init__(self, player, parent, *, size):
        super().__init__(parent, size=size, alignment_hor=Alignment.CENTER, alignment_ver=Alignment.START)

        self.player = player
        self.board = pygame.Surface((8 * 63 * 1.5, size[1]), pygame.SRCALPHA, 32).convert_alpha()

    def render(self):
        self.surface = self.clean_surface.copy()
        self.board = pygame.Surface((8 * 63 * 1.5, self.surface.get_height()), pygame.SRCALPHA, 32).convert_alpha()

        for i in range(min(8, len(self.player.cards))):
            self.board.blit(assets.images['card_back'], (i * 63 * 1.5, -75))

        self.surface.blit(self.board, get_center_coordinates(self.surface.get_size(), self.board.get_size()))

        super().render()


