import sys

from pygame.locals import *

from utils import *

from Assets import Assets as assets

from states.AbstractState import AbstractState

from entities.Menu import Menu


class MenuState(AbstractState):

    def __init__(self, app):
        super().__init__()
        self.config = app.config

        self.listens_on = {
            'key': self.key_handler
        }

        self.options = [
            {
                'text': 'PvP',
                'color': assets.colors['dark_brown'],
                'background': assets.colors['secondary']
            },
            {
                'text': 'PvE',
                'color': assets.colors['dark_brown'],
                'background': assets.colors['secondary']
            },
            {
                'text': 'Exit',
                'color': assets.colors['dark_brown'],
                'background': assets.colors['secondary']
            },
        ]

        self.menu = None

    def on_enter(self, *args, **kwargs):
        self.menu = Menu(self.config.display_item,
                         options=self.options,
                         size=(200, 300),
                         alignment_ver=Alignment.CENTER,
                         alignment_hor=Alignment.CENTER)

    def key_handler(self, *args, **kwargs):
        if kwargs['keys'][K_UP]:
            self.menu.current_option = max(0, self.menu.current_option - 1)

        if kwargs['keys'][K_DOWN]:
            self.menu.current_option = min(len(self.menu.options) - 1, self.menu.current_option + 1)

        if kwargs['keys'][K_RETURN]:
            if self.menu.current_option == 0:
                self.config.state_machine.change('player_game', mode='pvp')
            elif self.menu.current_option == 1:
                self.config.state_machine.change('player_game', mode='pve', level='easy')
            elif self.menu.current_option == 2:
                pygame.quit()
                sys.exit()

    def render(self):
        self.config.display_surf.blit(assets.images['background'], (0, 0))
        self.menu.render()
