from threading import Thread

from lib.broker import Agent, Broker
import time


class TimeTickAgent(Agent):
    def __init__(self, _broker=None):
        self._pleaseStop = False
        self.name = 'TimeTickAgent'
        self.time = 0
        self.broker = _broker
        self.thread = Thread(target=self.run)
        self.thread.start()
        # subscribe to "stop" topic
        self.broker.subscribe('pleaseStop', self.on_stop)

    def run(self):
        while not self._pleaseStop:
            broker.publish('tick', self.time)
            time.sleep(1.0)
            self.time += 1

    def on_stop(self, message):
        print(f'TimeTickAgent stops due to : {message}')
        self._pleaseStop = True
        self.thread.join()


class TimeprintAgent(Agent):
    def __init__(self, _broker=None):
        self.name = 'TimeprintAgent'
        self._broker = _broker
        self._broker.subscribe('tick',  self.on_message)
        self._broker.subscribe('pleaseStop', self.on_stop)

    def on_message(self,  message):
        print(f'{self.name} received {message}')

    def on_stop(self, message):
        print(f'TimeprintAgent stops due to : {message}')
        self._broker.unsubscribe('tick', self.on_message)
        self._broker.unsubscribe('pleaseStop', self.on_message)

    def run(self):
        pass


broker = Broker()
ticker = TimeTickAgent(broker)
printer = TimeprintAgent(broker)

time.sleep(3)
broker.publish('pleaseStop', "end of simulation.")
