try:
    import json
except ImportError:
    import simplejson as json

from .base import MarathonResource
from .constraint import MarathonConstraint
from .task import MarathonTask


class MarathonApp(MarathonResource):
    """Marathon Application resource.

    :param str cmd: cmd
    :param constraints: placement constraints
    :type constraints: list[:class:`marathon.models.constraint.MarathonConstraint`] or list[tuple]
    :param dict container: container
    :param float cpus: cpus required per instance
    :param dict env: env vars
    :param str executor: executor
    :param str id: app id
    :param int instances: instances
    :param float mem: memory (in MB) required per instance
    :param list[int] ports: ports
    :param list[str] uris: uris
    """

    UPDATE_OK_ATTRIBUTES = ['cmd', 'constraints', 'container', 'cpus', 'env', 'executor', 'mem', 'ports', 'uris']
    """List of attributes which may be updated/changed after app creation"""

    CREATE_ONLY_ATTRIBUTES = ['id']
    """List of attributes that should only be passed on creation"""

    READ_ONLY_ATTRIBUTES = []
    """List of read-only attributes"""

    def __init__(self, cmd=None, constraints=None, container=None, cpus=None, env=None, executor=None,
                 health_checks=None, id=None, instances=None, mem=None, ports=None, tasks=None, uris=None):
        self.cmd = cmd
        self.constraints = constraints or []
        self.container = container
        self.cpus = cpus
        self.env = env
        self.executor = executor
        self.health_checks = health_checks or []
        self.id = id
        self.instances = instances
        self.mem = mem
        self.ports = ports or []
        self.tasks = tasks or []
        self.uris = uris

    @classmethod
    def json_decode(cls, obj):
        """Construct a MarathonApp from a parsed response.

        :param dict attributes: object attributes from parsed response

        :rtype: :class:`MarathonApp`
        """
        return cls(
            cmd=obj.get('cmd'),
            constraints=[MarathonConstraint.json_decode(c) for c in obj.get('constraints', [])],
            container=obj.get('container'),
            cpus=obj.get('cpus'),
            env=obj.get('env'),
            executor=obj.get('executor'),
            health_checks=obj.get('healthChecks'),
            id=obj.get('id'),
            instances=obj.get('instances'),
            mem=obj.get('mem'),
            ports=obj.get('ports'),
            tasks=[MarathonTask.json_decode(t) for t in obj.get('tasks', [])],
            uris=obj.get('uris')
        )

    def json_encode(self):
        """Construct a JSON-friendly representation of the object.

        :rtype: dict
        """
        return {
            'cmd': self.cmd,
            'constraints': [c.json_encode() for c in self.constraints],
            'container': self.container,
            'cpus': self.cpus,
            'env': self.env,
            'executor': self.executor,
            'healthChecks': self.health_checks,
            'id': self.id,
            'instances': self.instances,
            'mem': self.mem,
            'ports': self.ports,
            'tasks': [t.json_encode() for t in self.tasks],
            'uris': self.uris
        }