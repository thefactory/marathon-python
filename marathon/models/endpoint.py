from .base import MarathonObject


class MarathonEndpoint(MarathonObject):

    """Marathon Endpoint helper object for service discovery. It describes a single port mapping for a running task.

    :param str app_id: application id
    :param str host: mesos slave running the task
    :param str task_id: task id
    :param int service_port: application service port
    :param int task_port: port allocated on the slave
    """

    def __repr__(self):
        return "{clazz}::{app_id}::{service_port}::{task_id}::{task_port}".format(
            clazz=self.__class__.__name__,
            app_id=self.app_id,
            service_port=self.service_port,
            task_id=self.task_id,
            task_port=self.task_port
        )

    def __init__(self, app_id=None, service_port=None,
                 host=None, task_id=None, task_port=None):
        self.app_id = app_id
        self.service_port = service_port
        self.host = host
        self.task_id = task_id
        self.task_port = task_port

    @classmethod
    def from_tasks(cls, tasks):
        """Construct a list of MarathonEndpoints from a list of tasks.

        :param list[:class:`marathon.models.MarathonTask`] tasks: list of tasks to parse

        :rtype: list[:class:`MarathonEndpoint`]
        """

        endpoints = [
            [
                MarathonEndpoint(task.app_id, task.service_ports[
                                 port_index], task.host, task.id, port)
                for port_index, port in enumerate(task.ports)
            ]
            for task in tasks
        ]
        # Flatten result
        return [item for sublist in endpoints for item in sublist]
