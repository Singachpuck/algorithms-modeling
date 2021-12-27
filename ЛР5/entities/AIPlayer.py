import pygame

from Assets import Assets as assets

from entities.Player import Player

from structures.StateTree import *


class AIPlayer(Player):

    def __init__(self, *, field, player_type, level):
        super().__init__(field)
        self.minmax = player_type == 'smaller'

        if level == 'hard':
            self.depth = 3
        elif level == 'medium':
            self.depth = 2
        else:
            self.depth = 1

    def move(self, *args, **kwargs):
        start_state = self.field.get_state(self.minmax)

        state_tree = StateTree(self.depth, start_state, self)

        next_state = state_tree.get_next()

        if next_state is None:
            self.blocked = False
            return True

        tile_pos = []

        for y in range(self.field.cells_number):
            for x in range(self.field.cells_number):
                if next_state.cells[y][x].tile is not None and self.field.cells[y][x].tile is None:
                    tile_pos.append((x, y))

                    if len(tile_pos) == 2:
                        break
            else:
                continue
            break

        color = next_state.cells[tile_pos[0][1]][tile_pos[0][0]].tile

        if color == Tile.RED:
            tile_asset = assets.images['red-tile']
        elif color == Tile.GREEN:
            tile_asset = assets.images['green-tile']
        elif color == Tile.BLUE:
            tile_asset = assets.images['blue-tile']
        elif color == Tile.YELLOW:
            tile_asset = assets.images['yellow-tile']

        new_tile = Tile(self.field,
                        asset=tile_asset if tile_pos[0][1] == tile_pos[1][1] else pygame.transform.rotate(tile_asset, 90),
                        color=next_state.cells[tile_pos[0][1]][tile_pos[0][0]].tile,
                        direction=Tile.HORIZONTAL if tile_pos[0][1] == tile_pos[1][1] else Tile.VERTICAL,
                        margin=(self.field.border_size + tile_pos[0][0] * self.field.cell_size,
                                self.field.border_size + tile_pos[0][1] * self.field.cell_size))

        if not self.field.append_tile(new_tile, self):
            raise Exception('AI Exception')

        return True

    def __build_state_tree(self):
        pass

