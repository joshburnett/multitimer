from threading import Thread, Event
from time import clock


class RepeatingTimer(Thread):
    """Start this timer by calling RepeatingTimer.start()"""
    def __init__(self, interval, ontimeout, params=None, count=-1, runonstart=True):
        Thread.__init__(self)
        self.dt = interval
        self.ontimeout = ontimeout
        self.params = params
        self.count = count
        self.counter = 0
        self.stopevent = Event()
        self.starttime = None
        self.runonstart = runonstart
        self._isfirst = True

    def run(self):
        self.starttime = clock()

        while True:
            if not (self._isfirst and not self.runonstart):
                # print(f'first: {self._isfirst}, onstart: {self.runonstart}')
                if self.params is None:
                    self.ontimeout()
                else:
                    self.ontimeout(**self.params)
                self.counter += 1
                if (self.count > 0) and (self.counter >= self.count):
                    self.stopevent.set()

            if self._isfirst:
                self._isfirst = False

            if self.stopevent.wait(self.dt - (clock() - self.starttime) % self.dt):
                break

    def stop(self):
        self.stopevent.set()


class MultiTimer(object):
    """This timer can be re-started multiple times by calling MultiTimer.start()"""
    def __init__(self, interval, ontimeout, params=None, count=-1, runonstart=True):
        self._dt = interval
        self._ontimeout = ontimeout
        self._params = params
        self._count = count
        self._runonstart = runonstart

        self._timer = None

    def start(self):
        try:
            self._timer.stop()
        except AttributeError:
            pass

        self._timer = RepeatingTimer(interval=self._dt, ontimeout=self._ontimeout,
                                     params=self._params, count=self._count,
                                     runonstart=self._runonstart)
        self._timer.start()

    def stop(self):
        self._timer.stop()

    @property
    def dt(self):
        return self._dt

    @dt.setter
    def dt(self, value):
        self._dt = value
        try:
            self._timer.dt = value
        except AttributeError:
            pass

    @property
    def ontimeout(self):
        return self._ontimeout

    @ontimeout.setter
    def ontimeout(self, value):
        self._ontimeout = value
        try:
            self._timer.ontimeout = value
        except AttributeError:
            pass

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, value):
        self._params = value
        try:
            self._timer.params = value
        except AttributeError:
            pass

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value
        try:
            self._timer.count = value
        except AttributeError:
            pass

    @property
    def runonstart(self):
        return self._runonstart

    @runonstart.setter
    def runonstart(self, value):
        self._runonstart = value
        try:
            self._timer.runonstart = value
        except AttributeError:
            pass

    @property
    def counter(self):
        try:
            return self._timer.counter
        except AttributeError:
            return 0



if __name__ == "__main__":
    pass
