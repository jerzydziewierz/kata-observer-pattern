import cython
from .observable import Observable
from .datatypes import Config
from .datatypes import SomeData


class ExampleProcessor(Observable):
    """
    This is a simple data processor that receives data events and processes them,
    Then notifies listeners with the processed data.
    """

    def __init__(self, name='unsetDataProcessor', verbose=False):
        super().__init__(name=name)
        self.verbose = verbose

    def internal_generate_events(self):
        pass

    def handle_events(self, sender, eventData):
        if eventData is Ellipsis and sender is self:
            if self.verbose:
                print(f"H|DataProcessor-{self.name}| received shutdown signal")
            return

        # do the actual processing here.
        if isinstance(eventData, SomeData):
            newValue = SomeData(value=eventData.value * eventData.value + 1, source=self.name)
            processedData = newValue
            if self.verbose:
                print(
                    f"H|DataProcessor-{self.name}| received event: {eventData} from {sender.name}, and processed it to {processedData}")
            self.notify_observers(processedData)
        else:
            raise ValueError(f"H|DataProcessor-{self.name}| received an unexpected event: {eventData} of type {type(eventData)}")


