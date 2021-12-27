from utils import *

from entities.GameItem import GameItem

from Assets import Assets as assets


class Board(GameItem):

    def __init__(self, parent, size, margin=(0, 115)):
        super().__init__(parent, size=size, alignment_hor=Alignment.CENTER, margin=margin)

        self.cells = [[None for _ in range(8)] for _ in range(4)]

        self.cell_size = (63, 91)
        self.gap_x = 0.5 * 63
        self.gap_y = 9
        self.current = (0, 0)
        self.last_card = None

    def clear(self):
        self.cells = [[None for _ in range(8)] for _ in range(4)]

        self.current = (0, 0)
        self.surface = self.clean_surface.copy()

    def append(self, card):
        self.cells[self.current[0]][self.current[1]] = card
        self.last_card = card
        self.current = (self.current[0], self.current[1] + 1) if self.current[1] + 1 < 8 else (self.current[0] + 1, 0)

    def get_cards(self):
        cards = []

        for cell_row in self.cells:
            for cell in cell_row:
                if cell is None:
                    break

                cards.append(cell)
            else:
                continue
            break

        self.clear()

        return cards

    def render(self):

        i = 0
        j = 0

        for cell_row in self.cells:
            for cell in cell_row:
                if cell is None:
                    break

                self.surface.blit(pygame.transform.scale(assets.images['cards'][cell], self.cell_size),
                                  (j * (self.cell_size[0] + self.gap_x), i * (self.cell_size[1] + self.gap_y)))

                j += 1
            else:
                j = 0
                i += 1
                continue
            break

        super().render()

