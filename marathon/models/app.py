from ..exceptions import InvalidChoiceError
from .base import MarathonResource, MarathonObject, assert_valid_path
from .constraint import MarathonConstraint
from .container import MarathonContainer
from .deployment import MarathonDeployment
from .task import MarathonTask
from ..util import get_log
from ..util import to_datetime

log = get_log()


class MarathonApp(MarathonResource):

    """Marathon Application resource.

    See: https://mesosphere.github.io/marathon/docs/rest-api.html#post-/v2/apps

    :param list[str] accepted_resource_roles: a list of resource roles (the resource offer
                                              must contain at least one of these for the app
                                              to be launched on that host)
    :param list[str] args: args form of the command to run
    :param int backoff_factor: multiplier for subsequent backoff
    :param int backoff_seconds: base time, in seconds, for exponential backoff
    :param str cmd: cmd form of the command to run
    :param constraints: placement constraints
    :type constraints: list[:class:`marathon.models.constraint.MarathonConstraint`] or list[tuple]
    :param container: container info
    :type container: :class:`marathon.models.container.MarathonContainer` or dict
    :param float cpus: cpus required per instance
    :param list[str] dependencies: services (app IDs) on which this app depends
    :param int disk: disk required per instance
    :param deployments: (read-only) currently running deployments that affect this app
    :type deployments: list[:class:`marathon.models.deployment.MarathonDeployment`]
    :param dict env: env vars
    :param str executor: executor
    :param int gpus: gpus required per instance
    :param health_checks: health checks
    :type health_checks: list[:class:`marathon.models.MarathonHealthCheck`] or list[dict]
    :param str id: app id
    :param str role: mesos role
    :param int instances: instances
    :param last_task_failure: last task failure
    :type last_task_failure: :class:`marathon.models.app.MarathonTaskFailure` or dict
    :param float mem: memory (in MB) required per instance
    :param dict secrets: A map with named secret declarations.
    :type port_definitions: list[:class:`marathon.models.app.PortDefinitions`] or list[dict]
    :param list[int] ports: ports
    :param bool require_ports: require the specified `ports` to be available in the resource offer
    :param list[str] store_urls: store URLs
    :param float task_rate_limit: (Removed in Marathon 0.7.0) maximum number of tasks launched per second
    :param tasks: (read-only) tasks
    :type tasks: list[:class:`marathon.models.task.MarathonTask`]
    :param int tasks_running: (read-only) the number of running tasks
    :param int tasks_staged: (read-only) the number of staged tasks
    :param int tasks_healthy: (read-only) the number of healthy tasks
    :param int tasks_unhealthy: (read-only) the number of unhealthy tasks
    :param upgrade_strategy: strategy by which app instances are replaced during a deployment
    :type upgrade_strategy: :class:`marathon.models.app.MarathonUpgradeStrategy` or dict
    :param list[str] uris: uris
    :param str user: user
    :param str version: version id
    :param version_info: time of last scaling, last config change
    :type version_info: :class:`marathon.models.app.MarathonAppVersionInfo` or dict
    :param task_stats: task statistics
    :type task_stats: :class:`marathon.models.app.MarathonTaskStats` or dict
    :param dict labels
    :type readiness_checks: list[:class:`marathon.models.app.ReadinessCheck`] or list[dict]
    :type residency: :class:`marathon.models.app.Residency` or dict
    :param int task_kill_grace_period_seconds: Configures the termination signal escalation behavior of executors when stopping tasks.
    :param list[dict] unreachable_strategy: Handling for unreachable instances.
    :param str kill_selection: Defines which instance should be killed first in case of e.g. rescaling.
    """

    UPDATE_OK_ATTRIBUTES = [
        'args', 'backoff_factor', 'backoff_seconds', 'cmd', 'constraints', 'container', 'cpus', 'dependencies', 'disk',
        'env', 'executor', 'gpus', 'health_checks', 'instances', 'kill_selection', 'labels', 'max_launch_delay_seconds',
        'mem', 'ports', 'require_ports', 'store_urls', 'task_rate_limit', 'upgrade_strategy', 'unreachable_strategy',
        'uris', 'user', 'version', 'role'
    ]
    """List of attributes which may be updated/changed after app creation"""

    CREATE_ONLY_ATTRIBUTES = ['id', 'accepted_resource_roles']
    """List of attributes that should only be passed on creation"""

    READ_ONLY_ATTRIBUTES = [
        'deployments', 'tasks', 'tasks_running', 'tasks_staged', 'tasks_healthy', 'tasks_unhealthy']
    """List of read-only attributes"""

    KILL_SELECTIONS = ["YOUNGEST_FIRST", "OLDEST_FIRST"]

    def __init__(self, accepted_resource_roles=None, args=None, backoff_factor=None, backoff_seconds=None, cmd=None,
                 constraints=None, container=None, cpus=None, dependencies=None, deployments=None, disk=None, env=None,
                 executor=None, health_checks=None, id=None, role=None, instances=None, kill_selection=None, labels=None,
                 last_task_failure=None, max_launch_delay_seconds=None, mem=None, ports=None, require_ports=None,
                 store_urls=None, task_rate_limit=None, tasks=None, tasks_running=None, tasks_staged=None,
                 tasks_healthy=None, task_kill_grace_period_seconds=None, tasks_unhealthy=None, upgrade_strategy=None,
                 unreachable_strategy=None, uris=None, user=None, version=None, version_info=None,
                 ip_address=None, fetch=None, task_stats=None, readiness_checks=None,
                 readiness_check_results=None, secrets=None, port_definitions=None, residency=None, gpus=None, networks=None):

        # self.args = args or []
        self.accepted_resource_roles = accepted_resource_roles
        self.args = args
        # Marathon 0.7.0-RC1 throws a validation error if this is [] and cmd is passed:
        # "error": "AppDefinition must either contain a 'cmd' or a 'container'."

        self.backoff_factor = backoff_factor
        self.backoff_seconds = backoff_seconds
        self.cmd = cmd
        self.constraints = [
            c if isinstance(c, MarathonConstraint) else MarathonConstraint(*c)
            for c in (constraints or [])
        ]
        self.container = container if (isinstance(container, MarathonContainer) or container is None) \
            else MarathonContainer.from_json(container)
        self.cpus = cpus
        self.dependencies = dependencies or []
        self.deployments = [
            d if isinstance(
                d, MarathonDeployment) else MarathonDeployment().from_json(d)
            for d in (deployments or [])
        ]
        self.disk = disk
        self.env = env or dict()
        self.executor = executor
        self.gpus = gpus
        self.health_checks = health_checks or []
        self.health_checks = [
            hc if isinstance(
                hc, MarathonHealthCheck) else MarathonHealthCheck().from_json(hc)
            for hc in (health_checks or [])
        ]
        self.id = assert_valid_path(id.lower())
        self.role = role
        self.instances = instances
        if kill_selection and kill_selection not in self.KILL_SELECTIONS:
            raise InvalidChoiceError(
                'kill_selection', kill_selection, self.KILL_SELECTIONS)
        self.kill_selection = kill_selection
        self.labels = labels or {}
        self.last_task_failure = last_task_failure if (isinstance(last_task_failure, MarathonTaskFailure) or last_task_failure is None) \
            else MarathonTaskFailure.from_json(last_task_failure)
        self.max_launch_delay_seconds = max_launch_delay_seconds
        self.mem = mem
        self.ports = ports or []
        self.port_definitions = [
            pd if isinstance(
                pd, PortDefinition) else PortDefinition.from_json(pd)
            for pd in (port_definitions or [])
        ]
        self.readiness_checks = [
            rc if isinstance(
                rc, ReadinessCheck) else ReadinessCheck().from_json(rc)
            for rc in (readiness_checks or [])
        ]
        self.readiness_check_results = readiness_check_results or []
        self.residency = residency
        self.require_ports = require_ports

        self.secrets = secrets or {}
        for k, s in self.secrets.items():
            if not isinstance(s, Secret):
                self.secrets[k] = Secret().from_json(s)

        self.store_urls = store_urls or []
        self.task_rate_limit = task_rate_limit
        self.tasks = [
            t if isinstance(t, MarathonTask) else MarathonTask().from_json(t)
            for t in (tasks or [])
        ]
        self.tasks_running = tasks_running
        self.tasks_staged = tasks_staged
        self.tasks_healthy = tasks_healthy
        self.task_kill_grace_period_seconds = task_kill_grace_period_seconds
        self.tasks_unhealthy = tasks_unhealthy
        self.upgrade_strategy = upgrade_strategy if (isinstance(upgrade_strategy, MarathonUpgradeStrategy) or upgrade_strategy is None) \
            else MarathonUpgradeStrategy.from_json(upgrade_strategy)
        self.unreachable_strategy = unreachable_strategy \
            if (isinstance(unreachable_strategy, MarathonUnreachableStrategy)
                or unreachable_strategy is None) \
            else MarathonUnreachableStrategy.from_json(unreachable_strategy)
        self.uris = uris or []
        self.fetch = fetch or []
        self.user = user
        self.version = version
        self.version_info = version_info if (isinstance(version_info, MarathonAppVersionInfo) or version_info is None) \
            else MarathonAppVersionInfo.from_json(version_info)
        self.task_stats = task_stats if (isinstance(task_stats, MarathonTaskStats) or task_stats is None) \
            else MarathonTaskStats.from_json(task_stats)
        self.networks = networks

    def add_env(self, key, value):
        self.env[key] = value


