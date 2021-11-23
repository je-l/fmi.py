from typing import Callable, Dict, Optional, Union, Any
from pprint import pformat

from fmi.constant import OBSERVATION_CODES, FORECAST_CODES

OBSERVATION_PARAMS: Dict[str, Callable[[str], Union[float, int]]] = {
    "n_man": float,
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

OBSERVATION_SCHEMA: Dict[str, Callable[[str], Any]] = {
    "lat": float,
    "lon": float,
    "timestamp": int,
    **OBSERVATION_PARAMS,
}


class Coordinates:
    def __init__(self, lat: float, lon: float) -> None:
        #:
        self.lat = lat

        #:
        self.lon = lon


class Observation:
    """Represents single weather condition state."""

    def __init__(
        self,
        coordinates: Coordinates,
        timestamp: int,
        temperature: Optional[float] = None,
        humidity: Optional[int] = None,
        clouds: Optional[float] = None,
        dewpoint: Optional[float] = None,
        pressure: Optional[int] = None,
        precipitation_1h: Optional[float] = None,
        snow: Optional[int] = None,
        visibility: Optional[int] = None,
        wind_direction: Optional[int] = None,
        wind_gust: Optional[int] = None,
        wind_speed: Optional[int] = None,
        wawa: Optional[int] = None,
    ) -> None:
        #: dictionary of lat/lon WGS84 coordinates for the interpreted place
        self.coordinates = coordinates

        #: clouds 0-8
        self.clouds = clouds

        #: pressure at sea level
        self.pressure = pressure

        #: rain (1h average)
        self.precipitation_1h = precipitation_1h

        #: relative humidity percentage
        self.humidity = humidity

        #: snow in millimeters
        self.snow = snow

        #: temperature in celsius at two meters from ground surface
        self.temperature = temperature

        #: dew point
        self.dewpoint = dewpoint

        #: observation timestamp in unix seconds
        self.timestamp = timestamp

        #: visibility in meters
        self.visibility = visibility

        #: wind direction in degrees for 10 minutes
        self.wind_direction = wind_direction

        #: wind gust for 10 minutes
        self.wind_gust = wind_gust

        #: wind speed for 10 minutes
        self.wind_speed = wind_speed

        self._wawa = wawa

    @property
    def weather_text(self) -> Optional[str]:
        """finnish description for the observation"""
        if self._wawa:
            return OBSERVATION_CODES[self._wawa]
        return None

    def __str__(self) -> str:
        return pformat(self.__dict__)


class Forecast:
    """Data class for representing forecast API responses"""

    def __init__(
        self,
        dewpoint: float,
        height: float,
        high_cloud_cover: float,
        humidity: float,
        landseamask: float,
        low_cloud_cover: float,
        max_wind: float,
        med_cloud_cover: float,
        precipitation_1h: float,
        precipitation_amount: float,
        pressure: float,
        radiation_diffuse_acc: float,
        radiation_global_acc: float,
        radiation_lwa_acc: float,
        radiation_netsurface_lwa_acc: float,
        radiation_netsurface_swa_acc: float,
        temperature: float,
        total_cloud_cover: float,
        wind_direction: int,
        wind_gust: float,
        wind_speed: float,
        wind_ums: float,
        wind_vms: float,
        coordinates: Coordinates,
        timestamp: int,
        weather_symbol_code: int,
    ) -> None:
        #: dew point
        self.dewpoint: float = dewpoint

        #: geopotential height
        self.height = height

        #:
        self.high_cloud_cover = high_cloud_cover

        #: relative humidity percentage
        self.humidity = humidity

        #:
        self.landseamask = landseamask

        #:
        self.low_cloud_cover = low_cloud_cover

        #:
        self.max_wind = max_wind

        #:
        self.med_cloud_cover = med_cloud_cover

        #: rain (1h average)
        self.precipitation_1h = precipitation_1h

        #: rain amount
        self.precipitation_amount = precipitation_amount

        #: pressure at sea level
        self.pressure = pressure

        #:
        self.radiation_diffuse_acc = radiation_diffuse_acc

        #:
        self.radiation_global_acc = radiation_global_acc

        #:
        self.radiation_lwa_acc = radiation_lwa_acc

        #:
        self.radiation_netsurface_lwa_acc = radiation_netsurface_lwa_acc

        #:
        self.radiation_netsurface_swa_acc = radiation_netsurface_swa_acc

        #: temperature in celsius at two meters from ground surface
        self.temperature = temperature

        #:
        self.total_cloud_cover = total_cloud_cover

        #: wind direction in degrees for 10 minutes
        self.wind_direction = wind_direction

        #: wind gust for 10 minutes
        self.wind_gust = wind_gust

        #: wind speed for 10 minutes
        self.wind_speed = wind_speed

        #:
        self.wind_ums = wind_ums

        #:
        self.wind_vms = wind_vms

        #: dictionary of lat/lon WGS84 coordinates for the interpreted place
        self.coordinates = coordinates

        #: observation timestamp in unix seconds
        self.timestamp = timestamp

        self._weather_symbol_code = weather_symbol_code

    @property
    def weather_text(self) -> Optional[str]:
        """finnish description for the observation"""
        if self._weather_symbol_code:
            return FORECAST_CODES[self._weather_symbol_code]

        return None

    def __str__(self) -> str:
        return pformat(self.__dict__)
