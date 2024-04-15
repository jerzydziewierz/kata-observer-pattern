from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(
        [
            "lib/data_replay.py",
            "lib/datatypes.py",
            "lib/event_printer.py",
            "lib/logger_json.py",
            "lib/logger_yaml.py",
            "lib/observable.py",
            "lib/processorBasic.py",
            "lib/timer.py",
            "demo_01.py"
        ]
       )
)
