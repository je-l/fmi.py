from distutils.core import setup
import os

from os import path

FILE_PATH = path.dirname(path.realpath(__file__))

info = {}
# package version
with open(path.join(FILE_PATH, "fmi", "__version__.py")) as f:
    exec(f.read(), info)


dependencies = [
    "lxml>=4.1.1,<5.0.0",
    "aiohttp>=2.3.3,<3.0.0",
    "python-dateutil>=2.6.1,<3.0.0",
]

setup(name="fmi.py",
      version=info["__version__"],
      description="Fmi api wrapper",
      long_description="http://fmipy.readthedocs.io/en/latest/",
      url="https://www.github.com/je-l/fmi.py",
      author="je-l",
      author_email=os.environ.get("PYPI_MAIL"),
      packages=["fmi"],
      install_requires=dependencies,
      classifiers=["Development Status :: 4 - Beta",
                   "Programming Language :: Python :: 3.5",
                   "Programming Language :: Python :: 3.6",
                   "Framework :: AsyncIO"],
      extras_require={
          "tests": [
              "pytest>=3.2.5,<4.0.0", "pytest-asyncio==0.8.0"],
          "docs": [
              "sphinxcontrib-asyncio==0.2.0", "sphinx-rtd-theme==0.2.4"]})
