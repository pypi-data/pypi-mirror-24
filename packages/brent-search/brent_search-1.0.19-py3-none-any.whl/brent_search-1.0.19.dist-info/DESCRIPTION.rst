brent-search
============

|PyPI-License| |PyPI-Version| |PyPI-Versions| |Anaconda-Version|
|Anaconda-Downloads| |Documentation Status| |Codacy Badge|

Brent's method for univariate function optimization.

Example
-------

.. code:: python

    from brent_search import brent

    def func(x, s):
      return (x - s)**2 - 0.8

    r = brent(lambda x: func(x, 0), -10, 10)
    print(r)

The output should be

::

    (0.0, -0.8, 6)

Install
-------

The recommended way of installing it is via
`conda <http://conda.pydata.org/docs/index.html>`__

.. code:: bash

    conda install -c conda-forge brent-search

An alternative way would be via pip

.. code:: bash

    pip install brent-search

Running the tests
-----------------

After installation, you can test it

::

    python -c "import brent_search; brent_search.test()"

as long as you have `pytest <http://docs.pytest.org/en/latest/>`__.

Authors
-------

-  **Danilo Horta** - https://github.com/Horta

License
-------

This project is licensed under the MIT License - see the
`LICENSE <LICENSE>`__ file for details

.. |PyPI-License| image:: https://img.shields.io/pypi/l/brent-search.svg?style=flat-square
   :target: https://pypi.python.org/pypi/brent-search/
.. |PyPI-Version| image:: https://img.shields.io/pypi/v/brent-search.svg?style=flat-square
   :target: https://pypi.python.org/pypi/brent-search/
.. |PyPI-Versions| image:: https://img.shields.io/pypi/pyversions/brent-search.svg
   :target: https://pypi.python.org/pypi/brent-search/
.. |Anaconda-Version| image:: https://anaconda.org/conda-forge/brent-search/badges/version.svg
   :target: https://anaconda.org/conda-forge/brent-search
.. |Anaconda-Downloads| image:: https://anaconda.org/conda-forge/brent-search/badges/downloads.svg
   :target: https://anaconda.org/conda-forge/brent-search
.. |Documentation Status| image:: https://readthedocs.org/projects/brent-search/badge/?style=flat-square&version=latest
   :target: https://brent-search.readthedocs.io/
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/259a10b874124d91bccf61e516522607
   :target: https://www.codacy.com/app/danilo.horta/brent-search?utm_source=github.com&utm_medium=referral&utm_content=limix/brent-search&utm_campaign=Badge_Grade


