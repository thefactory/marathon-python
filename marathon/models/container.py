from ..exceptions import InvalidChoiceError
from .base import MarathonObject


class MarathonContainer(MarathonObject):

    """Marathon health check.

    See https://mesosphere.github.io/marathon/docs/native-docker.html

    :param docker: docker field (e.g., {"image": "mygroup/myimage"})'
    :type docker: :class:`marathon.models.container.MarathonDockerContainer` or dict
    :param str type:
    :param port_mappings: New in Marathon v1.5. container.docker.port_mappings moved here.
    :type port_mappings: list[:class:`marathon.models.container.MarathonContainerPortMapping`] or list[dict]
    :param volumes:
    :type volumes: list[:class:`marathon.models.container.MarathonContainerVolume`] or list[dict]
    """

    TYPES = ['DOCKER', 'MESOS']
    """Valid container types"""

    def __init__(self, docker=None, type='DOCKER', port_mappings=None, volumes=None):
        if type not in self.TYPES:
            raise InvalidChoiceError('type', type, self.TYPES)
        self.type = type

        # Marathon v1.5 moved portMappings from within container.docker object directly
        # under the container object
        if port_mappings:
            self.port_mappings = [
                pm if isinstance(
                    pm, MarathonContainerPortMapping) else MarathonContainerPortMapping().from_json(pm)
                for pm in (port_mappings or [])
            ]

        if docker:
            self.docker = docker if isinstance(docker, MarathonDockerContainer) \
                else MarathonDockerContainer().from_json(docker)

        self.volumes = [
            v if isinstance(
                v, MarathonContainerVolume) else MarathonContainerVolume().from_json(v)
            for v in (volumes or [])
        ]


class MarathonDockerContainer(MarathonObject):

    """Docker options.

    See https://mesosphere.github.io/marathon/docs/native-docker.html

    :param str image: docker image
    :param str network:
    :param port_mappings:
    :type port_mappings: list[:class:`marathon.models.container.MarathonContainerPortMapping`] or list[dict]
    :param list[dict] parameters:
    :param bool privileged: run container in privileged mode
    :param bool force_pull_image: Force a docker pull before launching
    """

    NETWORK_MODES = ['BRIDGE', 'HOST', 'USER', 'NONE']
    """Valid network modes"""

    def __init__(self, image=None, network=None, port_mappings=None, parameters=None, privileged=None,
                 force_pull_image=None, **kwargs):
        self.image = image
        if network:
            if network not in self.NETWORK_MODES:
                raise InvalidChoiceError(
                    'network', network, self.NETWORK_MODES)
            self.network = network
        self.port_mappings = [
            pm if isinstance(
                pm, MarathonContainerPortMapping) else MarathonContainerPortMapping().from_json(pm)
            for pm in (port_mappings or [])
        ]
        self.parameters = parameters or []
        self.privileged = privileged or False
        self.force_pull_image = force_pull_image or False


class MarathonContainerPortMapping(MarathonObject):

    """Container port mapping.

    See https://mesosphere.github.io/marathon/docs/native-docker.html

    :param str name:
    :param int container_port:
    :param int host_port:
    :param str protocol:
    :param object labels:
    """

    PROTOCOLS = ['tcp', 'udp', 'udp,tcp']
    """Valid protocols"""

    def __init__(self, name=None, container_port=None, host_port=None, service_port=None, protocol='tcp', labels=None):
        self.name = name
        self.container_port = container_port
        self.host_port = host_port
        self.service_port = service_port
        if protocol not in self.PROTOCOLS:
            raise InvalidChoiceError('protocol', protocol, self.PROTOCOLS)
        self.protocol = protocol
        self.labels = labels


class MarathonContainerVolume(MarathonObject):

    """Volume options.

    See https://mesosphere.github.io/marathon/docs/native-docker.html

    :param str container_path: container path
    :param str host_path: host path
    :param str mode: one of ['RO', 'RW']
    :param object persistent: persistent volume options, should be of the form {'size': 1000}
    :param object external: external volume options
    """

    MODES = ['RO', 'RW']

    def __init__(self, container_path=None, host_path=None, mode='RW', persistent=None, external=None):
        self.container_path = container_path
        self.host_path = host_path
        if mode not in self.MODES:
            raise InvalidChoiceError('mode', mode, self.MODES)
        self.mode = mode
        self.persistent = persistent
        self.external = external
