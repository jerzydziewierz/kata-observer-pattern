import cython
from .observable import Observable


class EventPrinter(Observable):
    def __init__(self, name='event-printer'):
        super().__init__(name=name)

    def internal_generate_events(self):
        pass

    def handle_events(self, sender, eventData):
        if eventData is Ellipsis and sender is self:
            print("H|EventPrinter| received shutdown signal")
            return
        print(f"H|EventPrinter| from {sender.name}:{type(sender)} -> observed {eventData}")
