# concept:
# abstraction of MQTT broker.
# this broker class simplifies subscription to topics by allowing the classes to simply call "broker.subscribe(topic, callback)"
# and the broker will call the callback when mqtt message of topic "topic" arrives.

import paho.mqtt.client as mqttClient
import paho.mqtt.enums
import threading
import time
from queue import Queue
from abc import ABC, abstractmethod
from typing import Callable, ClassVar
from attr import dataclass, field


@dataclass
class Subscription:
    topic: str = field(default="unset")
    subscriberName: str = field(default="unset")
    callback: Callable = field(default=None)


class BrokerWrapper:
    def __init__(self, broker_ip="localhost", broker_port=1883):
        self.name = 'BrokerWrapper'
        self.topics: dict[str, list[Subscription]] = {}

        self.client = mqttClient.Client(callback_api_version=paho.mqtt.enums.CallbackAPIVersion.VERSION2)
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.connect(broker_ip, broker_port)
        self.thread = threading.Thread(target=self.forever)
        self.thread.start()

    def on_connect(self, client, userdata, flags, reason_code, properties):
        print("Connected with result code " + str(reason_code))
        # execute the subscriptions.
        # when the brokerWrapper first starts, there is no subscriptions. These come later.

    def forever(self):
        self.client.loop_start()

    def subscribe(self, subscription=None):
        """
        First part of the key value offering of this class.
        The agent subscribes to a topic calling this method, but it's the brokerWrapper that will subscribe to this method;
        and then, when a message arrives, it calls the callback function.
        This way, the agents do not need to worry about the complexity of mqtt; also, the mqtt could be replaced by kafka.

        :param subscription: brokerwrapper.Subscription: the subscription object containing at least, the topic and the callback.
        :return: None. This is a verb.
        """
        # first, register that this subscription is wanted.
        if subscription is None or not isinstance(subscription, Subscription):
            raise ValueError("Subscription must be a Subscription object")
        subscriptions = self.topics.get(subscription.topic, [])
        subscriptions.append(subscription)
        self.topics[subscription.topic] = subscriptions
        # and now, if connected, also subscribe to the MQTT
        self.client.subscribe(subscription.topic)
        return None

    def on_message(self, client, userdata, message):
        """
        Second part of the key value offering of this class.
        Once a message is received from the MQTT broker, the targets of this message are resolved, and their callbacks called.
        :param message: what was received.
        :param client: mqtt library parameter
        :param userdata:
        :return: None. this is a callback from the mqtt library.
        """
        print(f"Received a message on topic {message.topic}")

        subscriptions = self.topics.get(message.topic, [])

        if subscriptions:
            for subscription in subscriptions:
                subscription.callback(message.payload)
        else:
            print(f"Warning: No subscriptions found for topic {message.topic}")
        return None

    def publish(self, topic, message):
        """
        simply forward the message to the mqtt broker.
        :param topic: topic to publish on
        :param message: the message to publish
        :return: None
        """
        self.client.publish(topic, message)
        return None




