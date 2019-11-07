# multitimer

A pure-python auto-repeating timer that can be stopped and restarted multiple times.  

`multitimer.MultiTimer` is similar to
[`threading.Timer`](https://docs.python.org/3/library/threading.html#timer-objects),
but allows the timer to repeat multiple times.  Additionally, `MultiTimer` can be started and
stopped multiple times (unlike `threading.Timer`).

## Overview

`multitimer.MultiTimer(interval, function, args=None, kwargs=None, count=-1, runonstart=True)`

Creates a timer that will run _function_ with arguments _args_ and keyword
arguments _kwargs_, after _interval_ seconds have passed, a total of _count_ times.

If _runonstart_==True, then _function_ will be called immediately when `.start()` is called.

If _args_ is None (the default) then an empty list will be used. If _kwargs_ is None (the
default) then an empty dict will be used.

If _count_ == -1 (the default), the timer will repeat indefinitely, or until `.stop()`
is called.

Start this timer by calling `.start()`.  Once started, calling `.stop()` will terminate the
timer's loop and not produce any further calls to _function_. Note that if _function_ is
currently in the middle of running, it will finish the current iteration and not be interrupted.

_ontimeout_ and _params_ are deprecated in 0.2, and replaced by _function_, _args_
and _kwargs_, to match the `threading.Timer` API.
    
Since the underlying mechanism is purely based on python threads & events, the overall processor
load & memory usage are minimal.  Note that the timing accuracy is typically to within about 10 ms,
depending on the platform.


## Installation & usage

```bash
$ pip install multitimer
```

```python
import multitimer
import time

def job():
	print("I'm working...")

# This timer will run job() five times, one second apart
timer = multitimer.MultiTimer(interval=1, function=job, count=5)

# Pauses for one interval before starting job() five times
timer = multitimer.MultiTimer(interval=1, function=job, count=5, runonstart=False)


# You can specify input parameters for the _function_ function
def job2(foo):
	print(foo)

timer = multitimer.MultiTimer(interval=1, function=job2, kwargs={'foo':"I'm still working..."})

# Also, this timer would run indefinitely...
timer.start()

# ...unless it gets stopped
time.sleep(5)
timer.stop()

# and potentially waited for (in case an iteration was in progress)
timer.join()


# If a mutable object is used to specify input parameters, it can be changed after starting the timer
output = {'foo':"Doin' my job again."}
timer = multitimer.MultiTimer(interval=1, function=job2, kwargs=output, count=5)
timer.start()

time.sleep(3.5)
output['foo'] = "I'd like to be done now."

# And a MultiTimer can be re-started by just calling start() again
time.sleep(2)
output['foo'] = 'Please just let me be...'
timer.start()
time.sleep(4.5)
timer.stop()
```

Releases
--------

### 0.1, 2018-02-15

* Initial release

### 0.2, 2019-01-17

* Replace time.clock() calls with time.perf_counter(), as [time.clock is deprecated since python 3.3](https://docs.python.org/3/library/time.html#time.clock) and doesn't provide consistent behavior across different platforms.
* Replace _ontimeout_ with _function_, and _params_ with _args_ and _kwargs_, to match the `threading.Timer` API.
_ontimeout_ and _params_ are deprecated and will be removed in v0.3.
* Added lots of code comments to better explain how the module works. 

Meta
----

Josh Burnett - josh_github@burnettsonline.org

Distributed under the MIT license. See `LICENSE.txt` for more information.

<https://github.com/joshburnett/multitimer>

Hope you find this useful!