class MarathonHealthCheck(MarathonObject):

    """Marathon health check.

    See https://mesosphere.github.io/marathon/docs/health-checks.html

    :param str command: health check command (if protocol == 'COMMAND')
    :param int grace_period_seconds: how long to ignore health check failures on initial task launch (before first healthy status)
    :param int interval_seconds: how long to wait between health checks
    :param int max_consecutive_failures: max number of consecutive failures before the task should be killed
    :param str path: health check target path (if protocol == 'HTTP')
    :param int port_index: target port as indexed in app's `ports` array
    :param str protocol: health check protocol ('HTTP', 'TCP', or 'COMMAND')
    :param int timeout_seconds: how long before a waiting health check is considered failed
    :param bool ignore_http1xx: Ignore HTTP informational status codes 100 to 199.
    :param dict kwargs: additional arguments for forward compatibility
    """

    def __init__(self, command=None, grace_period_seconds=None, interval_seconds=None, max_consecutive_failures=None,
                 path=None, port_index=None, protocol=None, timeout_seconds=None, ignore_http1xx=None, **kwargs):

        if command is None:
            self.command = None
        elif isinstance(command, str):
            self.command = {
                "value": command
            }
        elif type(command) is dict and 'value' in command:
            log.warn('Deprecated: Using command as dict instead of string is deprecated')
            self.command = {
                "value": command['value']
            }
        else:
            raise ValueError(f'Invalid command format: {command}')

        self.grace_period_seconds = grace_period_seconds
        self.interval_seconds = interval_seconds
        self.max_consecutive_failures = max_consecutive_failures
        self.path = path
        self.port_index = port_index
        self.protocol = protocol
        self.timeout_seconds = timeout_seconds
        self.ignore_http1xx = ignore_http1xx
        # additional not previously known healthcheck attributes
        for k, v in kwargs.items():
            setattr(self, k, v)


