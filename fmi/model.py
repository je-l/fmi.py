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
    "vis": lambda s: int(float(s)),
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
    """Represents single weather condition state."""

    def __init__(self, **kwargs):
        #: dictionary of lat/lon WGS84 coordinates for the interpreted place
        self.coordinates = kwargs.get("coordinates")

        #: pressure at sea level
        self.pressure = kwargs.get("p_sea")

        #: rain (1h average)
        self.precipitation_1h = kwargs.get("r_1h")

        #: relative humidity percentage
        self.humidity = kwargs.get("rh")

        #: snow in millimeters
        self.snow = kwargs.get("snow_aws")

        #: temperature in celsius at two meters from ground surface
        self.temperature = kwargs.get("t2m")

        #: dew point
        self.dewpoint = kwargs.get("td")

        #: observation timestamp in unix seconds
        self.timestamp = kwargs.get("timestamp")

        #: visibility in meters
        self.visibility = kwargs.get("vis")

        #: wind direction in degrees for 10 minutes
        self.wind_direction = kwargs.get("wd_10min")

        #: wind gust for 10 minutes
        self.wind_gust = kwargs.get("wg_10min")

        #: wind speed for 10 minutes
        self.wind_speed = kwargs.get("ws_10min")

        self._wawa = kwargs.get("wawa")

    @property
    def weather_text(self):
        """finnish description for the observation"""
        return OBSERVATION_CODES.get(self._wawa)

    def __str__(self):
        return pformat(self.__dict__)


class Forecast:
    """Data class for representing forecast API responses"""

    def __init__(self, **kwargs):
        #: dew point
        self.dewpoint = float(kwargs.get("DewPoint"))

        #: geopotential height
        self.height = float(kwargs.get("GeopHeight"))

        #:
        self.high_cloud_cover = float(kwargs.get("HighCloudCover"))

        #: relative humidity percentage
        self.humidity = float(kwargs.get("Humidity"))

        #:
        self.landseamask = float(kwargs.get("LandSeaMask"))

        #:
        self.low_cloud_cover = float(kwargs.get("LowCloudCover"))

        #:
        self.max_wind = float(kwargs.get("MaximumWind"))

        #:
        self.med_cloud_cover = float(kwargs.get("MediumCloudCover"))

        #: rain (1h average)
        self.precipitation_1h = float(kwargs.get("Precipitation1h"))

        #: rain amount
        self.precipitation_amount = float(kwargs.get("PrecipitationAmount"))

        #: pressure at sea level
        self.pressure = float(kwargs.get("Pressure"))

        #:
        self.radiation_diffuse_acc = \
            float(kwargs.get("RadiationDiffuseAccumulation"))

        #:
        self.radiation_global_acc = \
            float(kwargs.get("RadiationGlobalAccumulation"))

        #:
        self.radiation_lwa_acc = \
            float(kwargs.get("RadiationLWAccumulation"))

        #:
        self.radiation_netsurface_lwa_acc = \
            float(kwargs.get("RadiationNetSurfaceLWAccumulation"))

        #:
        self.radiation_netsurface_swa_acc = \
            float(kwargs.get("RadiationNetSurfaceSWAccumulation"))

        #: temperature in celsius at two meters from ground surface
        self.temperature = float(kwargs.get("Temperature"))

        #:
        self.total_cloud_cover = float(kwargs.get("TotalCloudCover"))

        #: wind direction in degrees for 10 minutes
        self.wind_direction = float(kwargs.get("WindDirection"))

        #: wind gust for 10 minutes
        self.wind_gust = float(kwargs.get("WindGust"))

        #: wind speed for 10 minutes
        self.wind_speed = float(kwargs.get("WindSpeedMS"))

        #:
        self.wind_ums = float(kwargs.get("WindUMS"))

        #:
        self.wind_vms = float(kwargs.get("WindVMS"))

        #: dictionary of lat/lon WGS84 coordinates for the interpreted place
        self.coordinates = kwargs.get("coordinates")

        #: observation timestamp in unix seconds
        self.timestamp = kwargs.get("timestamp")

        self._weather_symbol_code = int(float(kwargs.get("WeatherSymbol3")))

    @property
    def weather_text(self):
        """finnish description for the observation"""
        return FORECAST_CODES.get(self._weather_symbol_code)

    def __str__(self):
        return pformat(self.__dict__)
