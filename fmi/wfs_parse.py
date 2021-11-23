from typing import List, Dict, Optional, Tuple, Any

import itertools
from functools import reduce
from dateutil.parser import parse as timeparse
from lxml import etree
from fmi.model import OBSERVATION_SCHEMA, Forecast, Observation, Coordinates


def _read_raw_gml(gml: bytes) -> Any:
    is_invalid_api_key = gml.startswith(b"<html>")

    if is_invalid_api_key:
        raise ValueError("invalid api key")

    parsed_gml = etree.fromstring(gml)
    if parsed_gml.tag.endswith("ExceptionReport"):
        error_reason = _parse_exception(parsed_gml)
        raise ValueError(error_reason)

    return parsed_gml


def _extract_features(gml: bytes) -> List[Dict[str, str]]:
    parsed_gml = _read_raw_gml(gml)

    elements = parsed_gml.findall(
        ".//BsWfs:BsWfsElement", namespaces=parsed_gml.nsmap
    )

    groups = itertools.groupby(elements, _extract_node_id)

    return [reduce(_merge, e, {}) for _, e in groups]


def parse_latest_observations(gml: bytes) -> List[Observation]:
    """Parse latest observations gml into observation objects.
    :param gml: raw gml text
    :returns: list of latest observations
    :raises ValueError: error raised if fmi api returns error
    """

    merged = _extract_features(gml)
    return [_dict_to_observation(i) for i in merged]


def parse_forecast(gml: bytes) -> List[Forecast]:
    """Parse forecast API response into list of forecast objects.
    :param gml: raw gml
    :returns: list of forecast objects
    """
    merged = _extract_features(gml)
    return [
        Forecast(
            dewpoint=float(i["DewPoint"]),
            height=float(i["GeopHeight"]),
            high_cloud_cover=float(i["HighCloudCover"]),
            humidity=float(i["Humidity"]),
            landseamask=float(i["LandSeaMask"]),
            low_cloud_cover=float(i["LowCloudCover"]),
            max_wind=float(i["MaximumWind"]),
            med_cloud_cover=float(i["MediumCloudCover"]),
            precipitation_1h=float(i["Precipitation1h"]),
            precipitation_amount=float(i["PrecipitationAmount"]),
            pressure=float(i["Pressure"]),
            radiation_diffuse_acc=float(i["RadiationDiffuseAccumulation"]),
            radiation_global_acc=float(i["RadiationGlobalAccumulation"]),
            radiation_lwa_acc=float(i["RadiationLWAccumulation"]),
            radiation_netsurface_lwa_acc=float(
                i["RadiationNetSurfaceLWAccumulation"]
            ),
            radiation_netsurface_swa_acc=float(
                i["RadiationNetSurfaceSWAccumulation"]
            ),
            temperature=float(i["Temperature"]),
            total_cloud_cover=float(i["TotalCloudCover"]),
            wind_direction=int(float(i["WindDirection"])),
            wind_gust=float(i["WindGust"]),
            wind_speed=float(i["WindSpeedMS"]),
            wind_ums=float(i["WindUMS"]),
            wind_vms=float(i["WindVMS"]),
            coordinates=Coordinates(float(i["lat"]), float(i["lon"])),
            timestamp=int(i["timestamp"]),
            weather_symbol_code=int(float(i["WeatherSymbol3"])),
        )
        for i in merged
    ]


def _parse_watlev_property(feature: Dict[str, str]) -> Optional[int]:
    if feature["WATLEV"] == "NaN":
        return None

    return int(float(feature["WATLEV"]))


def parse_sea_levels(gml: bytes) -> List[Tuple[str, Optional[int]]]:
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


def _parse_exception(gml: Any) -> str:
    exception_element = gml.find(".//Exception", namespaces=gml.nsmap)
    error_code = exception_element.get("exceptionCode")

    text = _gml_find(gml, "ExceptionText")
    return f"[{error_code}] {text}"


def _extract_node_id(element: Any) -> List[str]:
    id_text: str = element.values()[0]
    element_id = id_text.split(".", 1)[1]
    return element_id.split(".", 2)[:2]


def _dict_to_observation(obj: Dict[str, str]) -> Observation:
    obs = {k: OBSERVATION_SCHEMA[k](v) for k, v in obj.items() if v != "NaN"}

    return Observation(
        coordinates=Coordinates(float(obs["lat"]), float(obs["lon"])),
        pressure=int(obs["p_sea"]) if "p_sea" in obs else None,
        precipitation_1h=float(obs["r_1h"]) if "r_1h" in obs else None,
        humidity=int(obs["rh"]) if "rh" in obs else None,
        snow=int(obs["snow_aws"]) if "snow_aws" in obs else None,
        temperature=float(obs["t2m"]) if "t2m" in obs else None,
        dewpoint=float(obs["td"]) if "td" in obs else None,
        timestamp=int(obs["timestamp"]),
        visibility=int(obs["vis"]) if "vis" in obs else None,
        wind_direction=int(obs["wd_10min"]) if "wd_10min" in obs else None,
        wind_gust=int(obs["wg_10min"]) if "wg_10min" in obs else None,
        wind_speed=int(obs["ws_10min"]) if "ws_10min" in obs else None,
        clouds=int(obs["n_man"]) if "n_man" in obs else None,
        wawa=int(obs["wawa"]) if "wawa" in obs else None,
    )


def _merge(acc: Dict[str, str], cur: Any) -> Dict[str, str]:
    """Reducer function for aggregating feature properties into one dict"""
    parsed = _parse_feature(cur)
    acc["timestamp"] = parsed["timestamp"]
    acc["lat"] = parsed["lat"]
    acc["lon"] = parsed["lon"]
    key = parsed["property"]
    val = parsed["value"]

    acc[key] = val

    return acc


def _gml_find(gml: Any, search_term: str) -> str:
    element_text: str = gml.findtext(".//" + search_term, namespaces=gml.nsmap)
    return element_text.strip()


def _parse_feature(gml: Any) -> Dict[str, Any]:
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
        "lat": lat,
        "lon": lon,
    }