class MarathonTaskFailure(MarathonObject):

    """Marathon Task Failure.

    :param str app_id: application id
    :param str host: mesos slave running the task
    :param str message: error message
    :param str task_id: task id
    :param str instance_id: instance id
    :param str state: task state
    :param timestamp: when this task failed
    :type timestamp: datetime or str
    :param str version: app version with which this task was started
    """

    def __init__(self, app_id=None, host=None, message=None, task_id=None, instance_id=None,
                 slave_id=None, state=None, timestamp=None, version=None):
        self.app_id = app_id
        self.host = host
        self.message = message
        self.task_id = task_id
        self.instance_id = instance_id
        self.slave_id = slave_id
        self.state = state
        self.timestamp = to_datetime(timestamp)
        self.version = version


class MarathonUpgradeStrategy(MarathonObject):

    """Marathon health check.

    See https://mesosphere.github.io/marathon/docs/health-checks.html

    :param float minimum_health_capacity: minimum % of instances kept healthy on deploy
    """

    def __init__(self, maximum_over_capacity=None,
                 minimum_health_capacity=None):
        self.maximum_over_capacity = maximum_over_capacity
        self.minimum_health_capacity = minimum_health_capacity


class MarathonUnreachableStrategy(MarathonObject):

    """Marathon unreachable Strategy.

    Define handling for unreachable instances. Given
    `unreachable_inactive_after_seconds = 60` and
    `unreachable_expunge_after = 120`, an instance will be expunged if it has
    been unreachable for more than 120 seconds or a second instance is started
    if it has been unreachable for more than 60 seconds.",

    See https://mesosphere.github.io/marathon/docs/?

    :param int unreachable_inactive_after_seconds: time an instance is
        unreachable for in seconds before marked as inactive.
    :param int unreachable_expunge_after_seconds: time an instance is
        unreachable for in seconds before expunged.
    :param int inactive_after_seconds
    :param int expunge_after_seconds
    """
    DISABLED = 'disabled'

    def __init__(self, unreachable_inactive_after_seconds=None,
                 unreachable_expunge_after_seconds=None,
                 inactive_after_seconds=None, expunge_after_seconds=None):
        self.unreachable_inactive_after_seconds = unreachable_inactive_after_seconds
        self.unreachable_expunge_after_seconds = unreachable_expunge_after_seconds
        self.inactive_after_seconds = inactive_after_seconds
        self.expunge_after_seconds = expunge_after_seconds

    @classmethod
    def from_json(cls, attributes):
        if attributes == cls.DISABLED:
            return cls.DISABLED
        return super().from_json(attributes)


