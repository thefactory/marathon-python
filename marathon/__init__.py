import logging

from .client import MarathonClient
from .resources import MarathonApp, MarathonTask

log = logging.getLogger(__name__)
logging.basicConfig()