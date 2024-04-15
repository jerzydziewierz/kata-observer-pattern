import trio
import time


class Timer:
    def __init__(self, name='t1', interval=1.0, ):
        self._interval = interval
        self.name = name
        self._observers = []
        self.please_shutdown = False

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def shutdown(self):
        self.please_shutdown = True

    async def notify(self):
        for observer in self._observers:
            await observer.update(self)

    async def run(self):
        while not self.please_shutdown:
            start_time = time.monotonic()
            await self.notify()
            elapsed_time = time.monotonic() - start_time
            print(f'it took {elapsed_time} seconds to notify observers')
            await trio.sleep(max(0, self._interval - elapsed_time))


class Observer:
    def __init__(self, name):
        self.name = name

    async def update(self, timer):
        await trio.sleep(0.1)
        print(f"{self.name} observes a tick from Timer at {time.monotonic()}")

    async def observe(self, other):
        other.attach(self)


async def main():
    timer = Timer(1)  # Create a timer that ticks every 1 second
    observer1 = Observer(name='obs1')
    observer2 = Observer(name='obs2')

    timer.attach(observer1)
    timer.attach(observer2)

    async with trio.open_nursery() as nursery:
        nursery.start_soon(timer.run)

        # Let the timer run for 5 seconds
        await trio.sleep(3)

        # Detach observer2 after 5 seconds
        timer.detach(observer2)

        # Let the timer run for another 3 seconds
        await trio.sleep(3)
        timer.detach(observer1)
        await trio.sleep(3)
        timer.shutdown()


trio.run(main)
