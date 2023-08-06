palpyutil
##############
.. |PyPI-Status| |PyPI-Versions| |Build-Status| |Codecov| |LICENCE|

Fast optimal matching of items for source-sharing derivative time series.

.. code-block:: python

  from palpyutil import dynamic_timestamp_match
  dynamic_timestamp_match(timestamp1, timestamps2, delta=20)

.. contents::

.. section-numbering::

Installation
============

Install ``palpyutil`` with:

.. code-block:: bash

  pip install palpyutil


Contributing
============

Package author and current maintainer is Shay Palachy (shay.palachy@gmail.com); You are more than welcome to approach him for help. Contributions are very welcomed.

Installing for development
--------------------------

Clone:

.. code-block:: bash

  git clone git@github.com:shaypal5/palpyutil.git


Install in development mode with test dependencies:

.. code-block:: bash

  cd palpyutil
  pip install -e ".[test]"


Running the tests
-----------------

To run the tests, use:

.. code-block:: bash

  python -m pytest --cov=palpyutil


Adding documentation
--------------------

This project is documented using the `numpy docstring conventions`_, which were chosen as they are perhaps the most widely-spread conventions that are both supported by common tools such as Sphinx and result in human-readable docstrings (in my personal opinion, of course). When documenting code you add to this project, please follow `these conventions`_.

.. _`numpy docstring conventions`: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt
.. _`these conventions`: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt


Credits
=======
Created by Shay Palachy  (shay.palachy@gmail.com).


.. |PyPI-Status| image:: https://img.shields.io/pypi/v/palpyutil.svg
  :target: https://pypi.python.org/pypi/palpyutil

.. |PyPI-Versions| image:: https://img.shields.io/pypi/pyversions/palpyutil.svg
   :target: https://pypi.python.org/pypi/palpyutil

.. |Build-Status| image:: https://travis-ci.org/shaypal5/palpyutil.svg?branch=master
  :target: https://travis-ci.org/shaypal5/palpyutil

.. |LICENCE| image:: https://img.shields.io/pypi/l/palpyutil.svg
  :target: https://pypi.python.org/pypi/palpyutil

.. |Codecov| image:: https://codecov.io/github/shaypal5/palpyutil/coverage.svg?branch=master
   :target: https://codecov.io/github/shaypal5/palpyutil?branch=master
