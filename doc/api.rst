Api reference
=============

Main API
--------

.. autofunction:: fmi.latest_observations

.. autofunction:: fmi.forecast

.. autofunction:: fmi.weather_now

.. autofunction:: fmi.sea_levels

.. WARNING::
    Different weather stations have considerably different selection of data
    values. Don't assume that some specific property would never be None.

Observation
-----------

.. autoclass:: fmi.Observation()
    :members:

Forecast
-----------

.. autoclass:: fmi.Forecast()
    :members:


Coordinates
-----------

.. autoclass:: fmi.Coordinates()
    :members:
