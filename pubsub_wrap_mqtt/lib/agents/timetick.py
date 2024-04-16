from ..brokerwrapper import Subscription, BrokerWrapper
from threading import Thread
import time


class TimeTickAgent:
    def __init__(self, broker: BrokerWrapper = None):
        if broker is None or not isinstance(broker, BrokerWrapper):
            raise ValueError("Broker is required")

        self._pleaseStop = False
        self.name = 'TimeTickAgent'
        self.outputTopic = 'TimeTickAgent/tick'

        self.time = 0
        self.broker = broker
        self.thread = Thread(target=self.run)
        self.thread.start()
        # subscribe to "stop" topic
        self.broker.subscribe(Subscription(subscriberName=self.name, topic='pleaseStop', callback=self.on_stop))

    def run(self):
        while not self._pleaseStop:
            self.broker.publish(self.outputTopic, self.time)
            time.sleep(1.0)
            self.time += 1

    def on_stop(self, message):
        print(f'TimeTickAgent stops due to : {message.decode("utf-8")}')
        self._pleaseStop = True
        self.thread.join()
