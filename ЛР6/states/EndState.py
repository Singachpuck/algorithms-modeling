import pygame

from Assets import Assets as assets
from entities.GameItem import GameItem

from states.AbstractState import AbstractState
from utils import Alignment


class EndState(AbstractState):

    def __init__(self, app):
        super().__init__()
        self.config = app.config
        self.winner = None

    def on_enter(self, *args, **kwargs):
        self.winner = kwargs['winner']

    def render(self):
        self.config.display_surf.blit(pygame.transform.scale(assets.images['board'], self.config.size), (0, 0))

        if self.winner == 1:
            text = 'You win!'
        else:
            text = 'AI wins!'

        result_text = assets.fonts['main']['big'].render(text, True, assets.colors['dark'])
        win_text = GameItem(self.config.display_item, surface=result_text, alignment_hor=Alignment.CENTER, margin=(0, 20))

        win_text.render()