class MarathonAppVersionInfo(MarathonObject):

    """Marathon App version info.

    See release notes for Marathon v0.11.0
    https://github.com/mesosphere/marathon/releases/tag/v0.11.0

    :param str app_id: application id
    :param str host: mesos slave running the task
    """

    def __init__(self, last_scaling_at=None, last_config_change_at=None):
        self.last_scaling_at = to_datetime(last_scaling_at)
        self.last_config_change_at = to_datetime(last_config_change_at)


class MarathonTaskStats(MarathonObject):

    """Marathon task statistics

    See https://mesosphere.github.io/marathon/docs/rest-api.html#taskstats-object-v0-11

    :param started_after_last_scaling: contains statistics about all tasks that were started after the last scaling or restart operation.
    :type started_after_last_scaling: :class:`marathon.models.app.MarathonTaskStatsType` or dict
    :param with_latest_config: contains statistics about all tasks that run with the same config as the latest app version.
    :type with_latest_config: :class:`marathon.models.app.MarathonTaskStatsType` or dict
    :param with_outdated_config: contains statistics about all tasks that were started before the last config change
           which was not simply a restart or scaling operation.
    :type with_outdated_config: :class:`marathon.models.app.MarathonTaskStatsType` or dict
    :param total_summary: contains statistics about all tasks.
    :type total_summary: :class:`marathon.models.app.MarathonTaskStatsType` or dict
    """

    def __init__(self, started_after_last_scaling=None,
                 with_latest_config=None, with_outdated_config=None, total_summary=None):
        self.started_after_last_scaling = started_after_last_scaling if \
            (isinstance(started_after_last_scaling, MarathonTaskStatsType) or started_after_last_scaling is None) \
            else MarathonTaskStatsType.from_json(started_after_last_scaling)
        self.with_latest_config = with_latest_config if \
            (isinstance(with_latest_config, MarathonTaskStatsType) or with_latest_config is None) \
            else MarathonTaskStatsType.from_json(with_latest_config)
        self.with_outdated_config = with_outdated_config if \
            (isinstance(with_outdated_config, MarathonTaskStatsType) or with_outdated_config is None) \
            else MarathonTaskStatsType.from_json(with_outdated_config)
        self.total_summary = total_summary if \
            (isinstance(total_summary, MarathonTaskStatsType) or total_summary is None) \
            else MarathonTaskStatsType.from_json(total_summary)


class MarathonTaskStatsType(MarathonObject):

    """Marathon app task stats

    :param stats: stast about app tasks
    :type stats: :class:`marathon.models.app.MarathonTaskStatsStats` or dict
    """

    def __init__(self, stats=None):
        self.stats = stats if (isinstance(stats, MarathonTaskStatsStats) or stats is None)\
            else MarathonTaskStatsStats.from_json(stats)


