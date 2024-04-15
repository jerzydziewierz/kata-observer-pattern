from .observable import Observable
from .datatypes import SomeData
import json


class LoggerJsonl(Observable):
    def __init__(self, name='json_logger', filename='eventLog.jsonl'):
        super().__init__(name=name)
        self.filename = filename
        self.file = open(filename, 'w')

    def internal_generate_events(self):
        """no self-sourced events."""
        pass

    def handle_events(self, sender, eventData):
        if eventData is Ellipsis and sender is self:
            print("H|jsonlLogger| received shutdown signal")
            self.file.close()
            with open(self.filename, 'r') as f:
                print(f.read())
            print(f"H|jsonlLogger| file closed and contents printed")
            return
        if isinstance(eventData, SomeData):
            from attr import asdict
            eventPacket = {'sender': sender.name, 'event': asdict(eventData)}
        else:
            eventPacket = {'sender': sender.name, 'event': str(eventData)}
        self.file.write(json.dumps(eventPacket) + '\n')