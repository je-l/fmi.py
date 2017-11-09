from fmi.wfs_parse import (
    parse_latest_observations,
    _parse_feature,
    _compare_element_id,
    _dict_to_observation,
)

from datetime import datetime
from pytest import approx


def test_wfs_observation_parsing(example_gml):
    parsed = parse_latest_observations(example_gml)
    before_len = len(example_gml)
    after_len = len(parsed)
    assert after_len < before_len


def test_wfs_parse_coords(example_node):
    parsed = _parse_feature(example_node)
    coords = parsed["coordinates"]

    assert coords["lon"] > 0
    assert coords["lat"] < 100


def test_wfs_parse_property(example_node):
    parsed = _parse_feature(example_node)
    prop = parsed["property"]

    assert prop == "t2m"


def test_compare_element_id(example_node):
    res = _compare_element_id(example_node)
    assert len(res) == 2


def test_time_parsed_exact(example_node):
    parsed_node = _parse_feature(example_node)
    result_timestamp = datetime.utcfromtimestamp(parsed_node["timestamp"])
    assert result_timestamp.hour == 3
    assert result_timestamp.minute == 20


def test_create_observation():
    example = {"t2m": 14.5}
    parsed = _dict_to_observation(example)
    assert parsed.t2m == approx(14.5)


def test_should_not_have_nan_in_observation():
    example = {"t2m": "NaN"}
    parsed = _dict_to_observation(example)
    assert "NaN" not in parsed.__dict__.values()
