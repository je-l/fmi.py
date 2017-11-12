from fmi.constant import WAWA_CODES

OBSERVATION_PARAMS = {
    "t2m": float,
    "p_sea": float,
    "rh": float,
    "r_1h": float,
    "ri_10min": float,
    "snow_aws": float,
    "td": float,
    "vis": float,
    "wd_10min": float,
    "wg_10min": float,
    "ws_10min": float,
    "wawa": lambda s: int(float(s)),
}

OBSERVATION_SCHEMA = {
    "coordinates": dict,
    "timestamp": int,
    **OBSERVATION_PARAMS,
}


class Observation:
    """Represents single past observation from weather station

    :ivar coordinates: dictionary of lat/lon WGS84 coordinates for the weather
        station
    :ivar p_sea: pressure at sea level
    :ivar r_1h: rain (1h average)
    :ivar rh: relative humidity percentage
    :ivar snow_aws: snowfall
    :ivar t2m: temperature in celsius at two meters from ground surface
    :ivar td: dew point
    :ivar timestamp: observation timestamp in unix seconds
    :ivar vis: visibility in meters
    :ivar wd_10min: wind direction in degrees for 10 minutes
    :ivar wg_10min: wind gust for 10 minutes
    :ivar ws_10min: wind speed for 10 minutes
    :ivar wawa: description code of the observation
    """
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def verbal(self):
        """Get verbal representation of the observation. Only in finnish
        (sorry)
        """
        if not self.wawa:
            return None

        return WAWA_CODES[self.wawa]

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)
