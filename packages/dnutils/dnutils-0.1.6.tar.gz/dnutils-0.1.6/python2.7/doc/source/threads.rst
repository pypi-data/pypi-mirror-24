Multithreading
--------------

`dnutils` comes with its own reimplementation of the ``threading`` module with the :class:`Thread` class and its
thread synchronization data structures. The biggest difference to the original version is that the ``acquire()`` method
of the lock and thus all thread sync objects that are based on it are interruptable in `dnutils`.


Problem Description
~~~~~~~~~~~~~~~~~~~

The are a few peculiarities with Python and working in multiple threads. The official `Python documentation
<https://docs.python.org/2/library/thread.html>`_ charts a couple of caveats (among others):

    * Threads interact strangely with interrupts: the ``KeyboardInterrupt`` exception will be received by an arbitrary
      thread. (When the ``signal`` module is available, interrupts always go to the main thread.)

    * It is not possible to interrupt the ``acquire()`` method on a lock — the ``KeyboardInterrupt`` exception will
      happen after the lock has been acquired.

These two items cause indeed a `very` strange behavior. Consider, for example, a producer/consumer architecture
as it is described in the documentation of the ``threading`` module:

.. code-block:: python
    :linenos:

    cv = Condition()

    # Consume one item
    with cv:
        while not an_item_is_available():
            cv.wait()
        get_an_available_item()

    # Produce one item
    with cv:
        make_an_item_available()
        cv.notify()

In this snippet, the waiting thread will literally wait until it is notified and not even a ``KeyboardInterrupt`` is
capable of releasing the interal lock of the condition object. This impedes graceful termination of heavily
multithreaded processes like server applications.

The ``threads`` Module
~~~~~~~~~~~~~~~~~~~~~~

Interruptable Locks
^^^^^^^^^^^^^^^^^^^

The threads module is an almost exact replica of the normal Python :mod:`threading` module, but comes with
a reimplementation of locks, which are interruptable when ``acquire()`` blocks. ``acquire()``
raises a :class:`dnutils.threads.ThreadInterrupt` exception when ``interrupt()`` is called on a blocking lock.

.. autoclass:: dnutils.threads.Lock
    :members: acquire, interrupt

When :mod:`dnutils.threads` is used instead of :mod:`threading`, all waiting locks interrupted automatically
on an interrupt signal (``SIGINT``). Consequently, the following code can be ``Ctrl-C``'ed,

.. code-block:: python
    :linenos:

    l = dnutils.Lock()
    l.acquire()
    l.acquire()

whereas

.. code-block:: python
    :linenos:

    l = threading.Lock()
    l.acquire()
    l.acquire()

would block forever. Catching the :class:`dnutils.threads.ThreadInterrupt`, a blocking thread can gracefully terminate.

.. warning::
    As threads in the `dnutils` package make use of the :mod:`signal` module, one should not override the signal
    handler using ``signal.signal()`` as the interuption mechanism would break. Rather, it is advisable to use
    the :mod:`dnutils.signals` module to `add` custom signal handlers. Find more information on :doc:`signals`.

Interruptable Sleep
^^^^^^^^^^^^^^^^^^^

As also the regular ``time.sleep()`` function is not responsive, a customized sleep is included in `dnutils`,
which also throws a :class:`dnutils.threads.ThreadInterrupt` on a ``SIGINT``:

.. code-block:: python
    :linenos:

    try:
        dnutils.sleep(10)
    except ThreadInterrupt:
        pass

