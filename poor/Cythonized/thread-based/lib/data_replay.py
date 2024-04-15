import cython
from .observable import Observable
from .timer import TimedEventSource
import time


class DataReplay(Observable):
    def __init__(self,
                 name='data',
                 data_source=(1, 2, 3),
                 verbose=False):
        super().__init__(name=name)
        self.data_source = data_source
        self.data_gen = self.data_generator()
        self.verbose = verbose

    def internal_generate_events(self):
        pass

    def data_generator(self):
        yield from self.data_source

    def handle_events(self, sender, eventData):
        if eventData is Ellipsis and sender is self:
            if self.verbose:
                print("DataEventSource|handler| received shutdown signal")
            return

        if sender is self:
            if self.verbose:
                print(f"DataEventSource|handler| received self-message.")
            return

        # if the source of the event is a timer, emit a data event
        if isinstance(sender, TimedEventSource):
            try:
                eventData = self.data_gen.__next__()
                if self.verbose:
                    print(f'DataItemsSource|internal| creating event {eventData} and notifying observers')
                self.notify_observers(eventData)
                return
            except StopIteration:
                if self.verbose:
                    print('DataEventSource|internal| finished generating events')
                self.please_shutdown = True
                return

        raise ValueError(f'DataEventSource|handler| unhandled event from {sender.name} with data: {eventData}')
