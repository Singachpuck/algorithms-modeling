import copy
import math
import queue
import random
from utils import *


class StateTree:

    def __init__(self, depth, player, trump, board1, board2):
        self.depth = depth
        self.player = player
        self.trump = trump
        self.board1 = board1
        self.board2 = board2

    def minimax(self, node, depth, alpha, beta, minmax):
        if depth == 0 or not node.generate_children():
            return node.get_static_evaluation()

        if not minmax:
            max_eva = -math.inf

            for child in node.children:
                eva = self.minimax(child, depth - 1, alpha, beta, True)

                max_eva = max(max_eva, eva)
                alpha = max(alpha, max_eva)

                if beta <= alpha:
                    break

            return max_eva
        else:
            min_eva = math.inf
            for child in node.children:
                eva = self.minimax(child, depth - 1, alpha, beta, False)
                min_eva = min(min_eva, eva)
                beta = min(beta, eva)
                if beta <= alpha:
                    break
            return min_eva

    def get_next(self, state, to_beat=None):
        start_state = State(None, self.player.cards, self.trump, state, False, self.board1, self.board2)

        start_state.generate_children()

        if len(start_state.children) == 0 and state == 'beat':
            return None

        if len(start_state.children) == 0 and state == 'move':
            return 'end'

        if start_state.minmax:
            return min(start_state.children,
                       key=lambda child: self.minimax(child, self.depth, -math.inf, math.inf,
                                                      not start_state.minmax))
        else:
            return max(start_state.children,
                       key=lambda child: self.minimax(child, self.depth, -math.inf, math.inf,
                                                      not start_state.minmax))


class State:

    def __init__(self, parent, cards, trump, state, minmax, board1, board2, to_beat=None):
        self.parent = parent
        self.cards = cards
        self.minmax = minmax
        self.children = []
        self.alpha = -math.inf
        self.beta = math.inf
        self.cells_number = len(cards)
        self.processed = False
        self.trump = trump
        self.state = state
        self.to_beat = to_beat
        self.board1 = board1
        self.board2 = board2

    def suit_for_move(self, card):
        if self.board1.cells[0][0] is None:
            return True

        cards_on_boards = []

        for cell_row in self.board1.cells:
            for cell in cell_row:
                if cell is None:
                    break

                cards_on_boards.append(cell)

        for cell_row in self.board2.cells:
            for cell in cell_row:
                if cell is None:
                    break

                cards_on_boards.append(cell)

        for c in cards_on_boards:
            if is_same_number(c, card):
                return True

        return False

    def generate_children(self):
        self.children.clear()

        if self.state == 'move':
            cards = list(filter(lambda c: self.suit_for_move(c), self.cards))

            for card in cards:
                cds = self.cards[:]
                cds.remove(card)
                self.children.append(
                    State(self, cds, self.trump, 'move', False, self.board1, self.board2)
                )
        else:
            cards = list(filter(lambda c: self.suit_card(c), self.cards))

            for card in cards:
                cds = self.cards[:]
                cds.remove(card)
                self.children.append(
                    State(self, cds, self.trump, 'move', False, self.board1, self.board2)
                )

    def get_min(self):
        return min(map(lambda state: state.get_static_value(), self.children))

    def get_max(self):
        return max(map(lambda state: state.get_static_value(), self.children))

    def count_trumps(self):
        return len(tuple(filter(lambda card: get_suit(card) == self.trump, self.cards)))

    def count_cards(self):
        return len(self.cards)

    def get_static_evaluation(self):
        return self.count_trumps() + self.count_cards()

    def suit_card(self, card):
        return get_suit(card) == get_suit(self.board1.last_card) or get_suit(card) == self.trump
