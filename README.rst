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


    # You can specify input parameters for the ontimeout function
    def job2(foo):
        print(foo)

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
~~~~~~~~~~~~~~~~

* Initial release



Meta
----

Josh Burnett - josh@burnettsonline.org

Distributed under the MIT license. See ``LICENSE.txt`` for more information.

https://github.com/joshburnett/multitimer
