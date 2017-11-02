from distutils.core import setup

required = [
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
      install_requires=required,
      tests_require=["pytest"],
     )
