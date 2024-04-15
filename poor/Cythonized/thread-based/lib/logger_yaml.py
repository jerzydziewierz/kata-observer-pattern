import cython
from .observable import Observable
import yaml


class LoggerYaml(Observable):
    """
    on event, attempts to convert the event data to yaml, and stores to a file.
    on shutdown, closes the file and also prints the result.
    """

    def __init__(self, name='yaml_logger', filename='eventLog.yaml', verbose=False):
        super().__init__(name=name)
        self.event_counter = 0
        self.verbose = verbose
        self.filename = filename
        self.file = open(filename, 'w')
        self.file.write('---\n')

    def internal_generate_events(self):
        """no self-sourced events."""
        pass

    def handle_events(self, sender, eventData):
        # shutdown cleanup mode:
        if eventData is Ellipsis and sender is self:
            print("H|LoggerYaml| received shutdown signal")
            self.file.close()
            with open(self.filename, 'r') as f:
                print(f.read())
            print(f"H|LoggerYaml| file closed and contents printed")
            return

        # normal operation.
        self.event_counter += 1
        eventPacket = {'sender': sender.name, 'event': eventData}
        yaml.dump(eventPacket, self.file)
        # add a separator
        self.file.write('---\n')
        self.notify_observers({'event_counter': self.event_counter})
