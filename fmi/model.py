observation_schema = {
    "coordinates": dict,
    "t2m": float,
    "p_sea": float,
    "rh": float,
    "r_1h": float,
    "ri_10min": float,
    "snow_aws": float,
    "td": float,
    "timestamp": int,
    "vis": float,
    "wd_10min": float,
    "wg_10min": float,
    "ws_10min": float
}


class Observation:
    """Represents single past observation from weather station

    :ivar coordinates: dictionary of lat/lon WGS84 coordinates for the weather
        station
    :ivar p_sea: pressure at sea level
    :ivar rh: relative humidity percentage
    :ivar snow_aws: snowfall
    :ivar t2m: temperature in celsius at two meters from ground surface
    :ivar timestamp: observation timestamp in unix seconds
    :ivar vis: visibility in meters
    :ivar wd_10min: wind direction in degrees for 10 minutes
    :ivar wg_10min: wind gust for 10 minutes
    :ivar ws_10min: wind speed for 10 minutes
    """
    def __init__(self, **kwargs):
        self.coordinates = kwargs.get("coordinates")
        self.p_sea = kwargs.get("p_sea")
        self.r_1h = kwargs.get("r_1h")
        self.rh = kwargs.get("rh")
        self.ri_10min = kwargs.get("ri_10min")
        self.snow_aws = kwargs.get("snow_aws")
        self.t2m = kwargs.get("t2m")
        self.td = kwargs.get("td")
        self.timestamp = kwargs.get("timestamp")
        self.vis = kwargs.get("vis")
        self.wd_10min = kwargs.get("wd_10min")
        self.wg_10min = kwargs.get("wg_10min")
        self.ws_10min = kwargs.get("ws_10min")

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)
