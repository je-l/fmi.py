from fmi import (
    Client,
    _parse_latest_observations,
    _parse_feature,
    _compare_element_id
)

from os import path
from datetime import datetime
import pytest


FILE_DIR = path.dirname(path.realpath(__file__))


def test_can_create_new_client():
    Client("aaa")


def test_can_pass_api_key():
    c = Client("ab132")
    assert c.base_url == "http://data.fmi.fi/fmi-apikey/ab132/wfs?"


def test_cannot_use_empty_api_key():
    with pytest.raises(ValueError):
        Client("")


def test_wfs_observation_parsing(example_gml):
    parsed = _parse_latest_observations(example_gml)
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
