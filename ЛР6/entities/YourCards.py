from utils import *
from entities.GameItem import GameItem
from entities.Button import Button
from Assets import Assets as assets


class YourCards(GameItem):

    def __init__(self, player, parent, *, size):
        super().__init__(parent, size=size, alignment_hor=Alignment.CENTER, alignment_ver=Alignment.END)

        self.player = player

        self.left_arrow = Button(
            self.left_arrow_clicked,
            parent=self,
            asset=assets.images['arrow'],
            alignment_ver=Alignment.CENTER,
            margin=(20, 0)
        )

        self.right_arrow = Button(
            self.right_arrow_clicked,
            parent=self,
            asset=pygame.transform.flip(assets.images['arrow'], True, False),
            alignment_hor=Alignment.END,
            alignment_ver=Alignment.CENTER,
            margin=(20, 0)
        )

        self.board = pygame.Surface((8 * 63 * 1.5, size[1]), pygame.SRCALPHA, 32).convert_alpha()
        self.offset = 0
        self.card_size = 8

    def left_arrow_clicked(self):
        self.offset = max(0, self.offset - 1)

    def right_arrow_clicked(self):
        self.offset = min(len(self.player.cards) - self.card_size if len(self.player.cards) - self.card_size > 0 else 0,
                          self.offset + 1)

    def get_card(self, pos):
        point = (pos[0] - self.absolute_coords[0], pos[1] - self.absolute_coords[1])

        board_coords = get_center_coordinates(self.surface.get_size(),
                                              self.board.get_size())

        if not pygame.Rect(board_coords,
                           self.board.get_size()).collidepoint(point):
            return None

        return self.player.cards[int((point[0] - board_coords[0]) / (63 * 1.5)) + self.offset]

    def render(self):
        self.surface = self.clean_surface.copy()
        self.board = pygame.Surface((8 * 63 * 1.5, self.surface.get_height()), pygame.SRCALPHA, 32).convert_alpha()
        self.left_arrow.render()
        self.right_arrow.render()

        i = 0
        for card in self.player.cards[self.offset:]:
            self.board.blit(assets.images['cards'][card], (i * 63 * 1.5, 0))
            i += 1

        self.surface.blit(self.board, get_center_coordinates(self.surface.get_size(), self.board.get_size()))

        super().render()
