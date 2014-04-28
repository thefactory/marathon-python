from datetime import datetime
try:
    import json
except ImportError:
    import simplejson as json

from marathon.models.base import MarathonResource


class MarathonTask(MarathonResource):
    """Marathon Task resource.

    :param str app_id: application id
    :param str host: mesos slave running the task
    :param str id: task id
    :param list[int] ports: allocated ports
    :param datetime staged_at: when this task was staged
    :param datetime started_at: when this task was started
    """

    # Example: 2014-02-12T01:49:12.293Z
    TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
    """Timestamp format used in Marathon responses"""

    def __init__(self, app_id=None, host=None, id=None, ports=None, staged_at=None, started_at=None):
        self.app_id = app_id
        self.host = host
        self.id = id
        self.ports = ports
        self.staged_at = staged_at
        self.started_at = started_at

    @classmethod
    def json_decode(cls, obj):
        """Construct a MarathonTask from a parsed response.

        :param dict obj: object obj from parsed response

        :rtype: :class:`MarathonApp`
        """
        return cls(
            app_id=obj.get('appId'),
            host=obj.get('host'),
            id=obj.get('id'),
            ports=obj.get('ports'),
            staged_at=datetime.strptime(obj.get('stagedAt'), cls.TIMESTAMP_FORMAT),
            started_at=datetime.strptime(obj.get('startedAt'), cls.TIMESTAMP_FORMAT)
        )

    def json_encode(self):
        """Construct a JSON-friendly representation of the object.

        :rtype: dict
        """
        return {
            'appId': self.app_id,
            'host': self.host,
            'id': self.id,
            'ports': self.ports,
            'staged_at': self.staged_at.strftime(self.TIMESTAMP_FORMAT),
            'started_at': self.started_at.strftime(self.TIMESTAMP_FORMAT)
        }