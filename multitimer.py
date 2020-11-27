from threading import Thread, Event
from time import perf_counter


class RepeatingTimer(Thread):
    """Similar to threading.Timer, but allows the timer to repeat multiple times.  However,
    since we are still subclassing threading.Thread, the .start() method can only be called
    once.  If you need to stop and restart a repeating timer, use MultiTimer instead.

    This class creates a timer that will run _function_ with arguments _args_ and keyword
    arguments _kwargs_, after _interval_ seconds have passed, a total of _count_ times.

    If _runonstart_==True, then _function_ will be called immediately when .start() is called.

    If args is None (the default) then an empty list will be used. If kwargs is None (the
    default) then an empty dict will be used.

    If _count_ == -1 (the default), the timer will repeat indefinitely, or until .stop()
    is called.

    Start this timer by calling RepeatingTimer.start().  After starting the timer, calling
    .stop() will terminate the timer's loop and prevent any further calls to function().
    Note that is function() it is currently in the middle of running, it will finish the
    current iteration and not be interrupted.

    _ontimeout_ and _params_ were deprecated in 0.2 and replaced by _function_, _args_
    and _kwargs_ to match the threading.Timer API.  _ontimeout_ and _params_ have been removed
    in 0.3.
    """

    def __init__(self, interval, function=None, args=None, kwargs=None, count=-1, runonstart=True):
        Thread.__init__(self)
        if count == 0:
            raise ValueError('count must be -1 or greater than 1, not zero.')
        if function is None:
            raise ValueError('function must be specified')

        self.interval = interval
        self.function = function

        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}

        self.count = count
        self.counter = 0
        self.stopevent = Event()
        self.starttime = None
        self.runonstart = runonstart
        self._isfirst = True

    def run(self):
        """This method gets called by .start(), don't call this method yourself."""
        self.starttime = perf_counter()

        while True:
            # Skip this if it's the first time through and self.runonstart == False
            if not (self._isfirst and not self.runonstart):
                # print(f'first: {self._isfirst}, onstart: {self.runonstart}')
                self.function(*self.args, **self.kwargs)
                self.counter += 1
                # If count == -1, we will run indefinitely
                if (self.count >= 1) and (self.counter >= self.count):
                    self.stopevent.set()

            # set self._isfirst to False once we've completed the first iteration
            if self._isfirst:
                self._isfirst = False

            # Event.wait() returns False when the event times out, so the only way this
            # statement evalutes to True is if stopevent gets set (stopevent.set() is called).
            # We use the call to perf_counter() to adjust the timeout value to account for the
            # time taken to run self.function() each iteration.
            # Because we are taking (time since start) % interval, we will skip time intervals that
            # we've missed, and run on the next interval.
            if self.stopevent.wait(self.interval - (perf_counter() - self.starttime) % self.interval):
                break

    def stop(self):
        """Stop the timer if it hasn't finished yet."""
        self.stopevent.set()


class MultiTimer(object):
    """Similar to threading.Timer, but allows the timer to repeat multiple times.  Additionally,
    MultiTimer can be started and stopped multiple times (unlike threading.Timer and
    multimer.RepeatingTimer).

    This class creates a timer that will run _function_ with arguments _args_ and keyword
    arguments _kwargs_, after _interval_ seconds have passed, a total of _count_ times.

    If _runonstart_==True, then _function_ will be called immediately when .start() is called.

    If args is None (the default) then an empty list will be used. If kwargs is None (the
    default) then an empty dict will be used.

    If _count_ == -1 (the default), the timer will repeat indefinitely, or until .stop()
    is called.

    Start this timer by calling .start().  Once started, calling .stop() will terminate the
    timer's loop and not produce any further calls to function(). Note that if function() is
    currently in the middle of running, it will finish the current iteration and not be interrupted.
    By calling .join(), one can wait for the timer to finish its task (if any) before proceeding further.

    _ontimeout_ and _params_ were deprecated in 0.2 and replaced by _function_, _args_
    and _kwargs_ to match the threading.Timer API.  _ontimeout_ and _params_ have been removed
    in 0.3.
    """

    def __init__(self, interval, function=None, args=None, kwargs=None, count=-1, runonstart=True):
        # First, check for appropriate parameters, issue relevant deprecation warnings.
        if count == 0:
            raise ValueError('count must be -1 or greater than 1, not zero.')
        if function is None:
            raise ValueError('function must be specified')

        # Store parameters internally
        self._interval = interval
        self._function = function
        self._args = args
        self._kwargs = kwargs
        self._count = count
        self._runonstart = runonstart

        # Create the empty _timer reference, which then gets initialized when the .start() method is called.
        self._timer = None

    def start(self):
        try:
            # If .start() is called without previously stopping the MultiTimer, we need to stop it first.
            self._timer.stop()
        except AttributeError:
            # This error will get raised the first time through, as we haven't created the first
            # RepeatingTimer yet.
            pass

        self._timer = RepeatingTimer(interval=self._interval, function=self._function,
                                     args=self._args, kwargs=self._kwargs, count=self._count,
                                     runonstart=self._runonstart)
        self._timer.start()

    def stop(self):
        try:
            self._timer.stop()
        except AttributeError:
            # If .stop() is called without previously starting the MultiTimer, the RepeatingTimer won't have been
            # created yet.
            pass

    def join(self):
        """Wait for the current task to finish, if any."""
        assert not self._timer or self._timer.stopevent.is_set(), "timer must be stopped before being joined"
        if self._timer:
            self._timer.join()
        
    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value):
        self._interval = value
        try:
            self._timer.interval = value
        except AttributeError:
            pass

    @property
    def function(self):
        return self._function

    @function.setter
    def function(self, value):
        self._function = value
        try:
            self._timer.function = value
        except AttributeError:
            pass

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        self._args = value
        try:
            self._timer.args = value
        except AttributeError:
            pass

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, value):
        self._kwargs = value
        try:
            self._timer.kwargs = value
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

    @property
    def starttime(self):
        return self._timer.starttime


if __name__ == "__main__":
    pass
