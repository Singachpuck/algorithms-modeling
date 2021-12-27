from entities.Player import Player

from structures.StateTree import *


class AIPlayer(Player):

    def __init__(self, *, player_type, level, board1, board2):
        super().__init__()
        self.minmax = player_type == 'smaller'

        if level == 'hard':
            self.depth = 3
        elif level == 'medium':
            self.depth = 2
        else:
            self.depth = 1

        self.state_tree = StateTree(self.depth, self, self.trump, board1, board2)

    def move(self, *args, **kwargs):
        res = self.state_tree.get_next(kwargs['state'])

        if res is None or res == 'end':
            return res

        cards = res.cards

        diff_card = None

        for card in self.cards:
            if card not in cards:
                diff_card = card
                break

        return diff_card
