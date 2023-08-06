General Purpose Tools
---------------------

The :func:`dnutils.tools.ifnone` function is supposed to make the
ternary Python ``if-then-else`` idiom less verbose. The basic idea
of this function is that in many cases one is supposed to do only
few operations on a variable ``x``, but only if ``x`` is not ``None``.
A popular case is, for example, to obtain a string representation of ``x``,
but some special treatment of the ``None`` case: ::

    >>> str(x) if x is not None else 'N/A'

So far, so good. As long as ``x`` is a pretty short expression, there is
nothing to argue against the above construct. But what if ``x`` is, for
instance, a concatenation of functions or dictionary queries, like ::

    >>> str(myobj.textfield.gettext().getdata()) if myobj.textfield.gettext().getdata() is not None else ''

There are at least three shortcomings with such a construct:

  * Verbosity: myobj.textfield.gettext().getdata() needs to be written twice
  * Speed: myobj.textfield.gettext().getdata() needs to be evaluated twice
  * Readability: the expression is hard to read

To make such constructs more convenient, `dnutils` provide the
:func:`dnutils.tools.ifnone` function:

.. autofunction:: dnutils.tools.ifnone

Using :func:`dnutils.tools.ifnone`, the above expression can be written
more concisely as ::

    >>> ifnone(myobj.textfield.gettext().getdata(), '', str)

Another frequent example is parsing a number with a default value in
case of ``None``: ::

    ifnone(str_to_parse, 0, int)

.. note::
    Note that, in contrast to the ternary ``if-then-else`` construct,
    :func:`dnutils.tools.ifnone` always evaluates the ``else`` part, i.e.
    it does not support lazy evaluation.

:func:`dnutils.tools.ifnot` is equivalent to :func:`ifnone` except
for it checks for Boolean truth instead of ``None``:

.. autofunction:: dnutils.tools.ifnot

.. autofunction:: dnutils.tools.allnone

.. autofunction:: dnutils.tools.allnot

List Convenience Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~



Enhanced Dictionary Functionality
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Multiple Signal Handlers
~~~~~~~~~~~~~~~~~~~~~~~~

The original :mod:`signal` module only allows to register one handler 
at a time. :mod:`dnutils.signals` can be used to register an arbitrary 
number of different handlers, which will all be executed in the order 
they have been registered. More information can be found on
:doc:`signals`.


.. .. toctree::
   :hidden:
   debug
   console
   threads
   logging
