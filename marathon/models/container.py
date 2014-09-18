from ..exceptions import InvalidContainerTypeError
from .base import MarathonObject


class MarathonContainer(MarathonObject):
    """Marathon health check.

    See https://mesosphere.github.io/marathon/docs/native-docker.html

    :param docker: docker field (e.g., {"image": "mygroup/myimage"})'
    :type docker: :class:`marathon.models.container.MarathonDockerContainer` or dict
    :param str type:
    :param volumes:
    :type volumes: list[:class:`marathon.models.container.MarathonContainerVolume`] or list[dict]
    """

    TYPES = ['DOCKER']
    """Valid container types"""

    def __init__(self, docker=None, type=None, volumes=None):
        if not type in self.TYPES:
            raise InvalidContainerTypeError(type)
        self.type = type
        self.docker = docker if isinstance(docker, MarathonDockerContainer) \
            else MarathonDockerContainer().from_json(docker)
        self.volumes = [
            v if isinstance(v, MarathonContainerVolume) else MarathonContainerVolume().from_json(v)
            for v in (volumes or [])
        ]


class MarathonDockerContainer(MarathonObject):
    """Docker options.

    See https://mesosphere.github.io/marathon/docs/native-docker.html

    :param str image: docker image
    """

    def __init__(self, image=None):
        self.image = image


class MarathonContainerVolume(MarathonObject):
    """Volume options.

    See https://mesosphere.github.io/marathon/docs/native-docker.html

    :param str container_path: container path
    :param str host_path: host path
    :param str mode: one of ['RO', 'RW']
    """

    def __init__(self, container_path=None, host_path=None, mode=None):
        self.container_path = container_path
        self.host_path = host_path
        self.mode = mode