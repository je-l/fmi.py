from lxml import etree
import itertools
from functools import reduce
from dateutil.parser import parse as timeparse

from fmi import Observation
from fmi.model import observation_schema


def _compare_element_id(element):
    id_text = element.values()[0]
    element_id = id_text.split(".", 1)[1]
    return element_id.split(".", 2)[:2]


def parse_latest_observations(gml):
    """Parse latest observations object into python dict.
    :param gml: lxml Element
    :return: list of latest observations
    """
    parsed_gml = etree.fromstring(gml)

    elements = parsed_gml.findall(".//BsWfs:BsWfsElement",
                                  namespaces=parsed_gml.nsmap)

    groups = itertools.groupby(elements, _compare_element_id)

    merged = [reduce(_merge, e, {}) for _, e in groups]
    return [_dict_to_observation(i) for i in merged]


def _dict_to_observation(obs):
    # Replace "NaN" with None
    for k, v in obs.items():
        if v == "NaN":
            obs[k] = None
        else:
            obs[k] = observation_schema[k](v)

    return Observation(**obs)



def _merge(acc, cur):
    parsed = _parse_feature(cur)
    acc["timestamp"] = parsed["timestamp"]
    acc["coordinates"] = parsed["coordinates"]
    key = parsed["property"]
    val = parsed["value"]

    acc[key] = val

    return acc


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

