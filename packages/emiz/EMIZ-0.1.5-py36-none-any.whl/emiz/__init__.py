# coding=utf-8

from pkg_resources import DistributionNotFound, get_distribution

from .miz import Mission, Miz
from .parking_spots import parkings
from .weather import MissionWeather, set_weather_from_icao

try:
    __version__ = get_distribution('emiz').version
except DistributionNotFound:  # pragma: no cover
    # package is not installed
    __version__ = 'not installed'
