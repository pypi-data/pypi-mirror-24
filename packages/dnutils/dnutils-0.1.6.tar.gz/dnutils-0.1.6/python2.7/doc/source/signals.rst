Signal Handling
---------------

``dnutils`` comes with a little wrapper around the Python :mod:`signal`
module, allowing to register `multiple` signal handlers that are being
executed in the order in which they have been registered. The usage
is very simple:

To add a function to the signal handlers that is to be executed when
a particular signal is sent to the main thread, just call :func:`dnutils.signals.add_handler`:

.. code-block:: python
   :linenos:
   
   from dnutils import signals
   
   def goodbye(*_):
       print('bye')
    
   signals.add_handler(signals.SIGINT, goodbye) 
    
will call ``goodbye`` when the main thread receives a ``SIGINT``. As 
opposed to the regular ``signal`` module, with ``dnutils`` one can 
register as many handler functions as needed.

A handler function can be removed with a call to :func:`dnutils.signals.rm_handler`:

.. autofunction:: dnutils.signals.rm_handler

As ``dnutils`` uses the ``signal`` module by default, there is no
``KeyboradInterrupt`` being raised by default in case ``Ctrl-C`` is
pressed. To activate this default behavior, one can call 
:func:`dnutils.signals.enable_ctrlc`.
