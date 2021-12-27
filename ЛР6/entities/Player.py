import abc
import random

"""
Suit:
    0 - Темна
    1 - Червона
Trump:
    1 - Піка
    2 - Хреста
    3 - Буба
    4 - Чирва
"""


class Player:

    def __init__(self):
        self.cards = []
        self.suit = random.randint(0, 1)
        self.trump = random.randint(0, 3)

    @abc.abstractmethod
    def move(self, *args, **kwargs):
        pass
