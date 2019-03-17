"""Main library interface for the FMI api
"""
from typing import List, Tuple, Optional, Any

from urllib.parse import urlencode
from datetime import datetime, timedelta

from fmi import util
from fmi.model import Observation, Forecast
from fmi.wfs_parse import (
    parse_latest_observations,
    parse_forecast,
    parse_sea_levels,
)

from fmi.model import OBSERVATION_PARAMS

WFS_URL = "https://data.fmi.fi/wfs?"


class Client:
    """Client for interacting with FMI api."""

    def __init__(self, api_key: str) -> None:
        """
        :param api_key: FMI api key
        """
        if not api_key:
            raise ValueError("fmi api key cannot be empty")

        self.fetch = util.authed_fetch(api_key)

    async def latest_observations(
        self,
        place: str,
        starttime: Optional[str] = None,
        timestep: int = 10,
        aiohttp_kwargs: Any = None,
    ) -> List[Observation]:
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
            `aiohttp.ClientSession.request <https://aiohttp.readthedocs.io\
            /en/stable/client_reference.html#aiohttp.ClientSession.request>`_

        :raises ValueError: error raised if fmi api returns error, for example
            no results for given place parameter
        :returns: list of :class:`Observation` objects
        """
        sensor_parameters = ",".join(OBSERVATION_PARAMS.keys())

        params = {
            "request": "getFeature",
            "storedquery_id": "fmi::observations::weather::simple",
            "place": place,
            "parameters": sensor_parameters,
        }

        if timestep % 10 != 0:
            raise ValueError("timestep must be divisable by 10")

        if timestep != 10:
            params["timestep"] = str(timestep)

        if starttime:
            params["starttime"] = starttime

        url = WFS_URL + urlencode(params)
        unparsed_gml = await self.fetch(url, aiohttp_kwargs)

        return parse_latest_observations(unparsed_gml)

    async def forecast(
        self,
        place: str,
        timestep: int = 60,
        count: int = 5,
        aiohttp_kwargs: Any = None,
    ) -> List[Forecast]:
        """Fetch forecast for single place.

        :param place: search term for place. For example "Arabia, Helsinki"
        :param timestep: interval between forecast points in minutes
        :param count: # of forecast objects. Maximum is 5
        :returns: list of :class:`Forecast` objects
        """
        if count > 5:
            raise ValueError("forecast count must be <= 5")

        params = {
            "request": "getFeature",
            "storedquery_id": "fmi::forecast::hirlam::surface::point::simple",
            "place": place,
        }

        if timestep != 60:
            params["timestep"] = str(timestep)

        if count != 5:
            # API count parameter affects the returned properties, not returned
            # forecast amount, so we must multiply it with the # of properties
            params["count"] = str(count * 24)

        url = WFS_URL + urlencode(params)
        unparsed_gml = await self.fetch(url, aiohttp_kwargs)
        return parse_forecast(unparsed_gml)

    async def weather_now(
        self, place: str, aiohttp_kwargs: Any = None
    ) -> Observation:
        """Fetch current weather for a specific place.

        :param place: term for the place, city, or town.
        :param aiohttp_kwargs: see :func:`fmi.Client.latest_observations`
        :raises ValueError: error raised if fmi api returns error, for example
            no results for given place parameter
        :returns: :class:`Observation` object
        """
        half_hour_before = datetime.utcnow() - timedelta(minutes=30)
        iso_time = datetime.isoformat(half_hour_before.replace(microsecond=0))

        observations = await self.latest_observations(
            place,
            starttime=iso_time,
            timestep=10,
            aiohttp_kwargs=aiohttp_kwargs,
        )

        if not observations:
            raise ValueError('No results found for "{}"'.format(place))

        return observations[-1]

    async def sea_levels(
        self,
        fmisid: str,
        starttime: Optional[str] = None,
        endtime: Optional[str] = None,
        timestep: int = 60,
        aiohttp_kwargs: Any = None,
    ) -> List[Tuple[str, Optional[int]]]:
        """Fetch 12 hour sea level observations from a mareograph station.

        :param fmisid: FMISID of a mareograph station as listed `here
            <https://en.ilmatieteenlaitos.fi/observation-stations>`_
        :param timestep: time interval between results in minutes. Must be
            divisible by 30
        :param starttime: UTC ISO 8601 time string. Maximum precision is one
            second
        :param enddtime: UTC ISO 8601 time string
        :returns: list of unix timestamp - sea level -pairs. Units in
            millimeters
        """
        if timestep % 30 != 0:
            raise ValueError("timestep must be divisible by 30")

        raw_params = {
            "request": "getFeature",
            "storedquery_id": "fmi::observations::mareograph::simple",
            "fmisid": fmisid,
            "timestep": timestep,
            "starttime": starttime,
            "endtime": endtime,
        }

        # remove null params
        params = {k: v for k, v in raw_params.items() if v is not None}

        url = WFS_URL + urlencode(params)

        unparsed_gml = await self.fetch(url, aiohttp_kwargs)
        return parse_sea_levels(unparsed_gml)
