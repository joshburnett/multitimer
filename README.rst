multitimer
========================

A pure-python periodic timer that can be started multiple times

Usage
--------
.. code-block:: bash

    $ pip install multitimer

.. code-block:: python
    import multitimer
    import time

    def job():
        print("I'm working...")

    # This timer will run job() five times, one second apart
    timer = multitimer.MultiTimer(interval=1, ontimeout=job, count=5)

    # Pauses for one interval before starting job() five times
    timer = multitimer.MultiTimer(interval=1, ontimeout=job, count=5, runonstart=False)


    def job2(foo):
        print(foo)

    # You can specify input parameters for the ontimeout function
    timer = multitimer.MultiTimer(interval=1, ontimeout=job2, params={'foo':"I'm still working..."})

    # Also, this timer would run indefinitely...
    timer.start()

    time.sleep(5)

    # ...unless it gets stopped
    timer.stop()


    # If a mutable object is used to specify input parameters, it can be changed after starting the timer
    output = {'foo':"Doin' my job again."}
    timer = multitimer.MultiTimer(interval=1, ontimeout=job2, params=output, count=5)
    timer.start()

    time.sleep(3.5)
    output['foo'] = "I'd like to be done now."

    # And a MultiTimer can be re-started by just calling start() again
    time.sleep(2)
    output['foo'] = 'Please just let me be...'
    timer.start()
    time.sleep(4.5)
    timer.stop()

Releases
--------

0.1, 2018-02-15
* Initial release



License
-------

Copyright 2018 Josh Burnett

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.