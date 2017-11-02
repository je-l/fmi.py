"""FMI api fetching and WFS parsing.
"""

from urllib.parse import urlencode

from functools import reduce
import itertools

from dateutil.parser import parse as timeparse
from lxml import etree
import aiohttp

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
        :return: list of observations
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

        parsed_gml = etree.fromstring(unparsed_gml)

        return _parse_latest_observations(parsed_gml)


def _compare_element_id(element):
    id_text = element.values()[0]
    element_id = id_text.split(".", 1)[1]
    return element_id.split(".", 2)[:2]


def _merge(acc, cur):
    parsed = _parse_feature(cur)
    acc["timestamp"] = parsed["timestamp"]
    acc["coordinates"] = parsed["coordinates"]
    key = parsed["property"]
    val = parsed["value"]

    acc[key] = val

    return acc


def _parse_latest_observations(gml):
    """Parse latest observations object into python dict.
    :param gml: lxml Element
    :return: list of latest observations
    """

    elements = gml.findall(".//BsWfs:BsWfsElement", namespaces=gml.nsmap)
    groups = itertools.groupby(elements, _compare_element_id)

    return [reduce(_merge, e, {}) for _, e in groups]


def _gml_find(gml, search_term):
    return gml.findtext(".//" + search_term, namespaces=gml.nsmap)


def _parse_feature(gml):
    coords = _gml_find(gml, "gml:pos")
    lon, lat = coords.strip().split(" ")

    prop = _gml_find(gml, "BsWfs:ParameterName")
    value = _gml_find(gml, "BsWfs:ParameterValue")
    time_prop = _gml_find(gml, "BsWfs:Time")

    unix_timestamp = int(timeparse(time_prop).timestamp())

    return {
        "property": prop,
        "value": value,
        "timestamp": unix_timestamp,
        "coordinates": {"lat": float(lat), "lon": float(lon)},
    }
