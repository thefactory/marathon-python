from .base import MarathonResource, MarathonObject
from ..util import to_datetime


class MarathonTask(MarathonResource):

    """Marathon Task resource.

    :param str app_id: application id
    :param health_check_results: health check results
    :type health_check_results: list[:class:`marathon.models.MarathonHealthCheckResult`] or list[dict]
    :param str host: mesos slave running the task
    :param str id: task id
    :param list[int] ports: allocated ports
    :param list[int] service_ports: ports exposed for load balancing
    :param str state: State of the task e.g. TASK_RUNNING
    :param str slave_id: Mesos slave id
    :param staged_at: when this task was staged
    :type staged_at: datetime or str
    :param started_at: when this task was started
    :type started_at: datetime or str
    :param str version: app version with which this task was started
    :type region: str
    :param region: fault domain region support in DCOS EE
    :type zone: str
    :param zone: fault domain zone support in DCOS EE
    :type role: str
    :param role: mesos role
    """

    DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

    def __init__(self, app_id=None, health_check_results=None, host=None, id=None, ports=None, service_ports=None,
                 slave_id=None, staged_at=None, started_at=None, version=None, ip_addresses=[], state=None, local_volumes=None,
                 region=None, zone=None, role=None):
        self.app_id = app_id
        self.health_check_results = health_check_results or []
        self.health_check_results = [
            hcr if isinstance(
                hcr, MarathonHealthCheckResult) else MarathonHealthCheckResult().from_json(hcr)
            for hcr in (health_check_results or []) if any(health_check_results)
        ]
        self.host = host
        self.id = id
        self.ports = ports or []
        self.service_ports = service_ports or []
        self.slave_id = slave_id
        self.staged_at = to_datetime(staged_at)
        self.started_at = to_datetime(started_at)
        self.state = state
        self.version = version
        self.ip_addresses = [
            ipaddr if isinstance(
                ip_addresses, MarathonIpAddress) else MarathonIpAddress().from_json(ipaddr)
            for ipaddr in (ip_addresses or [])]
        self.local_volumes = local_volumes or []
        self.region = region
        self.zone = zone
        self.role = role


class MarathonIpAddress(MarathonObject):
    """
    """
    def __init__(self, ip_address=None, protocol=None):
        self.ip_address = ip_address
        self.protocol = protocol


class MarathonHealthCheckResult(MarathonObject):

    """Marathon health check result.

    See https://mesosphere.github.io/marathon/docs/health-checks.html

    :param bool alive: boolean to determine task health
    :param int consecutive_failures: number of failed healthchecks in a row
    :param str first_success: first time when which healthcheck succeeded
    :param str last_failure: last time when which healthcheck failed
    :param str last_failure_cause: cause for last failure
    :param str last_success: last time when which healthcheck succeeded
    :param str task_id: task id
    :param str instance_id: instance id
    """

    DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

    def __init__(self, alive=None, consecutive_failures=None, first_success=None,
                 last_failure=None, last_success=None, task_id=None,
                 last_failure_cause=None, instance_id=None):
        self.alive = alive
        self.consecutive_failures = consecutive_failures
        self.first_success = to_datetime(first_success)
        self.last_failure = to_datetime(last_failure)
        self.last_success = to_datetime(last_success)
        self.task_id = task_id
        self.last_failure_cause = last_failure_cause
        self.instance_id = instance_id
