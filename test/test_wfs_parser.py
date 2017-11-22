from fmi.wfs_parse import (
    parse_latest_observations,
    _parse_feature,
    _extract_node_id,
    _dict_to_observation,
    _parse_exception,
    parse_forecast,
)

from datetime import datetime
from pytest import approx


def test_wfs_observation_parsing(observation_gml):
    parsed = parse_latest_observations(observation_gml)
    before_len = len(observation_gml)
    after_len = len(parsed)
    assert after_len < before_len


def test_wfs_parse_coords(observation_node):
    parsed = _parse_feature(observation_node)
    coords = parsed["coordinates"]

    assert coords["lon"] > 0
    assert coords["lat"] < 100


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


def test_create_observation():
    example = {"t2m": 14.5}
    parsed = _dict_to_observation(example)
    assert parsed.temperature == approx(14.5)


def test_should_not_have_nan_in_observation():
    example = {"t2m": "NaN"}
    parsed = _dict_to_observation(example)
    assert "NaN" not in parsed.__dict__.values()


def test_parse_forecast_not_empty(forecast_gml):
    forecasts = parse_forecast(forecast_gml)

    assert len(forecasts) > 0


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