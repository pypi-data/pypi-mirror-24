palpyutil
#########

Shay Palachy's personal common Python 3 utility functions and classes.

.. code-block:: python

  from palpyutil.decorators import lazy_property

  @lazy_property
  def some_big_calc(param_array):
    sub_res = [big_func(param) for param in param_array]
    return sum(sub_res)


Installation
============

Install ``palpyutil`` with:

.. code-block:: bash

  pip install palpyutil


Credits
=======
Created by Shay Palachy  (shay.palachy@gmail.com).
