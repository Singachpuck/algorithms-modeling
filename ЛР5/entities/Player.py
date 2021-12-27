import abc


class Player:

    def __init__(self, field):
        self.field = field
        self.blocked = False

    @abc.abstractmethod
    def move(self, *args, **kwargs):
        pass
