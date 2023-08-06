Logging
-------

Exposures
~~~~~~~~~

`dntuils` provides a complementary logging and debugging instrument called "exposures". An exposure is a data
structure that allows a process to "expose" its state in parts to other processes under a given name. The data
exchange format is JSON. Only one process may have write permissions on an exposure at a time, while many may
read from the exposure. The basic functions to work with exposures are ``expose`` for writing into an exposure
and ``inspect`` to read from it. Exposures have hierarchically structured names similar to the file system
hierarchy in Unix-based operating systems. Names of exposures may be, for instance ``'/users/anna'`` or ``'/users/bob'``.
In order to expose a instance of a data structure, it must be JSON-ifiable in the sense of the
:func:`dnutils.tools.jsonify`, i.e. it must be either a type natively supported by JSON (int, float, string, list,
or dict) or it must have a ``json`` property, which is being called.

A process can expose a string message using the :func:`dnutils.logs.expose` method, which expects the data to be
exposed as well as the name under which it is supposed to be accessible by other processes:

.. code-block:: python
    :linenos:

    >>> from dnutils import expose, inspect
    >>> expose('/msgs/greeting', 'hello, world!')

The exposure can be read by another process using the :func:`dnutils.logs.inspect` method:

.. code-block:: python
    :lineno-start: 3

    >>> inspect('/msgs/greeting')
    'hello, world!'

More complex JSON data can be exposed in the same way:

.. code-block:: python
    :lineno-start: 5

    >>> expose('/mydict', {'first': 1, 'second': 2, 'third': 3})
    >>> inspect('/mydict')
    {'second': 2, 'first': 1, 'third': 3}

Exposures are a 1-to-many broadcast mechanism for inter-process communcations, ie. if a process tries to expose
data on an exposure that is already occupied by another process, ``expose()`` will raise a :class:`dnutils.logs.ExposureLockedError`
If ``inspect()`` is called on an exposure that no process is holding a write lock for, a :class:`dnutils.logs.EmptyExposureError`.