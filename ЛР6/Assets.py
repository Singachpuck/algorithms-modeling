import pygame

from utils import *


class Assets:

    fonts = {
        'main': {
            'small': None,
            'medium': None,
            'big': None
        }
    }

    images = {
        'icon': pygame.image.load('assets/icon.png'),
        'board': pygame.image.load('assets/board.jpg'),
        'cards': organize_cards(list(map(lambda img: pygame.transform.scale(img, (63 * 1.5, 91 * 1.5)),
                                         cut_out_tiles(pygame.image.load('assets/cards.png'),
                                                       (0, 0), (63, 91), (0, 0))))),
        'card_back': pygame.transform.scale(pygame.image.load('assets/card_back.png'), (63 * 1.5, 91 * 1.5)),
        'arrow': pygame.transform.scale(pygame.image.load('assets/arrow.png'), (50, 50)),
        'end_turn': pygame.image.load('assets/end_button.png'),
        'accept': pygame.image.load('assets/accept.png')
    }

    colors = {
        'dark': pygame.Color('#7F5443'),
        'light': pygame.Color('#ffffff')
    }
