# Usage example:

# import the modules
from lib import DataReplay, TimedEventSource, ExampleProcessor
from lib import EventPrinter, LoggerJsonl, LoggerYaml

from lib.datatypes import SomeData

# create the instances of the modules
logger_json = LoggerJsonl(filename='eventLog.jsonl')
logger_yaml = LoggerYaml(filename='eventLog.yaml')
event_printer = EventPrinter()

src_timer = TimedEventSource(interval=1, verbose=False)

src_data = DataReplay(data_source=[
    SomeData(value=1, source='replay'),
    SomeData(value=2, source='replay'),
    SomeData(value=3, source='replay'),
    SomeData(value=4, source='replay'),
    SomeData(value=5, source='replay'),
    SomeData(value=7, source='replay-last'),
    ],
    verbose=False)


data_processor1 = ExampleProcessor(name='step1')
data_processor2 = ExampleProcessor(name='step2')
data_processor3 = ExampleProcessor(name='step3')
#
# # list the modules so that they can be gathered and reasoned about together.

modules = [src_timer, src_data, event_printer, logger_json, logger_yaml, data_processor1, data_processor2, data_processor3]

src_data.observe(src_timer)
data_processor1.observe(src_data)
data_processor2.observe(data_processor1)
data_processor3.observe(data_processor2)

event_printer.observe(data_processor2)
logger_json.observe(data_processor3)
logger_yaml.observe(data_processor3)

# event_printer.observe(src_timer)
# event_printer.observe(src_data)
# event_printer.observe(data_processor1)
# event_printer.observe(data_processor2)
# event_printer.observe(data_processor3)
# event_printer.observe(logger_json)

# start the system
for module in modules:
    module.start()

# let the system run for a while
import time

time.sleep(2)

# stop the threads
for module in modules:
    module.stop()

