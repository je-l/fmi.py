Getting started
===============

::

    import fmi

    client = fmi.Client("api-key-here")
    res = await client.latest_observations("helsinki")
    print(res)

