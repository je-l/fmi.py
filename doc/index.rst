fmi.py documentation
==================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Getting started
---------------

::

    import fmi

    client = fmi.Client("api-key-here"):
    res = await client.latest_observations("helsinki")
    print(res)


Api reference
-----------------------------

.. autoclass:: fmi.Client
    :members:
