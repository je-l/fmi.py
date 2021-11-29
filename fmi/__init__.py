from .model import Observation, Forecast, Coordinates
from .fmi import latest_observations, forecast, weather_now, sea_levels
from .__version__ import __version__

__all__ = [
    "Observation",
    "Forecast",
    "Coordinates",
    "latest_observations",
    "forecast",
    "weather_now",
    "sea_levels",
]
