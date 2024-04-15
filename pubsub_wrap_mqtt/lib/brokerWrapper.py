# concept:
# abstraction of MQTT broker.
# this broker class simplifies subscription to topics by allowing the classes to simply call "broker.subscribe(topic, callback)"
# and the broker will call the callback when mqtt message of topic "topic" arrives.

import paho.mqtt.client as mqtt
import threading
import time
from queue import Queue
from abc import ABC, abstractmethod
from typing import Callable, ClassVar
from attr import dataclass, field


@dataclass
class Subscription:
    topic: str
    callback: Callable


class BrokerWrapper:
    def __init__(self, broker_ip="localhost", broker_port=1883):
        self.topics: dict[str, list[Subscription]] = {}
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.connect(broker_ip, broker_port)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        # execute the subscriptions.
        # ! todo.

    def start(self):
        self.client.loop_start()

    def subscribe(self, topic, callback):
        """
        First part of the key value offering of this class.
        The agent subscribes to a topic calling this method, but it's the brokerWrapper that will subscribe to this method;
        and then, when a message arrives, it calls the callback function.
        This way, the agents do not need to worry about the complexity of mqtt; also, the mqtt could be replaced by kafka.

        :param topic: string: The topic to subscribe to.
        :param callback: the function to be called with one parameter, the message.
        :return: None. This is a verb.
        """
        # first, register that this subscription is wanted.
        subscriptions = self.topics.get(topic, [])
        subscriptions.append(Subscription(callback))
        self.topics[topic] = subscriptions
        # and now, if connected, also subscribe to the MQTT
        self.client.subscribe(topic)
        return None

    def on_message(self, client, userdata, msg):
        """
        Second part of the key value offering of this class.
        Once a message is received from the MQTT broker, the targets of this message are resolved, and their callbacks called.
        :param client: mqtt library parameter
        :param userdata:
        :param msg:
        :return:
        """
        print("Received a message on topic " + msg.topic)
        ! TODO: implement tomorrow
