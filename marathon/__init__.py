import logging

from .client import MarathonClient
from .models import MarathonResource, MarathonApp, MarathonTask, MarathonConstraint
from .exceptions import MarathonError, MarathonHttpError, NotFoundError, InvalidOperatorError

log = logging.getLogger(__name__)
logging.basicConfig()