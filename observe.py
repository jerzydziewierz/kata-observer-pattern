import threading
import time
from queue import Queue
from abc import ABC, abstractmethod
import yaml
import json


class HyObservable(object):
    def __init__(self, name='HyObservable'):
        self.name = name
        self.observers = []
        self.event_queue = Queue()
        self.internal_event_thread = threading.Thread(target=self.internal_generate_events)
        self.incoming_event_thread = threading.Thread(target=self.process_incoming_events)
        self.please_shutdown = False

    def start(self):
        self.internal_event_thread.start()
        self.incoming_event_thread.start()

    def register_observer(self, observer):
        """
        registers an observer to receive notifications from this observable.
        the observer must implement the "notify" method. It must be exactly the method named "notify".
        """
        self.observers.append(observer)

    def observe(self, observable):
        """
        calls the register_observer method of the observable object, passing self as the observer.
        """
        observable.register_observer(self)

    def notify_observers(self, event):
        for observer in self.observers:
            observer.notify(self, event)

    def internal_generate_events(self):
        raise NotImplementedError("Subclasses must implement internal_generate_events method")

    def process_incoming_events(self):
        while not self.please_shutdown:
            sender, event = self.event_queue.get()  # blocks until an event is available. This is thread-safe because the queue is thread-safe.
            self.handle_events(sender, event)

    def handle_events(self, sender, event):
        raise NotImplementedError("Subclasses must implement handle_events method")

    def notify(self, sender, event):
        """
        Puts the event data into the event queue, to be processed by the `handle_events` method, animated by the internal "incoming_event_thread".

        Note that no actual processing is done here, ever. This procedure is animated by the sender's thread, and we must not hog that thread.
        Notifications are supposed to return immediately.

        Hence, actual signal processing is done in the `handle_events` method animated by own thread.
        """
        self.event_queue.put((sender, event))

    def stop(self):
        self.please_shutdown = True
        self.notify(self, Ellipsis)  # unblock the incoming_event_thread
        self.internal_event_thread.join()
        self.incoming_event_thread.join()


class TimedEventSource(HyObservable):
    def __init__(self, name='timer', interval=1.0):
        super().__init__(name=name)
        self.interval = interval

    def internal_generate_events(self):
        while not self.please_shutdown:
            time.sleep(self.interval)
            eventData = f'time: {time.strftime('%H:%M:%S')}'
            print(f'timerEventSource|internal| creating event {eventData} and notifying observers')
            self.notify_observers(eventData)

    def handle_events(self, sender, eventData):
        if eventData is not Ellipsis:
            print(f"timerEventSource|handlder| received event: {eventData} from {sender.name}")
        else:  # this is the last event before shutdown. Do any cleanup here.
            print("timerEventSource|handler| received shutdown signal")


class DataItemsSource(HyObservable):
    def __init__(self, name='data', data_source=(1, 2, 3)):
        super().__init__(name=name)
        self.data_source = data_source

    def internal_generate_events(self):
        time.sleep(0.5)
        for data in self.data_source:
            if self.please_shutdown:
                break
            eventData = f"{data}"
            print(f'DataEventSource|internal| creating event {eventData} and notifying observers')
            self.notify_observers(eventData)
            time.sleep(1)
        print('DataEventSource|internal| finished generating events')
        self.please_shutdown = True

    def handle_events(self, sender, eventData):
        if eventData is Ellipsis and sender is self:
            print("DataEventSource|handler| received shutdown signal")
            return
        if sender is not self:
            print(f"DataEventSource|handler| received event: {eventData} from {sender.name}")
        else:
            print(f'DataEventSource|handler| received self-message.')


class ItemPrinter(HyObservable):
    def __init__(self, name='itemPrinter'):
        super().__init__(name=name)

    def internal_generate_events(self):
        pass

    def handle_events(self, sender, eventData):
        if eventData is Ellipsis and sender is self:
            print("ItemPrinter|handler| received shutdown signal")
            return
        print(f"ItemPrinter|handler| received event: {eventData} from {sender.name}")


class YamlLogger(HyObservable):
    """
    on event, attempts to convert the event data to yaml, and stores to a file.
    on shutdown, closes the file and also prints the result.
    """

    def __init__(self, name='yaml_logger', filename='eventLog.yaml'):
        super().__init__(name=name)
        self.event_counter = 0
        self.filename = filename
        self.file = open(filename, 'w')
        self.file.write('---\n')

    def internal_generate_events(self):
        pass

    def handle_events(self, sender, eventData):
        # shutdown cleanup mode:
        if eventData is Ellipsis and sender is self:
            print("yamlLogger|handler| received shutdown signal")
            self.file.close()
            with open(self.filename, 'r') as f:
                print(f.read())
            print(f"yamlLogger|handler| file closed and contents printed")
            return

        # normal operation.
        self.event_counter += 1
        eventPacket = {'sender': sender.name, 'event': eventData}
        yaml.dump(eventPacket, self.file)
        # add a separator
        self.file.write('---\n')
        self.notify_observers({'event_counter': self.event_counter})


class jsonlLogger(HyObservable):
    def __init__(self, name='json_logger', filename='eventLog.jsonl'):
        super().__init__(name=name)
        self.filename = filename
        self.file = open(filename, 'w')

    def internal_generate_events(self):
        pass

    def handle_events(self, sender, eventData):
        if eventData is Ellipsis and sender is self:
            print("jsonlLogger|handler| received shutdown signal")
            self.file.close()
            with open(self.filename, 'r') as f:
                print(f.read())
            print(f"jsonlLogger|handler| file closed and contents printed")
            return

        eventPacket = {'sender': sender.name, 'event': eventData}
        self.file.write(json.dumps(eventPacket) + '\n')


class DataProcessingStep(HyObservable):
    """
    This is a simple data processor that receives data events, and processes them, then notifies listeners with the processed data.
    """

    def __init__(self, name='dataProcessorStep1'):
        super().__init__(name=name)

    def internal_generate_events(self):
        pass

    def handle_events(self, sender, eventData):
        if eventData is Ellipsis and sender is self:
            print("DataProcessorStep1|handler| received shutdown signal")
            return
        processedData = f"processed:{eventData}, len={len(str(eventData))}"
        print(
            f"DataProcessorStep1|handler| received event: {eventData} from {sender.name}, and processed it to {processedData}")
        self.notify_observers(processedData)


# Usage example:

# create instances of the modules
src_timer = TimedEventSource(interval=1)
src_data = DataItemsSource(data_source=[1, 2, {'some': 'data'}, 4, 5, 'data6', 'data7', 'data8'])
item_printer = ItemPrinter()
yaml_logger = YamlLogger(filename='eventLog.yaml')
jsonl_logger = jsonlLogger(filename='eventLog.jsonl')
data_processor1 = DataProcessingStep(name='step1')
data_processor2 = DataProcessingStep(name='step2')
data_processor3 = DataProcessingStep(name='step3')

# list the modules so that they can be gathered and reasoned about together.
modules = [src_timer, src_data, item_printer, yaml_logger, jsonl_logger, data_processor1, data_processor2,
           data_processor3]

# register connections

src_data.observe(src_timer)
src_timer.observe(src_data)

src_data.observe(src_data)  # This is a self-loop. Timer shall respond to timer events.
src_timer.observe(src_timer)  # This is a self-loop. Data shall respond to data events.

item_printer.observe(src_data)
item_printer.observe(src_timer)

yaml_logger.observe(src_timer)
yaml_logger.observe(src_data)
yaml_logger.observe(item_printer)

data_processor1.observe(src_data)
data_processor2.observe(data_processor1)
data_processor3.observe(data_processor2)
jsonl_logger.observe(data_processor3)

yaml_logger.observe(data_processor1)
yaml_logger.observe(data_processor2)
yaml_logger.observe(data_processor3)
jsonl_logger.observe(yaml_logger)

# start the system
for module in modules:
    module.start()

# let the system run for a while
import time

time.sleep(2)

# stop the threads
for module in modules:
    module.stop()
