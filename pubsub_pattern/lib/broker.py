import threading
import time
from queue import Queue
from abc import ABC, abstractmethod
from typing import Callable, ClassVar
from attr import dataclass, field


Broker = ClassVar

@dataclass
class Agent(ABC):
    broker: Broker = None
    pass


@dataclass
class Subscription:
    callback: Callable


class Broker(object):
    def __init__(self):
        # topics is a dict with key->list of Subscription.
        self.topics: dict[str, list[Subscription]] = {}

    def subscribe(self, topic, callback):
        # get the list and extend it, and if not, create a fresh one.
        subscriptions = self.topics.get(topic, [])
        subscription = Subscription(callback=callback)
        subscriptions.append(subscription)
        self.topics[topic] = subscriptions
        return None

    def unsubscribe(self, topic, callback):
        subscriptions = self.topics.get(topic, [])
        for item in subscriptions:
            if item.callback == callback:
                subscriptions.remove(item)
        return None

    def publish(self, topic, message):
        for subscription in self.topics.get(topic, []):
            subscription.callback(message)
