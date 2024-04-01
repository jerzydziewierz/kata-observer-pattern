from .observable import Observable
from .datatypes import SomeData
import time

class TimedEventSource(Observable):
    def __init__(self, name='timer', interval=1.0, verbose=False):
        super().__init__(name=name)
        self.interval = interval
        self.verbose = verbose

    def internal_generate_events(self):
        while not self.please_shutdown:
            time.sleep(self.interval)
            eventData = SomeData(value=self.interval)
            if self.verbose:
                print(f'timerEventSource|internal| creating event {eventData} and notifying observers')
            self.notify_observers(eventData)

    def handle_events(self, sender, eventData):
        if eventData is not Ellipsis:
            if self.verbose:
                print(f"timerEventSource|handlder| received event: {eventData} from {sender.name}")
        else:  # this is the last event before shutdown. Do any cleanup here.
            if self.verbose:
                print("timerEventSource|handler| received shutdown signal")
