import random

import pygame

from utils import *

from entities.PvpPlayer import PvpPlayer
from entities.AIPlayer import AIPlayer
from entities.YourCards import YourCards
from entities.Board import Board
from entities.Button import Button
from entities.EnemyBoard import EnemyBoard

from states.AbstractState import AbstractState

from Assets import Assets as assets


class PlayerGameState(AbstractState):

    def __init__(self, app):
        super().__init__()

        self.listens_on = {
            'click': self.click_handler
        }

        self.config = app.config
        self.board = Board(self.config.display_item, (8 * 63 * 1.5, 4 * 100))
        self.beat_board = Board(self.config.display_item, (8 * 63 * 1.5, 4 * 100), margin=(0, 130))
        self.player1 = PvpPlayer()
        self.player2 = AIPlayer(player_type='smaller', level='easy', board1=self.board, board2=self.beat_board)
        self.current_card = None
        self.turn = None
        self.your_cards = YourCards(self.player1,
                                    self.config.display_item,
                                    size=(self.config.display_surf.get_width(), 91 * 1.5))

        self.enemy_cards = EnemyBoard(self.player2,
                                      self.config.display_item,
                                      size=(self.config.display_surf.get_width(), 91 * 1.5))
        self.state = 'move'

        def end_turn():
            self.board.get_cards()
            self.beat_board.get_cards()

        self.end_turn = Button(click_handler=end_turn,
                               parent=self.config.display_item,
                               asset=assets.images['end_turn'],
                               alignment_hor=Alignment.END,
                               alignment_ver=Alignment.END,
                               margin=(0, 200))

        def accept():
            self.player1.cards.extend(self.board.get_cards())
            self.player1.cards.extend(self.beat_board.get_cards())

        self.accept_btn = Button(click_handler=accept,
                                 parent=self.config.display_item,
                                 asset=assets.images['accept'],
                                 alignment_hor=Alignment.END,
                                 alignment_ver=Alignment.END,
                                 margin=(0, 300))

    def on_enter(self, *args, **kwargs):
        self.turn = random.randint(1, 2)
        random.shuffle(deck)
        self.player1.cards = deck[:int(len(deck) / 2)]
        self.player2.cards = deck[int(len(deck) / 2):]

        print(len(self.player1.cards), len(self.player2.cards), int(len(deck) / 2))

        self.exchange()

    def exchange(self):
        player1_cards_to_give = []
        player2_cards_to_give = []

        if self.player1.suit:
            for card in self.player1.cards:
                if card in black_cards:
                    player1_cards_to_give.append(card)
                    self.player1.cards.remove(card)
        else:
            for card in self.player1.cards:
                if card in red_cards:
                    player1_cards_to_give.append(card)
                    self.player1.cards.remove(card)

        if self.player2.suit:
            for card in self.player2.cards:
                if card in black_cards:
                    player2_cards_to_give.append(card)
                    self.player2.cards.remove(card)
        else:
            for card in self.player2.cards:
                if card in red_cards:
                    player2_cards_to_give.append(card)
                    self.player2.cards.remove(card)

        self.player1.cards.extend(player2_cards_to_give)
        self.player2.cards.extend(player1_cards_to_give)

    def click_handler(self, *args, **kwargs):
        pos = kwargs['event'].pos
        if self.your_cards.left_arrow.is_clicked(pos):
            self.your_cards.left_arrow.clicked()
        elif self.your_cards.right_arrow.is_clicked(pos):
            self.your_cards.right_arrow.clicked()

        if self.turn == 1:
            if self.state == 'move' and self.end_turn.is_clicked(pos):
                self.end_turn.clicked()
                self.turn = 2
                return

            if self.state == 'beat' and self.accept_btn.is_clicked(pos):
                self.state = 'move'
                self.accept_btn.clicked()
                self.turn = 2
                return

            if self.your_cards.is_clicked(pos):
                card = self.your_cards.get_card(pos)

                if card is not None:
                    if self.state == 'move':
                        if self.board.cells[0][0] is None or self.suit_for_move(card):
                            self.board.append(card)
                            self.state = 'beat'
                            self.player1.cards.remove(card)
                            self.turn = 2
                    else:
                        if self.suit_card(card, self.player1.trump):
                            self.beat_board.append(card)
                            self.state = 'move'
                            self.player1.cards.remove(card)
                            self.turn = 2

                if len(self.player1.cards) == 0:
                    self.config.state_machine.change('end', winner=1)
        else:
            card = self.player2.move(state=self.state, to_beat=self.board.last_card)

            if card == 'end':
                self.board.get_cards()
                self.beat_board.get_cards()
                self.state = 'move'
                self.turn = 1
                return

            if card is None:
                self.player2.cards.extend(self.board.get_cards())
                self.player2.cards.extend(self.beat_board.get_cards())
                self.state = 'move'
                self.turn = 1
                return

            if self.state == 'move':
                self.board.append(card)
                self.state = 'beat'
                self.turn = 1
            else:
                self.beat_board.append(card)
                self.state = 'move'
                self.turn = 1

            self.player2.cards.remove(card)

            if len(self.player2.cards) == 0:
                self.config.state_machine.change('end', winner=2)

    def suit_card(self, card, trump):
        card_to_beat = self.board.last_card

        return get_suit(card) == get_suit(card_to_beat) or get_suit(card) == trump

    def suit_for_move(self, card):
        cards_on_boards = []

        for cell_row in self.board.cells:
            for cell in cell_row:
                if cell is None:
                    break

                cards_on_boards.append(cell)

        for cell_row in self.beat_board.cells:
            for cell in cell_row:
                if cell is None:
                    break

                cards_on_boards.append(cell)

        for c in cards_on_boards:
            if is_same_number(c, card):
                return True

        return False

    def render(self):
        self.config.display_surf.blit(pygame.transform.scale(assets.images['board'], self.config.size), (0, 0))

        self.board.render()
        self.beat_board.render()
        self.end_turn.render()
        self.accept_btn.render()

        self.config.display_surf.blit(pygame.transform.rotate(assets.images['arrow'], -90 if self.turn == 2 else 90),
                                      (10, get_axis_center_coords(self.config.height,
                                                                  assets.images['arrow'].get_height())))

        self.your_cards.render()
        self.enemy_cards.render()
