from distutils.core import setup
import os


dependencies = [
    "lxml",
    "aiohttp",
    "python-dateutil",
]

setup(name="fmi.py",
      version="0.2.0",
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
              "pytest", "pytest-asyncio"],
          "docs": [
              "sphinxcontrib-asyncio"]})