class MarathonTaskStatsStats(MarathonObject):

    """Marathon app task stats

    :param counts: app task count breakdown
    :type counts: :class:`marathon.models.app.MarathonTaskStatsCounts` or dict
    :param life_time: app task life time stats
    :type life_time: :class:`marathon.models.app.MarathonTaskStatsLifeTime` or dict
    """

    def __init__(self, counts=None, life_time=None):
        self.counts = counts if (isinstance(counts, MarathonTaskStatsCounts) or counts is None)\
            else MarathonTaskStatsCounts.from_json(counts)
        self.life_time = life_time if (isinstance(life_time, MarathonTaskStatsLifeTime) or life_time is None)\
            else MarathonTaskStatsLifeTime.from_json(life_time)


class MarathonTaskStatsCounts(MarathonObject):

    """Marathon app task counts

    Equivalent to tasksStaged, tasksRunning, tasksHealthy, tasksUnhealthy.

    :param int staged: Staged task count
    :param int running: Running task count
    :param int healthy: Healthy task count
    :param int unhealthy: unhealthy task count
    """

    def __init__(self, staged=None,
                 running=None, healthy=None, unhealthy=None):
        self.staged = staged
        self.running = running
        self.healthy = healthy
        self.unhealthy = unhealthy


class MarathonTaskStatsLifeTime(MarathonObject):

    """Marathon app life time statistics

    Measured from `"startedAt"` (timestamp of the Mesos TASK_RUNNING status update) of each running task until now

    :param float average_seconds: Average seconds
    :param float median_seconds: Median seconds
    """

    def __init__(self, average_seconds=None, median_seconds=None):
        self.average_seconds = average_seconds
        self.median_seconds = median_seconds


class ReadinessCheck(MarathonObject):
    """Marathon readiness check: https://mesosphere.github.io/marathon/docs/readiness-checks.html

    :param string name (Optional. Default: "readinessCheck"): The name used to identify this readiness check.
    :param string protocol (Optional. Default: "HTTP"): Protocol of the requests to be performed. Either HTTP or HTTPS.
    :param string path (Optional. Default: "/"): Path to the endpoint the task exposes to provide readiness status.
           Example: /path/to/readiness.
    :param string port_name (Optional. Default: "http-api"): Name of the port to query as described in the
           portDefinitions. Example: http-api.
    :param int interval_seconds (Optional. Default: 30 seconds): Number of seconds to wait between readiness checks.
    :param int timeout_seconds (Optional. Default: 10 seconds): Number of seconds after which a readiness check
           times out, regardless of the response. This value must be smaller than interval_seconds.
    :param list http_status_codes_for_ready (Optional. Default: [200]): The HTTP/HTTPS status code to treat as ready.
    :param bool preserve_last_response (Optional. Default: false): If true, the last readiness check response will be
           preserved and exposed in the API as part of a deployment.

    """

    def __init__(self, name=None, protocol=None, path=None, port_name=None, interval_seconds=None,
                 http_status_codes_for_ready=None, preserve_last_response=None, timeout_seconds=None):
        self.name = name
        self.protocol = protocol
        self.path = path
        self.port_name = port_name
        self.interval_seconds = interval_seconds
        self.http_status_codes_for_ready = http_status_codes_for_ready
        self.preserve_last_response = preserve_last_response
        self.timeout_seconds = timeout_seconds


class PortDefinition(MarathonObject):
    """Marathon port definitions: https://mesosphere.github.io/marathon/docs/ports.html

    :param int port: The port
    :param string protocol: tcp or udp
    :param string name: (optional) the name of the port
    :param dict labels: undocumented
    """

    def __init__(self, port=None, protocol=None, name=None, labels=None):
        self.port = port
        self.protocol = protocol
        self.name = name
        self.labels = labels


class Residency(MarathonObject):
    """Declares how "resident" an app is: https://mesosphere.github.io/marathon/docs/persistent-volumes.html

    :param int relaunch_escalation_timeout_seconds: How long marathon will try to relaunch where the volumes is, defaults to 3600
    :param string task_lost_behavior: What to do after a TASK_LOST. See the official Marathon docs for options

    """

    def __init__(self, relaunch_escalation_timeout_seconds=None, task_lost_behavior=None):
        self.relaunch_escalation_timeout_seconds = relaunch_escalation_timeout_seconds
        self.task_lost_behavior = task_lost_behavior


class Secret(MarathonObject):
    """Declares marathon secret object.
    :param str source: The source of the secret's value. The format depends on the secret store used by Mesos.

    """

    def __init__(self, source=None):
        self.source = source
