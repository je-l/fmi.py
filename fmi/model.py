from pprint import pformat
from fmi.constant import OBSERVATION_CODES, FORECAST_CODES

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
    """Represents single weather condition state, either an observation or
    forecast.

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
    :ivar wawa: description for the observation (only finnish)
    """
    def __init__(self, **kwargs):
        self.coordinates = kwargs.get("coordinates")
        self.p_sea = kwargs.get("p_sea")
        self.r_1h = kwargs.get("r_1h")
        self.rh = kwargs.get("rh")
        self.snow_aw = kwargs.get("snow_aw")
        self.t2m = kwargs.get("t2m")
        self.td = kwargs.get("td")
        self.timestamp = kwargs.get("timestamp")
        self.vis = kwargs.get("vis")
        self.wd_10min = kwargs.get("wd_10min")
        self.wg_10min = kwargs.get("wg_10min")
        self.ws_10min = kwargs.get("ws_10min")
        self._wawa = kwargs.get("wawa")

    @property
    def wawa(self):
        return OBSERVATION_CODES.get(self._wawa)

    def __str__(self):
        return pformat(self.__dict__)


class Forecast:
    """Data class for representing forecast API responses"""

    def __init__(self, **kwargs):
        self.dewpoint = float(kwargs.get("DewPoint"))
        self.height = float(kwargs.get("GeopHeight"))
        self.high_cloud_cover = float(kwargs.get("HighCloudCover"))
        self.humidity = float(kwargs.get("Humidity"))
        self.landseamask = float(kwargs.get("LandSeaMask"))
        self.low_cloud_cover = float(kwargs.get("LowCloudCover"))
        self.max_wind = float(kwargs.get("MaximumWind"))
        self.med_cloud_cover = float(kwargs.get("MediumCloudCover"))
        self.precipitation_1h = float(kwargs.get("Precipitation1h"))
        self.precipitation_amount = float(kwargs.get("PrecipitationAmount"))
        self.pressure = float(kwargs.get("Pressure"))

        self.radiation_diffuse_acc = \
            float(kwargs.get("RadiationDiffuseAccumulation"))

        self.radiation_global_acc = \
            float(kwargs.get("RadiationGlobalAccumulation"))

        self.radiation_lwa_acc = \
            float(kwargs.get("RadiationLWAccumulation"))

        self.radiation_netsurface_lwa_acc = \
            float(kwargs.get("RadiationNetSurfaceLWAccumulation"))

        self.radiation_netsurface_swa_acc = \
            float(kwargs.get("RadiationNetSurfaceSWAccumulation"))

        self.temperature = float(kwargs.get("Temperature"))
        self.total_cloud_cover = float(kwargs.get("TotalCloudCover"))
        self.wind_direction = float(kwargs.get("WindDirection"))
        self.wind_gust = float(kwargs.get("WindGust"))
        self.wind_speed = float(kwargs.get("WindSpeedMS"))
        self.wind_ums = float(kwargs.get("WindUMS"))
        self.wind_vms = float(kwargs.get("WindVMS"))
        self.coordinates = kwargs.get("coordinates")
        self.timestamp = kwargs.get("timestamp")

        self._WeatherSymbol3 = int(float(kwargs.get("WeatherSymbol3")))

    @property
    def weather_text(self):
        return FORECAST_CODES.get(self._WeatherSymbol3)

    def __str__(self):
        return pformat(self.__dict__)

