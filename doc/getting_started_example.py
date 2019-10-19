"""fmi.py minimal example (python 3.7+)"""

import asyncio
import fmi


async def main():
    observation = await fmi.weather_now("turku")

    print(f"it's {observation.temperature}°C warm and wind is blowing "
          f"{observation.wind_speed} m/s")


asyncio.run(main())
