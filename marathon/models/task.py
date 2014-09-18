from datetime import datetime

from .base import MarathonResource


class MarathonTask(MarathonResource):
    """Marathon Task resource.

    :param str app_id: application id
    :param str host: mesos slave running the task
    :param str id: task id
    :param list[int] ports: allocated ports
    :param staged_at: when this task was staged
    :type staged_at: datetime or str
    :param started_at: when this task was started
    :type started_at: datetime or str
    :param str version: app version with which this task was started
    """

    DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

    def __init__(self, app_id=None, host=None, id=None, ports=None, staged_at=None, started_at=None, version=None):
        self.app_id = app_id
        self.host = host
        self.id = id
        self.ports = ports or []
        self.staged_at = staged_at if (staged_at is None or isinstance(staged_at, datetime)) \
            else datetime.strptime(staged_at, self.DATETIME_FORMAT)
        self.started_at = started_at if (started_at is None or isinstance(started_at, datetime)) \
            else datetime.strptime(started_at, self.DATETIME_FORMAT)
        self.version = version
