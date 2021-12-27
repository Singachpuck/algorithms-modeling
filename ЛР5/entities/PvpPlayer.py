from entities.Player import Player


class PvpPlayer(Player):

    def __init__(self, *, field, tile_setting):
        super().__init__(field)
        self.tile_setting = tile_setting

    def move(self, *args, **kwargs):
        mouse_x, mouse_y = kwargs['event'].pos

        if self.field.is_sheet_coords(mouse_x, mouse_y):
            tile = self.tile_setting.get_tile(self.field, self.field.get_cell_coords(mouse_x, mouse_y))
            return self.field.append_tile(tile, self)

        return False
