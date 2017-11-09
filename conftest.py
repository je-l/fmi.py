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
        return f.read()


@pytest.fixture(scope="session")
def example_node(example_gml):
    parsed = etree.fromstring(example_gml)
    xpath = ".//BsWfs:BsWfsElement"
    return parsed.find(xpath, namespaces=parsed.nsmap)
