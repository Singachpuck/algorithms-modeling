import sys
import pygame
from pygame.locals import *

from utils import *

from Assets import Assets as assets

from states.AbstractState import AbstractState

from entities.GameItem import GameItem
from entities.Menu import Menu


class EndState(AbstractState):

    def __init__(self, app):
        super().__init__()

        self.listens_on = {
            'key': self.key_handler
        }

        self.options = [
            {
                'text': 'Try again',
                'color': assets.colors['dark_brown'],
                'background': assets.colors['secondary']
            },
            {
                'text': 'Exit',
                'color': assets.colors['dark_brown'],
                'background': assets.colors['secondary']
            },
        ]

        self.config = app.config
        self.result_size = (600, 400)
        self.result_surf = pygame.Surface(self.result_size)
        self.result_surf.fill(assets.colors['secondary'])
        self.result = GameItem(self.config.display_item,
                               surface=self.result_surf,
                               alignment_hor=Alignment.CENTER,
                               alignment_ver=Alignment.CENTER)
        self.winner = None
        self.menu = Menu(self.result, options=self.options, size=(200, 300), alignment_hor=Alignment.CENTER, margin=(0, 200))

    def on_enter(self, *args, **kwargs):
        self.winner = kwargs['winner']

    def key_handler(self, *args, **kwargs):
        if kwargs['keys'][K_UP]:
            self.menu.current_option = max(0, self.menu.current_option - 1)

        if kwargs['keys'][K_DOWN]:
            self.menu.current_option = min(len(self.menu.options) - 1, self.menu.current_option + 1)

        if kwargs['keys'][K_RETURN]:
            if self.menu.current_option == 0:
                self.config.state_machine.change('menu')
            elif self.menu.current_option == 1:
                pygame.quit()
                sys.exit()

    def render(self):
        self.config.display_surf.blit(assets.images['background'], (0, 0))
        self.result.surface.blit(self.result_surf, (0, 0))

        result_text = assets.fonts['main']['big'].render(self.winner + ' wins!', True, assets.colors['dark_brown'])
        win_text = GameItem(self.result, surface=result_text, alignment_hor=Alignment.CENTER, margin=(0, 20))

        win_text.render()
        self.menu.render()
        self.result.render()
