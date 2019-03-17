from datetime import datetime

from fmi.wfs_parse import (
    parse_latest_observations,
    _parse_feature,
    _extract_node_id,
    _dict_to_observation,
    _parse_exception,
    parse_forecast,
    parse_sea_levels,
    _parse_watlev_property,
)

from pytest import approx


def test_wfs_observation_parsing(observation_gml):
    parsed = parse_latest_observations(observation_gml)
    before_len = len(observation_gml)
    after_len = len(parsed)
    assert after_len < before_len


def test_wfs_parse_coords(observation_node):
    parsed = _parse_feature(observation_node)
    lat = float(parsed["lat"])
    lon = float(parsed["lon"])

    assert lon > 0
    assert lat < 100


def test_wfs_parse_property(observation_node):
    parsed = _parse_feature(observation_node)
    prop = parsed["property"]

    assert prop == "t2m"


def test_compare_element_id(observation_node):
    res = _extract_node_id(observation_node)
    assert len(res) == 2


def test_time_parsed_exact(observation_node):
    parsed_node = _parse_feature(observation_node)
    result_timestamp = datetime.utcfromtimestamp(parsed_node["timestamp"])
    assert result_timestamp.hour == 3
    assert result_timestamp.minute == 20


def test_parse_forecast_not_empty(forecast_gml):
    forecasts = parse_forecast(forecast_gml)

    assert forecasts


def test_parse_forecast_has_temperature(forecast_gml):
    forecast = parse_forecast(forecast_gml)[0]

    assert forecast.temperature == approx(0.08)


def test_parse_forecast_has_text_representation(forecast_gml):
    forecast = parse_forecast(forecast_gml)[0]

    assert forecast.weather_text == "pilvistä"


def test_parse_exception(api_exception):
    res = _parse_exception(api_exception)

    assert "ParsingFailed" in res
    assert "language" in res


def test_parse_sea_level_valid_timestamp(sea_level_gml):
    unix_timestamp, _ = parse_sea_levels(sea_level_gml)[0]
    datetime.utcfromtimestamp(unix_timestamp)


def test_parse_sea_level_value(sea_level_gml):
    sea_levels = parse_sea_levels(sea_level_gml)
    _, sea_level = sea_levels[0]

    assert sea_level == 452


def test_sea_level_trailing_null_is_removed(sea_level_gml):
    sea_levels = parse_sea_levels(sea_level_gml)
    _, sea_level = sea_levels[-1]

    assert sea_level is not None


def test_parse_null_watlev_property():
    example = {"WATLEV": "NaN"}
    result = _parse_watlev_property(example)
    assert result is None


def test_parse_watlev_property():
    example = {"WATLEV": 465.0}
    result = _parse_watlev_property(example)
    assert result == 465
