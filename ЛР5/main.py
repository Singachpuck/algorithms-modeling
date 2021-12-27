import pygame
from pygame.locals import *

from pydispatch import Dispatcher

from Assets import Assets as assets

from states.MenuState import MenuState
from states.PlayerGameState import PlayerGameState
from states.EndState import EndState
from StateMachine import StateMachine

from entities.GameItem import GameItem


class App(Dispatcher):
    _events_ = ['click', 'key']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._running = True
        self.config = AppConfiguration()

    def on_init(self):
        pygame.init()
        pygame.display.set_caption('Linkage')
        pygame.display.set_icon(assets.images['icon'])

        assets.fonts['main']['small'] = pygame.font.SysFont('inkfree', 16)
        assets.fonts['main']['medium'] = pygame.font.SysFont('inkfree', 24)
        assets.fonts['main']['big'] = pygame.font.SysFont('inkfree', 36)

        self.config.display_surf = pygame.display.set_mode(self.config.size)
        self.config.display_item = GameItem(None, surface=self.config.display_surf, copy_surface=False)

        assets.images = dict(map(lambda key: (key, assets.images[key].convert_alpha()), assets.images))

        self.config.state_machine = StateMachine({
            'menu': MenuState(self),
            'player_game': PlayerGameState(self),
            'end': EndState(self)
        })

        self.bind(click=self.config.state_machine.click_event, key=self.config.state_machine.key_event)

        self.config.state_machine.change('menu')

        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        keys = pygame.key.get_pressed()

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.emit('click', event=event)

        self.emit('key', keys=keys)

    def on_loop(self, rate):
        self.config.state_machine.update(rate)

    def on_render(self):
        self.config.state_machine.render()
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            rate = self.config.clock.tick(self.config.fps)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop(rate)
            self.on_render()

        self.on_cleanup()


class AppConfiguration:

    def __init__(self):
        self.display_surf = None
        self.display_item = None
        self.size = self.width, self.height = 1024, 500
        self.field_border_size = 27
        self.cell_size = 45
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.state_machine = None


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
