Debugging
---------

The :mod:`dnutils.debug` module provides a couple of useful tools
for convenient and lightweight debugging.

Printing
~~~~~~~~

The first and simplest function is the :func:`out` function:

.. autofunction:: dnutils.debug.out

The :func:`out` function is a simple wrapper around Python's ordinary
:func:`print` function, but it prepends to any output the module's file
name and line number of the calling frame. Let us consider an exemplay
python module ``test.py``:

.. code-block:: python
   :linenos:

   from dnutils import out

   if __name__ == '__main__':
       out('hello, world!')

Running the module prints ::

   $ python test.py
   test.py: l.4: hello, world!

So, :func:`dnutils.debug.out` is basically a print function that allows
to trace back where the call to it was actually issued.

Ideally, one should set up a real logging infrastructure
properly instead of using ``print``. However, the :func:`out`
function provides a convenient way of doing it the "quick-and-dirty"
way, which lets one locate the print statements that one has introduced
in the code, which can be really cumbersome to detect.

The :func:`out` function has a parameter ``tb`` that extends the
parameter list inherited from :func:`print`. Normally, when just
printing single statements to the console, one can just disregard it.
However, it might happen that one wants to outsource a more complex
debug output into a separate function. For example, consider the
following function that prints all global variables in the current
frame:

.. code-block:: python
   :linenos:

   def print_globals():
       out('global variables'):
       for k, v in globals().iter():
           print(k, ': ', v)

If the :func:`print_globals` function is now used somewhere in the
code, the location printed would always be the :func:`out` call (in
this example, line 2). The desirable output, however, would be the
location of the :func:`print_globals` function. The :func:`out`
function provides an additional parameter ``tb``, which lets us control
the number of indirections that it traces back to find the actual
caller frame. As :func:`out` is used in one additional level of
indirections,

.. code-block:: python
   :linenos:

   def print_globals():
       out('global variables', tb=2):
       for k, v in globals().iter():
           print(k, ': ', v)

Always prints the desired location in the code, where
:func:`print_globals` is called.

The :func:`dnutils.debug.stop` function is a modification of
:func:`dnutils.debug.out`, which stops after having printed the
desired output and waits until the user presses the return key:

.. autofunction:: dnutils.debug.stop

.. code-block:: python

   >>> from dnutils import stop
   >>> stop('waiting...')
   <stdin>: l.1: waiting...
   <press enter to continue> # hit enter here
   >>>



Stack Traces
~~~~~~~~~~~~

.. autofunction:: dnutils.debug.trace

.. toctree::
   :maxdepth: 2
   :caption: Contents:
