import pygame

from Assets import Assets as assets

from entities.GameItem import GameItem


class Option(GameItem):

    def __init__(self, parent, text_dict, height, y_margin):
        super().__init__(parent, size=(parent.surface.get_width(), height), margin=(0, y_margin))

        self.surface.fill(text_dict['background'])

        self.text_dict = text_dict

    def render(self):
        text = assets.fonts['main']['medium'].render(self.text_dict['text'], True, self.text_dict['color'])
        text_coords = ((self.surface.get_width() - text.get_width()) / 2,
                       (self.surface.get_height() - text.get_height()) / 2)

        self.surface.blit(text, text_coords)

        super().render()
