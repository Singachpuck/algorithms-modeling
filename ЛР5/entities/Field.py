import copy
import pygame

from utils import *

from entities.Cell import Cell
from entities.Tile import Tile
from entities.GameItem import GameItem

from structures.StateTree import State


class Field(GameItem):

    def __init__(self, parent, border_size, asset, cell_size):
        super().__init__(parent, surface=asset, alignment_hor=Alignment.CENTER, alignment_ver=Alignment.CENTER)
        self.border_size = border_size
        self.sheet_coords = tuple(map(lambda coord: coord + self.border_size, self.absolute_coords))
        self.cell_size = cell_size
        self.cells_number = int((self.surface.get_width() - 2 * border_size) / cell_size)
        self.tiles = []
        self.cells = [[Cell(cell_size, (x, y)) for x in range(self.cells_number)] for y in range(self.cells_number)]
        self.previous_tile = None
        self.blocked_list = []

    def append_tile(self, tile, player):
        if self._tile_fit(tile, player):
            new_tile_cell_x, new_tile_cell_y = self._get_tile_pos(tile)

            self.cells[new_tile_cell_y][new_tile_cell_x].tile = tile

            for cell in self.blocked_list:
                cell.blocked = False

            self.blocked_list.clear()

            if new_tile_cell_x != 0:
                self.cells[new_tile_cell_y][new_tile_cell_x - 1].blocked = True
                self.blocked_list.append(self.cells[new_tile_cell_y][new_tile_cell_x - 1])

            if new_tile_cell_y != 0:
                self.cells[new_tile_cell_y - 1][new_tile_cell_x].blocked = True
                self.blocked_list.append(self.cells[new_tile_cell_y - 1][new_tile_cell_x])

            if new_tile_cell_x != self.cells_number - 1:
                self.cells[new_tile_cell_y][new_tile_cell_x + 1].blocked = True
                self.blocked_list.append(self.cells[new_tile_cell_y][new_tile_cell_x + 1])

            if new_tile_cell_y != self.cells_number - 1:
                self.cells[new_tile_cell_y + 1][new_tile_cell_x].blocked = True
                self.blocked_list.append(self.cells[new_tile_cell_y + 1][new_tile_cell_x])

            if tile.direction == Tile.HORIZONTAL:
                self.cells[new_tile_cell_y][new_tile_cell_x + 1].tile = tile

                if new_tile_cell_y != 0:
                    self.cells[new_tile_cell_y - 1][new_tile_cell_x + 1].blocked = True
                    self.blocked_list.append(self.cells[new_tile_cell_y - 1][new_tile_cell_x + 1])

                if new_tile_cell_x + 1 < self.cells_number - 1:
                    self.cells[new_tile_cell_y][new_tile_cell_x + 2].blocked = True
                    self.blocked_list.append(self.cells[new_tile_cell_y][new_tile_cell_x + 2])

                if new_tile_cell_y < self.cells_number - 1:
                    self.cells[new_tile_cell_y + 1][new_tile_cell_x + 1].blocked = True
                    self.blocked_list.append(self.cells[new_tile_cell_y + 1][new_tile_cell_x + 1])
            else:
                self.cells[new_tile_cell_y + 1][new_tile_cell_x].tile = tile

                if new_tile_cell_x != 0:
                    self.cells[new_tile_cell_y + 1][new_tile_cell_x - 1].blocked = True
                    self.blocked_list.append(self.cells[new_tile_cell_y + 1][new_tile_cell_x - 1])

                if new_tile_cell_x < self.cells_number - 1:
                    self.cells[new_tile_cell_y + 1][new_tile_cell_x + 1].blocked = True
                    self.blocked_list.append(self.cells[new_tile_cell_y + 1][new_tile_cell_x + 1])

                if new_tile_cell_y + 1 < self.cells_number - 1:
                    self.cells[new_tile_cell_y + 2][new_tile_cell_x].blocked = True
                    self.blocked_list.append(self.cells[new_tile_cell_y + 2][new_tile_cell_x])

            self.tiles.append(tile)
            self.previous_tile = tile

            return True

        return False

    def _tile_fit(self, new_tile, player):
        if not pygame.Rect(self.sheet_coords,
                           tuple(map(lambda size: size - 2 * self.border_size, self.surface.get_size()))) \
                .contains(pygame.Rect(new_tile.absolute_coords, new_tile.surface.get_size())):
            return False

        new_tile_cell_x, new_tile_cell_y = self._get_tile_pos(new_tile)

        if not player.blocked:
            for blocked_cell in self.blocked_list:
                if blocked_cell.pos == (new_tile_cell_x, new_tile_cell_y):
                    player.blocked = True
                    return False

                if new_tile.direction == Tile.HORIZONTAL \
                        and blocked_cell.pos == (new_tile_cell_x + 1, new_tile_cell_y):
                    player.blocked = True
                    return False
                elif new_tile.direction == Tile.VERTICAL \
                        and blocked_cell.pos == (new_tile_cell_x, new_tile_cell_y + 1):
                    player.blocked = True
                    return False

        if new_tile_cell_x == 3 and new_tile_cell_y == 3 \
                or new_tile.direction == Tile.HORIZONTAL and new_tile_cell_x == 2 and new_tile_cell_y == 3 \
                or new_tile.direction == Tile.VERTICAL and new_tile_cell_x == 3 and new_tile_cell_y == 2:
            return False

        if new_tile.direction == Tile.HORIZONTAL \
                and self.cells[new_tile_cell_y][new_tile_cell_x + 1].tile is not None:
            return False
        elif new_tile.direction == Tile.VERTICAL \
                and self.cells[new_tile_cell_y + 1][new_tile_cell_x].tile is not None:
            return False

        return True

    def _get_tile_pos(self, tile):
        return tuple(map(lambda coords: int((coords[1] - coords[0]) / self.cell_size),
                         zip(self.sheet_coords, tile.absolute_coords)))

    def get_cell_coords(self, x, y):
        return int(
            (x - self.border_size - self.absolute_coords[0]) / self.cell_size) * self.cell_size + self.border_size, \
               int((y - self.border_size - self.absolute_coords[
                   1]) / self.cell_size) * self.cell_size + self.border_size

    def is_sheet_coords(self, x, y):
        return pygame.Rect(self.sheet_coords,
                           (self.surface.get_width() - 2 * self.border_size,
                            self.surface.get_height() - 2 * self.border_size)) \
            .collidepoint(x, y)

    def filled(self):
        for i in range(self.cells_number):
            for j in range(self.cells_number - 1):
                if self.cells[i][j].tile is None and self.cells[i][j + 1].tile is None and i not in (2, 3) and j != 3:
                    return False

                if self.cells[j][i].tile is None and self.cells[j + 1][i].tile is None and j not in (2, 3) and i != 3:
                    return False

        return True

    # def count_sections(self):
    #     section_count = 0
    #
    #     for y in range(self.cells_number):
    #         for x in range(self.cells_number):
    #             if self.cells[y][x].tile is None:
    #                 continue
    #
    #             if x != 0 and self.cells[y][x - 1].tile is not None and \
    #                     self.cells[y][x].tile.color == self.cells[y][x - 1].tile.color:
    #                 continue
    #
    #             if y != 0 and self.cells[y - 1][x].tile is not None and \
    #                     self.cells[y][x].tile.color == self.cells[y - 1][x].tile.color:
    #                 continue
    #
    #             section_count += 1
    #
    #     return section_count

    def get_state(self, minmax=False):
        cells = list(map(lambda cell_row: list(map(lambda c: copy.copy(c), cell_row)), self.cells))

        for cell_row in cells:
            for cell in cell_row:
                if cell.tile is not None:
                    cell.tile = cell.tile.color

        return State(None, cells, minmax)

    def get_static_evaluation(self):
        return self.get_state().get_static_evaluation()

    def render(self):
        for tile in self.tiles:
            tile.render()

        super(Field, self).render()
