"""Main library interface for the FMI api
"""

from urllib.parse import urlencode
from datetime import datetime, timedelta
from fmi import util
from fmi.wfs_parse import parse_latest_observations, parse_forecast
from fmi.model import OBSERVATION_PARAMS

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

    async def latest_observations(self, place, starttime=None, timestep=10,
                                  **aiohttp_kwargs):
        """Fetch most recent weather observations for a specific place. Default
        is last 12 hours in 10 minute intervals.

        :param place: name for city or town
        :param starttime: fetch observations after this time. Use ISO 8601
            format with second precision
        :param timestep: interval between observations in minutes. Must be
            divisible by 10
        :param aiohttp_kwargs: keyword arguments for aiohttp request.
            This is useful for providing timeout, proxy etc. "low level"
            configuration for the underlying http requests. For possible values
            see
            `aiohttp.ClientSession.request <http://aiohttp.readthedocs.io\
            /en/stable/client_reference.html#aiohttp.ClientSession.request>`_

        :raises ValueError: error raised if fmi api returns error, for example
            no results for given place parameter
        :return: list of :class:`Observation` objects
        """
        sensor_parameters = ",".join(OBSERVATION_PARAMS.keys())

        params = {
            "request": "getFeature",
            "storedquery_id": "fmi::observations::weather::simple",
            "place": place,
            "parameters": sensor_parameters
        }

        if timestep % 10 != 0:
            raise ValueError("timestep must be divisable by 10")

        if timestep != 10:
            params["timestep"] = timestep

        if starttime:
            params["starttime"] = starttime

        url = self.base_url + urlencode(params)
        unparsed_gml = await util.fetch(url, **aiohttp_kwargs)

        return parse_latest_observations(unparsed_gml)

    async def forecast(self, place, timestep=60, count=5, **aiohttp_kwargs):
        """Fetch forecast for single place.

        :param place: search term for place. For example "Arabia, Helsinki"
        :param timestep: interval between forecast points in minutes
        :param count: # of forecast objects. Maximum is 5"""

        if count > 5:
            raise ValueError("forecast count must be <= 5")

        params = {
            "request": "getFeature",
            "storedquery_id": "fmi::forecast::hirlam::surface::point::simple",
            "place": place
        }

        if timestep != 60:
            params["timestep"] = timestep

        if count != 5:
            # API count parameter affects the returned properties, not returned
            # forecast amount, so we must multiply it with the # of properties
            params["count"] = count * 24

        url = self.base_url + urlencode(params)
        unparsed_gml = await util.fetch(url, **aiohttp_kwargs)
        return parse_forecast(unparsed_gml)

    async def weather_now(self, place, **aiohttp_kwargs):
        """Fetch current weather for a specific place.

        :param place: term for the place, city, or town.
        :param aiohttp_kwargs: see :func:`fmi.Client.latest_observations`
        :raises ValueError: error raised if fmi api returns error, for example
            no results for given place parameter
        :return: :class:`Observation` object
        """
        half_hour_before = datetime.utcnow() - timedelta(minutes=30)
        iso_time = datetime.isoformat(half_hour_before.replace(microsecond=0))

        observations = await self.latest_observations(place, starttime=iso_time,
                                                      **aiohttp_kwargs)
        return observations[-1]
