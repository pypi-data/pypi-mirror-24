========
Zomatopy
========
**A Python wrapper for the Zomato API v2.1**

Installation
************

.. code-block:: python

 pip install zomatopy

Getting Started
***************

This wrapper was written for Python 3 and might not work well with Python 2.


Adding zomatopy to your application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

 import zomatopy

 config={
    "user_key"="ZOMATO_API_KEY"
 }

 zomato = zomatopy.initialize_app(config)

For more information
^^^^^^^^^^^^^^^^^^^^

Please see the `official documentation <https://github.com/sharadbhat/Zomatopy>`_
.