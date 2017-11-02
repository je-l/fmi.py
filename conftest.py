"""
Pytest utility functions
"""

import pytest
from os import path
from lxml import etree

FILE_DIR = path.dirname(path.realpath(__file__))


@pytest.fixture(scope="session")
def example_gml():
    """Create example gml tree for test modules"""
    directory = path.join(FILE_DIR,
                          "test",
                          "fixture",
                          "salo_latest_observations.gml")

    with open(directory, "rb") as f:
        salo_fixture = f.read()

    parsed = etree.fromstring(salo_fixture)

    return parsed


@pytest.fixture(scope="session")
def example_node(example_gml):
    xpath = ".//BsWfs:BsWfsElement"
    return example_gml.find(xpath, namespaces=example_gml.nsmap)
