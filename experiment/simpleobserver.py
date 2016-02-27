from rx.observer import Observer


class SimpleObserver(Observer):
    def __init__(self):
        super().__init__()

    def on_next(self, value):
        print('Observing {}'.format(value))
