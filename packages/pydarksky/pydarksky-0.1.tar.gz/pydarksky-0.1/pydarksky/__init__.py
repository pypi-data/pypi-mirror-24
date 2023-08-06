import logging

from .darksky import DarkSky
from .weather import Weather


logging.getLogger(__name__).setLevel(logging.DEBUG)
logging.getLogger(__name__).addHandler(logging.NullHandler())
