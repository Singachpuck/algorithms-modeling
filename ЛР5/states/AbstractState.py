
class AbstractState:

    def __init__(self):
        self.listens_on = {}

    def on_enter(self, *args, **kwargs):
        pass

    def on_exit(self, *args, **kwargs):
        pass

    def update(self, rate):
        pass

    def render(self):
        pass
