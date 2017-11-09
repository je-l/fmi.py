"""FMI api fetching and WFS parsing.
"""

from urllib.parse import urlencode
import aiohttp
from fmi.wfs_parse import parse_latest_observations

from fmi import Observation

WFS_URL = "http://data.fmi.fi/fmi-apikey/{}/wfs?"


class Client:
    """Client for interacting with FMI api."""

    def __init__(self, api_key):
        """
        :param api_key: FMI api key
        """
        if not api_key:
            raise ValueError("fmi api key cannot be empty")

        self.base_url = WFS_URL.format(api_key)

    async def latest_observations(self, place):
        """Fetch most recent weather observations for a specific place.

        :param place: name for city or town
        :return: list of :class:`Observation` objects
        """
        params = {
            "request": "getFeature",
            "storedquery_id": "fmi::observations::weather::simple",
            "place": place
        }

        url = self.base_url + urlencode(params)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                unparsed_gml = await response.read()

        return parse_latest_observations(unparsed_gml)

    async def weather_now(self, place):
        """Fetch current weather for a specific place.

        :param place: term for the place, city, or town.
        :return: :class:`Observation` object
        """
        return (await self.latest_observations(place))[-1]




