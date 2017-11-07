class Observation:
    """Represents single past observation from weather station

    :cvar coordinates: location for the weather station in WGS84 lat/lon format
    :cvar p_sea: pressure at sea level
    ...
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

