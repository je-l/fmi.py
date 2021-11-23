"""Main library interface for the FMI api
"""
from typing import List, Tuple, Optional, Any, Dict
from datetime import datetime, timedelta

from urllib.parse import urlencode
import aiohttp

from fmi.model import Observation, Forecast
from fmi.wfs_parse import (
    parse_latest_observations,
    parse_forecast,
    parse_sea_levels,
)

from fmi.model import OBSERVATION_PARAMS

WFS_URL = "https://opendata.fmi.fi/wfs/eng?"


async def fetch(url: str, aiohttp_kwargs: Dict[str, Any]) -> bytes:
    aiohttp_kwargs = aiohttp_kwargs or {}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, **aiohttp_kwargs) as response:
            res: bytes = await response.read()
            return res


async def latest_observations(
    place: Optional[str] = None,
    fmisid: Optional[int] = None,
    starttime: Optional[str] = None,
    endtime: Optional[str] = None,
    timestep: int = 10,
    aiohttp_kwargs: Any = None,
) -> List[Observation]:
    """Fetch most recent weather observations for a specific place. Default
    is last 12 hours in 10 minute intervals.

    :param place: name for city or town
    :param fmisid: id of a location
    :param starttime: fetch observations after this time. Use ISO 8601
        format with second precision
    :param endtime: fetch observations bevore this time. Use ISO 8601
        format with second precision
    :param timestep: interval between observations in minutes. Must be
        divisible by 10
    :param aiohttp_kwargs: keyword arguments for aiohttp request. This is
        useful for providing timeout, proxy etc. "low level" configuration for
        the underlying http requests. For possible values see
        `aiohttp.ClientSession.request
        <https://docs.aiohttp.org/en/stable/client_reference.html>`_

    :raises ValueError: error raised if fmi api returns error, for example
        no results for given place parameter
    :returns: list of :class:`Observation` objects
    """
    sensor_parameters = ",".join(OBSERVATION_PARAMS.keys())

    params = {
        "request": "getFeature",
        "storedquery_id": "fmi::observations::weather::simple",
        "parameters": sensor_parameters,
    }

    if timestep % 10 != 0:
        raise ValueError("timestep must be divisable by 10")

    if timestep:
        params["timestep"] = str(timestep)

    if starttime:
        params["starttime"] = starttime

    if endtime:
        params["endtime"] = endtime

    if place:
        params["place"] = place

    if fmisid:
        params["fmisid"] = str(fmisid)

    url = WFS_URL + urlencode(params)
    unparsed_gml = await fetch(url, aiohttp_kwargs)

    return parse_latest_observations(unparsed_gml)


async def forecast(
    place: str, timestep: int = 60, count: int = 5, aiohttp_kwargs: Any = None
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
    unparsed_gml = await fetch(url, aiohttp_kwargs)
    return parse_forecast(unparsed_gml)


async def weather_now(place: str, aiohttp_kwargs: Any = None) -> Observation:
    """Fetch current weather for a specific place.

    :param place: term for the place, city, or town.
    :param aiohttp_kwargs: see :func:`fmi.Client.latest_observations`
    :raises ValueError: error raised if fmi api returns error, for example
        no results for given place parameter
    :returns: :class:`Observation` object
    """
    half_hour_before = datetime.utcnow() - timedelta(minutes=30)
    iso_time = datetime.isoformat(half_hour_before.replace(microsecond=0))

    observations = await latest_observations(
        place, starttime=iso_time, timestep=10, aiohttp_kwargs=aiohttp_kwargs
    )

    if not observations:
        raise ValueError(f'No results found for "{place}"')

    return observations[-1]


async def sea_levels(
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

    unparsed_gml = await fetch(url, aiohttp_kwargs)
    return parse_sea_levels(unparsed_gml)
