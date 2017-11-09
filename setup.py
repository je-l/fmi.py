from distutils.core import setup


dependencies = [
    "lxml",
    "aiohttp",
    "python-dateutil",
]

setup(name="fmi.py",
      version="0.1.0",
      description="Fmi api wrapper",
      author="je-l",
      url="https://www.github.com/je-l/fmi.py",
      packages=["fmi"],
      install_requires=dependencies,
      extras_require={
          "tests": [
              "pytest"],
          "docs": [
              "sphinxcontrib-asyncio"]})
