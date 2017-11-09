from fmi import Client
from os import path
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


