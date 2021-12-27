from states.AbstractState import AbstractState


class StateMachine:

    def __init__(self, states):
        self.current = AbstractState()
        self.__states = states

    def change(self, state, **kwargs):
        self.current.on_exit()
        self.current = self.__states[state]
        self.current.on_enter(**kwargs)

    def update(self, rate):
        self.current.update(rate)

    def render(self):
        self.current.render()

    def click_event(self, *args, **kwargs):
        if 'click' in self.current.listens_on:
            self.current.listens_on['click'](*args, **kwargs)

    def key_event(self, *args, **kwargs):
        if 'key' in self.current.listens_on:
            self.current.listens_on['key'](*args, **kwargs)
