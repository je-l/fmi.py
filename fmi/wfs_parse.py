import itertools
from functools import reduce
from dateutil.parser import parse as timeparse
from lxml import etree
from fmi import Observation, Forecast
from fmi.model import OBSERVATION_SCHEMA


def _extract_features(gml):
    parsed_gml = etree.fromstring(gml)
    if parsed_gml.tag.endswith("ExceptionReport"):
        error_reason = _parse_exception(parsed_gml)
        raise ValueError(error_reason)

    elements = parsed_gml.findall(".//BsWfs:BsWfsElement",
                                  namespaces=parsed_gml.nsmap)

    groups = itertools.groupby(elements, _extract_node_id)

    return [reduce(_merge, e, {}) for _, e in groups]


def parse_latest_observations(gml):
    """Parse latest observations gml into observation objects.
    :param gml: raw gml text
    :returns: list of latest observations
    :raises ValueError: error raised if fmi api returns error
    """

    merged = _extract_features(gml)
    return [_dict_to_observation(i) for i in merged]


def parse_forecast(gml):
    """Parse forecast API response into list of forecast objects.
    :param gml: raw gml
    :returns: list of forecast objects
    """
    merged = _extract_features(gml)
    return [Forecast(**i) for i in merged]


def _parse_watlev_property(feature):
    if feature["WATLEV"] == "NaN":
        return None

    return int(float(feature["WATLEV"]))


def parse_sea_levels(gml):
    """Parse sea level API response
    :param gml: input xml
    :returns: list of timestamp - sea level -pairs
    """
    raw_features = _extract_features(gml)

    timestamps = (o["timestamp"] for o in raw_features)
    sea_levels = (_parse_watlev_property(o) for o in raw_features)

    combined = list(zip(timestamps, sea_levels))

    while combined and combined[-1][1] is None:
        combined.pop()

    if not combined:
        raise ValueError("no sea level data available with given parameters")

    return combined


def _parse_exception(gml):
    exception_element = gml.find(".//Exception", namespaces=gml.nsmap)
    error_code = exception_element.get("exceptionCode")

    text = _gml_find(gml, "ExceptionText")
    return "[{}] {}".format(error_code, text)


def _extract_node_id(element):
    id_text = element.values()[0]
    element_id = id_text.split(".", 1)[1]
    return element_id.split(".", 2)[:2]


def _dict_to_observation(obs):
    # Replace "NaN" with None
    for key, val in obs.items():
        if val == "NaN":
            obs[key] = None
        else:
            obs[key] = OBSERVATION_SCHEMA[key](val)

    return Observation(**obs)


def _merge(acc, cur):
    """Reducer function for aggregating feature properties into one dict"""
    parsed = _parse_feature(cur)
    acc["timestamp"] = parsed["timestamp"]
    acc["coordinates"] = parsed["coordinates"]
    key = parsed["property"]
    val = parsed["value"]

    acc[key] = val

    return acc


def _gml_find(gml, search_term):
    element_text = gml.findtext(".//" + search_term, namespaces=gml.nsmap)
    return element_text.strip()


def _parse_feature(gml):
    coords = _gml_find(gml, "gml:pos")
    lat, lon = coords.strip().split(" ")

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
