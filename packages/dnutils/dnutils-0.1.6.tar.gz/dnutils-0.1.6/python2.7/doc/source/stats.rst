Statistics Tools
----------------

Incremental Gaussian Distributions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Packages for numerical math such as ``numpy`` provide powerful support for sampling from and inducing of
probabilty distributions. Most of them only work in batches, i.e. a user needs to provide
all data at one time. In many scenarios, it is desirable to work with `incremental` updates on a distribution, however.
`dnutils` provides a simple implementation of a Normal (ie. Gaussian) distribution, which can be updated when
new data points arrive in constant time, without recalculating explicitly for every previous datapoint.

The implementation is contained in :class:`dnutils.stats.Gaussian`, and its use is pretty simple: To generate a
distribution, we can just instantiate it:

.. code-block:: python
    :linenos:

    >>> from dnutils.stats import Gaussian
    >>> import numpy
    >>> data = numpy.random.normal(.5, .1, 10000) # our test data
    >>> gauss = Gaussian()
    >>> for point in data:
    ...     gauss.update(point)

    >>> print(gauss)
    <Gaussian mean=0.50, var=0.01>

Batch processing is still supported:

.. code-block:: python
    :linenos:

    print(Gaussian(data=data))
    <Gaussian mean=0.50, var=0.01>

And multivariate Gaussians can be processed:

.. code-block:: python
    :linenos:

    >>> mean = [5., 4.]
    >>> cov = [[1., -0.3], [-0.3, 1.]]
    >>> data = np.random.multivariate_normal(mean, cov, size=50000)
    >>> gauss = Gaussian()
    >>> for d in data:
    ...     gauss.update(d)
    >>> print(gauss)
    <Gaussian
    mean=
    [ 4.99449741  4.00247152]
    cov=
    ---------  ---------
     1.00105   -0.298396
    -0.298396   0.993321
    ---------  --------->




