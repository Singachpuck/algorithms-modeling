import pygame


class Assets:
    images = {
        'field': pygame.image.load('assets/field.png'),
        'red-tile': pygame.image.load('assets/red-tile.gif'),
        'green-tile': pygame.image.load('assets/green-tile.gif'),
        'blue-tile': pygame.image.load('assets/blue-tile.gif'),
        'yellow-tile': pygame.image.load('assets/yellow-tile.gif'),
        'arrow': pygame.transform.scale(pygame.image.load('assets/arrow.png'), (50, 50)),
        'rotate': pygame.transform.scale(pygame.image.load('assets/rotate.png'), (50, 50)),
        'background': pygame.image.load('assets/background.jpg'),
        'icon': pygame.image.load('assets/icon.jpg')
    }

    colors = {
        'secondary': pygame.Color('#E9C085'),
        'dark_brown': pygame.Color('#7F5443')
    }

    fonts = {
        'main': {
            'small': None,
            'medium': None,
            'big': None,
        }
    }

