from distutils.core import setup
import os

from os import path

FILE_PATH = path.dirname(path.realpath(__file__))

info = {}
# package version
with open(path.join(FILE_PATH, "fmi", "__version__.py")) as f:
    exec(f.read(), info)

setup(name="fmi.py",
      version=info["__version__"],
      description="Finnish Meteorological Institute API wrapper",
      long_description="http://fmipy.readthedocs.io/en/latest/",
      url="https://www.github.com/je-l/fmi.py",
      author="je-l",
      packages=["fmi"],
      classifiers=["Development Status :: 4 - Beta",
                   "Programming Language :: Python :: 3.5",
                   "Programming Language :: Python :: 3.6",
                   "Framework :: AsyncIO"],
      python_requires=">=3.5",
      install_requires=[
          "lxml>=4.1.1,<5.0.0",
          "aiohttp>=2.3.3,<3.0.0",
          "python-dateutil>=2.6.1,<3.0.0"],
      extras_require={
          "dev": [
              "pytest>=3.2.5,<4.0.0",
              "pytest-asyncio==0.8.0",
              "pytest-cov>=2.5.1,<3.0.0",
              "pylint==1.8.3",
              "twine"],
          "docs": [
              "sphinx>=1.7.2,<2.0.0",
              "sphinxcontrib-asyncio==0.2.0",
              "sphinx-rtd-theme==0.2.4"]
      })
