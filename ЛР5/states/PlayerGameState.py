from Assets import Assets as assets
from states.AbstractState import AbstractState

from utils import *
from entities.Field import Field
from entities.TileSetting import TileSetting
from entities.PvpPlayer import PvpPlayer
from entities.AIPlayer import AIPlayer


class PlayerGameState(AbstractState):

    def __init__(self, app):
        super().__init__()
        self.config = app.config
        self.listens_on = {
            'click': self.click_handler
        }

        self.tile_setting = None
        self.field = None

        self.greaterPlayer = None
        self.smallerPlayer = None
        self.turn = 'greater'

    def on_enter(self, *args, **kwargs):
        self.tile_setting = TileSetting(self.config.display_item,
                                        assets.colors['secondary'],
                                        Alignment.END,
                                        20)

        self.field = Field(self.config.display_item,
                           self.config.field_border_size,
                           assets.images['field'],
                           self.config.cell_size)

        if kwargs['mode'] == 'pvp':
            self.greaterPlayer = PvpPlayer(field=self.field, tile_setting=self.tile_setting)
            self.smallerPlayer = PvpPlayer(field=self.field, tile_setting=self.tile_setting)
        elif kwargs['mode'] == 'pve':
            self.greaterPlayer = PvpPlayer(field=self.field, tile_setting=self.tile_setting)
            self.smallerPlayer = AIPlayer(field=self.field, player_type='smaller', level=kwargs['level'])

        self.turn = 'greater'

    def click_handler(self, *args, **kwargs):
        mouse_x, mouse_y = kwargs['event'].pos

        if self.tile_setting.is_left_arrow_clicked(mouse_x, mouse_y):
            self.tile_setting.left_arrow.clicked()
        elif self.tile_setting.is_right_arrow_clicked(mouse_x, mouse_y):
            self.tile_setting.right_arrow.clicked()
        elif self.tile_setting.is_rotate_button_clicked(mouse_x, mouse_y):
            self.tile_setting.rotate_button.clicked()

        if self.turn == 'greater':
            if self.greaterPlayer.move(event=kwargs['event']):
                self.turn = 'smaller'
        elif self.turn == 'smaller':
            if self.smallerPlayer.move(event=kwargs['event']):
                self.turn = 'greater'

        print(self.field.get_state().count_sections())

        if self.game_end():
            self.config.state_machine.change('end',
                                             winner='Greater Player'
                                             if self.field.get_state().get_static_evaluation() >= 12
                                             else 'Smaller Player')

    def game_end(self):
        return self.field.filled()

    def render(self):
        self.config.display_surf.blit(assets.images['background'], (0, 0))
        self.field.render()
        self.tile_setting.render()
