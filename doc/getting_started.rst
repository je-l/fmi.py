Getting started
===============

Get api key from here:
https://ilmatieteenlaitos.fi/rekisteroityminen-avoimen-datan-kayttajaksi

::

    import fmi

    client = fmi.Client("api-key-here")
    res = await client.latest_observations("helsinki")
    print(res)

    turku_weather = await client.weather_now("turku")
    print(f"temperature at Turku: {turku_weather.t2m} c")

