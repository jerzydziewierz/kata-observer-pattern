import threading
import time
from queue import Queue
from abc import ABC, abstractmethod
import yaml
import json
from .datatypes import Config


class Observable(object):
    def __init__(self, name='observable-base'):
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