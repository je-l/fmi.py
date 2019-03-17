from setuptools import setup
import os
import sys

from os import path

FILE_PATH = path.dirname(path.realpath(__file__))

info = {}
# package version
with open(path.join(FILE_PATH, "fmi", "__version__.py")) as f:
    exec(f.read(), info)

setup(
    name="fmi.py",
    version=info["__version__"],
    description="Finnish Meteorological Institute API wrapper",
    long_description="http://fmipy.readthedocs.io/en/latest/",
    url="https://www.github.com/je-l/fmi.py",
    author="je-l",
    packages=["fmi"],
    package_data={"fmi": ["py.typed"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: AsyncIO",
        "Typing :: Typed",
    ],
    python_requires=">=3.5",
    install_requires=[
        "lxml>=4.1.1,<5.0.0",
        "aiohttp>=3.0.8,<4.0.0",
        "python-dateutil>=2.6.1,<3.0.0",
    ],
)
