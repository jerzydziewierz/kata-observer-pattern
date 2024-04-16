import threading
import time
from queue import Queue
from abc import ABC, abstractmethod
from typing import Callable, ClassVar
from attr import dataclass, field

from ..brokerwrapper import Subscription
from ..brokerwrapper import BrokerWrapper


class MessagePrint:
    def __init__(self, broker: BrokerWrapper = None, print_topics=['TimeTickAgent/tick', 'pleaseStop']):
        self.name = 'MessagePrintAgent'

        if broker is None or not isinstance(broker, BrokerWrapper):
            raise ValueError("Broker is required")

        self.broker = broker
        self.print_topics = print_topics
        for topic in print_topics:
            self.broker.subscribe(Subscription(subscriberName=f'self.name+{topic}', topic=topic, callback=self.on_message))

    def on_message(self, message):
        # the received message is bytes. decode:
        message = message.decode('utf-8')
        print(f'{self.name} received {message}')

    def on_stop(self, message):
        print(f'TimeprintAgent stops due to : {message.decode("utf-8")}')
        self.broker.unsubscribe('tick', self.on_message)
        self.broker.unsubscribe('pleaseStop', self.on_message)

    def run(self):
        pass
