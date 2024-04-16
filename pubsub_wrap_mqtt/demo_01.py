from threading import Thread

from lib.brokerwrapper import BrokerWrapper
from lib.agents.msgprint import MessagePrint
from lib.agents.timetick import TimeTickAgent
import time


broker = BrokerWrapper()
ticker = TimeTickAgent(broker)
printer = MessagePrint(broker)


time.sleep(5)
broker.publish('pleaseStop', "end of simulation.")
