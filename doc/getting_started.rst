Getting started
===============

Get api key from here:
https://ilmatieteenlaitos.fi/rekisteroityminen-avoimen-datan-kayttajaksi

::

    import asyncio
    import fmi


    async def run():
        client = fmi.Client("fmi-api-key")
        observation = await client.weather_now("turku")

        print(f"it's {observation.temperature}°C warm and wind is blowing "
              f"{observation.wind_speed} m/s")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
