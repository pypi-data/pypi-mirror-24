brent-search
============

|PyPI-Status| |PyPI-Versions| |Conda-Forge-Status| |Conda-Downloads|

|Build-Status| |Codacy-Grade| |License|

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

.. code::

    (0.0, -0.8, 6)

Install
-------

The recommended way of installing it is via conda_

.. code:: bash

    conda install -c conda-forge brent-search

An alternative way would be via pip_

.. code:: bash

    pip install brent-search

Running the tests
-----------------

After installation, you can test it

.. code:: bash

    python -c "import brent_search; brent_search.test()"

as long as you have pytest_.

Authors
-------

* `Danilo Horta`_

License
-------

This project is licensed under the MIT License - see the
License-File_ file for details.

.. |Build-Status| image:: https://travis-ci.org/limix/brent-search.svg?branch=master
    :target: https://travis-ci.org/limix/brent-search

.. |Codacy-Grade| image:: https://api.codacy.com/project/badge/Grade/259a10b874124d91bccf61e516522607
    :target: https://www.codacy.com/app/danilo.horta/brent-search?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=limix/brent-search&amp;utm_campaign=Badge_Grade

.. |PyPI-Status| image:: https://img.shields.io/pypi/v/brent-search.svg
    :target: https://pypi.python.org/pypi/brent-search

.. |PyPI-Downloads| image:: https://img.shields.io/pypi/dm/brent-search.svg
    :target: https://pypi.python.org/pypi/brent-search

.. |PyPI-Versions| image:: https://img.shields.io/pypi/pyversions/brent-search.svg
    :target: https://pypi.python.org/pypi/brent-search

.. |Conda-Forge-Status| image:: https://anaconda.org/conda-forge/brent-search/badges/version.svg
    :target: https://anaconda.org/conda-forge/brent-search

.. |Conda-Downloads| image:: https://anaconda.org/conda-forge/brent-search/badges/downloads.svg
    :target: https://anaconda.org/conda-forge/brent-search

.. |License| image:: https://img.shields.io/pypi/l/brent-search.svg
    :target: https://raw.githubusercontent.com/brent-search/brent-search/master/LICENCE

.. |PyTest| image:: http://docs.pytest.org/en/latest/
    :target: http://docs.pytest.org/en/latest/

.. _License-File: https://raw.githubusercontent.com/limix/brent-search/master/LICENSE

.. _Danilo Horta: https://github.com/horta

.. _conda: http://conda.pydata.org/docs/index.html

.. _pip: https://pypi.python.org/pypi/pip

.. _pytest: http://docs.pytest.org/en/latest/
