"""
Pytest utility functions
"""

import pytest
from os import path, environ
from lxml import etree

import fmi

FIXTURE_DIR = path.join(path.dirname(path.realpath(__file__)), "fixture")


def parse_first_node(gml):
    parsed = etree.fromstring(gml)
    xpath = ".//BsWfs:BsWfsElement"
    return parsed.find(xpath, namespaces=parsed.nsmap)


@pytest.fixture(scope="session")
def observation_gml():
    """Create example gml byte array for test modules"""
    observation_file = path.join(FIXTURE_DIR, "salo_latest_observations.gml")

    with open(observation_file, "rb") as f:
        return f.read()


@pytest.fixture(scope="session")
def observation_node(observation_gml):
    return parse_first_node(observation_gml)


@pytest.fixture(scope="session")
def forecast_gml():
    forecast_file = path.join(FIXTURE_DIR, "salo_forecast.gml")

    with open(forecast_file, "rb") as f:
        return f.read()


@pytest.fixture(scope="session")
def forecast_node(forecast_gml):
    return parse_first_node(forecast_gml)


@pytest.fixture(scope="session")
def api_exception():
    with open(path.join(FIXTURE_DIR, "exception.gml"), "rb") as ex_file:
        return etree.fromstring(ex_file.read())


@pytest.fixture(scope="session")
def sea_level_gml():
    with open(path.join(FIXTURE_DIR, "sea_level.gml"), "rb") as gml_file:
        return gml_file.read()


@pytest.fixture(scope="session")
def real_client():
    key = environ.get("FMI_KEY")

    if not key:
        return None

    return fmi.Client(key)
