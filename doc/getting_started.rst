Getting started
===============

Get api key from here:
https://ilmatieteenlaitos.fi/rekisteroityminen-avoimen-datan-kayttajaksi

::

    import asyncio
    import fmi


    async def run():
        client = fmi.Client("fmi-api-key")
        weather = await client.weather_now("turku")

        print(f"it's {weather.t2m}°C warm and wind is blowing "
              f"{weather.ws_10min} m/s")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
