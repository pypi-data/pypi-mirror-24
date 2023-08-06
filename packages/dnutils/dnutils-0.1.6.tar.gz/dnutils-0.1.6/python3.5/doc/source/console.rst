Console
-------

Progress Bars
~~~~~~~~~~~~~

The :class:`dnutils.console.ProgressBar` class implements a pseudo-animated
controllable progress bar in the console like the following:

.. image:: _static/progress-bars.png


.. autoclass:: dnutils.console.ProgressBar
    :members: __init__, setlayout, update, inc, finish

Status Messages
~~~~~~~~~~~~~~~

`dnutils` contains a class that mimics the behavior of
status messages of a typical Linux boot screen:

.. image:: _static/status-msg.png


.. autoclass:: dnutils.console.StatusMsg
    :members: __init__, setwidth, write, finish

A :class:`dnutils.console.StatusMsg` object can be instantiated
with an optional width, a message and a status. The width is a
string or a number determining the width (in absolute characters)
or the percentage of console that the status message will consume.
A behavior as shown in the above screenshot, for instance, can be
achieved by somehting like::

    for i in range(100):
        status = StatusMsg(message='  * Operation #%d:' % (i + 1))
        status.status = StatusMsg.OK if random.random() > .3 else StatusMsg.ERROR
        status.finish()

which will print 100 status bars and assign each the status ``OK``
with 70% probability and an ``ERROR`` state with 30%. The
following predefined stati are available:

* :attr:`dnutils.console.StatusMsg.OK` - a green "OK" label
* :attr:`dnutils.console.StatusMsg.ERROR` - a red "ERROR" label
* :attr:`dnutils.console.StatusMsg.PASSED` - a green "PASSED" label
* :attr:`dnutils.console.StatusMsg.FAILED` - a red "FAILED" label
* :attr:`dnutils.console.StatusMsg.WARNING` - a yellow "WARNING" label

For a particular ``StatusMsg`` instance, the set of available
stati can be customized by handing them over in the ``stati``
parameter of the constructor. A status is just a (possibly ASCII
escaped color) string. So customized status labels can be
easily created.
