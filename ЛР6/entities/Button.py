from entities.GameItem import GameItem
from utils import *


class Button(GameItem):

    def __init__(self, click_handler, *,
                 parent,
                 asset,
                 alignment_hor=Alignment.START,
                 alignment_ver=Alignment.START,
                 margin=(0, 0)):
        super().__init__(parent,
                         surface=asset,
                         alignment_hor=alignment_hor,
                         alignment_ver=alignment_ver,
                         margin=margin)
        self.click_handler = click_handler

    def clicked(self):
        self.click_handler()
