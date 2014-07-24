import time
import itertools

try:
    import json
except ImportError:
    import simplejson as json
try:
    from urllib2 import HTTPError
except ImportError:
    from urllib.error import HTTPError

import requests

import marathon
from .models import MarathonApp, MarathonTask, MarathonEndpoint
from .exceptions import NotFoundError


class MarathonClient(object):
    """Client interface for the Marathon REST API."""

    def __init__(self, base_url, username=None, password=None):
        self.base_url = base_url.rstrip('/')
        self.auth = (username, password) if username and password else None

    def __repr__(self):
        return "Connection:%s" % self.base_url

    def _parse_response(self, response, clazz, is_list=False):
        """Parse a Marathon response into an object or list of objects."""
        resource_name = None
        if clazz is MarathonApp:
            resource_name = 'apps' if is_list else 'app'
        elif clazz is MarathonTask:
            resource_name = 'tasks' if is_list else 'task'

        if not resource_name:
            return

        if is_list:
            return [clazz.json_decode(resource) for resource in response.json()[resource_name]]
        else:
            return clazz.json_decode(response.json()[resource_name])

    def _do_request(self, method, path, params=None, data=None):
        """Query Marathon server."""
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        url = "".join([self.base_url, path])
        try:
            response = requests.request(method, url, params=params, data=data, headers=headers, auth=self.auth)

            if response.status_code >= 300:
                marathon.log.warn("Got HTTP {code}: {body}".format(code=response.status_code, body=response.text))
            else:
                marathon.log.debug("Got HTTP {code}: {body}".format(code=response.status_code, body=response.text))

            return response
        except Exception as e:
            print e

    def list_endpoints(self):
        """List the current endpoints for all applications

        :returns: list of endpoints
        :rtype: list[`MarathonEndpoint`]
        """
        response = self._do_request("GET", "/v1/endpoints")
        endpoints = [MarathonEndpoint.json_decode(app) for app in response.json()]
        # Flatten result
        return [item for sublist in endpoints for item in sublist]

    def create_app(self, **kwargs):
        """Create and start an app.

        :param kwargs: application properties

        :returns: success
        :rtype: bool
        """
        data = json.dumps(kwargs)
        response = self._do_request("POST", "/v2/apps", data=data)
        return True if response.status_code is 201 else False

    def list_apps(self, cmd=None, **kwargs):
        """List all apps, optionally filtered by `cmd`.

        :param str app_id: application ID
        :param str cmd: if passed, only show apps with a matching `cmd`
        :param kwargs: arbitrary search filters

        :returns: list of applications
        :rtype: list[:class:`marathon.models.app.MarathonApp`]
        """
        params = {'cmd': cmd} if cmd else {}
        response = self._do_request("GET", "/v2/apps", params=params)
        apps = self._parse_response(response, MarathonApp, is_list=True)
        for k,v in kwargs.iteritems():
            apps = filter(lambda o: getattr(o, k) == v, apps)
        return apps

    def get_app(self, app_id):
        """Get a single app.

        :param str app_id: application ID

        :returns: application
        :rtype: :class:`marathon.models.app.MarathonApp`
        """
        response = self._do_request("GET", "/v2/apps/{app_id}".format(app_id=app_id))
        return self._parse_response(response, MarathonApp)

    def update_app(self, app_id=None, app=None, **kwargs):
        """Update an app.

        If `app` is passed, use this as a base on which `kwargs` are overlaid. The resulting configuration
        is pushed to Marathon.

        Note: this method can not be used to rename apps.

        :param str app_id: application ID
        :param app: [optional] an app instance
        :type app: :class:`marathon.models.app.MarathonApp`
        :param kwargs: application properties

        :returns: success
        :rtype: bool
        """
        if app:
            updated_app = MarathonApp(**app.__dict__)
            for key, value in kwargs.iteritems():
                setattr(updated_app, key, value)
        else:
            updated_app = MarathonApp(**kwargs)

        data = json.dumps(updated_app.json_encode())
        response = self._do_request("PUT", "/v2/apps/{app_id}".format(app_id=app_id), data=data)
        return True if response.status_code is 204 else False

    def delete_app(self, app_id):
        """Stop and destroy an app.

        :param str app_id: application ID

        :returns: success
        :rtype: bool
        """
        response = self._do_request("DELETE", "/v2/apps/{app_id}".format(app_id=app_id))
        return True if response.status_code is 204 else False

    def scale_app(self, app_id, instances=None, delta=None):
        """Scale an app.

        Scale an app to a target number of instances (with `instances`), or scale the number of
        instances up or down by some delta (`delta`). If the resulting number of instances would be negative,
        desired instances will be set to zero.

        If both `instances` and `delta` are passed, use `instances`.

        :param str app_id: application ID
        :param int instances: [optional] the number of instances to scale to
        :param int delta: [optional] the number of instances to scale up or down by

        :returns: success
        :rtype: bool
        """
        if instances is None and delta is None:
            marathon.log.error("instances or delta must be passed")
            return

        try:
            app = self.get_app(app_id)
        except NotFoundError:
            marathon.log.error("App '{app}' not found".format(app=app_id))
            return

        new_instances = instances if instances is not None else (app.instances + delta)
        return self.update_app(app_id, app=app, instances=new_instances)

    def list_tasks(self, app_id=None, **kwargs):
        """List running tasks, optionally filtered by app_id.

        :param str app_id: if passed, only show tasks for this application
        :param kwargs: arbitrary search filters

        :returns: list of tasks
        :rtype: list[:class:`marathon.models.task.MarathonTask`]
        """
        if app_id:
            response = self._do_request("GET", "/v2/apps/{app_id}/tasks".format(app_id=app_id))
        else:
            response = self._do_request("GET", "/v2/tasks")

        tasks = self._parse_response(response, MarathonTask, is_list=True)
        for k,v in kwargs.iteritems():
            tasks = filter(lambda o: getattr(o, k) == v, tasks)
        return tasks

    def kill_tasks(self, app_id, scale=False, host=None, batch_size=0, batch_delay=0):
        """Kill all tasks belonging to app.

        :param str app_id: application ID
        :param bool scale: if true, scale down the app by the number of tasks killed
        :param str host: if provided, only terminate tasks on this Mesos slave
        :param int batch_size: if non-zero, terminate tasks in groups of this size
        :param int batch_delay: time (in seconds) to wait in between batched kills

        :returns: list of killed tasks
        :rtype: list[:class:`marathon.models.task.MarathonTask`]
        """
        def batch(iterable, size):
            sourceiter = iter(iterable)
            while True:
                batchiter = itertools.islice(sourceiter, size)
                yield itertools.chain([batchiter.next()], batchiter)

        if batch_size == 0:
            # Terminate all at once
            params = {'scale': scale}
            if host: params['host'] = host
            response = self._do_request("DELETE", "/v2/apps/{app_id}/tasks".format(app_id=app_id), params)
            return self._parse_response(response, MarathonTask, is_list=True)
        else:
            # Terminate in batches
            tasks = self.list_tasks(app_id, host=host) if host else self.list_tasks(app_id)
            for tbatch in batch(tasks, batch_size):
                [self.kill_task(app_id, t.id, scale=scale) for t in tbatch]
                time.sleep(batch_delay)

            return tasks

    def kill_task(self, app_id, task_id, scale=False):
        """Kill a task.

        :param str app_id: application ID
        :param bool scale: if true, scale down the app by one if the task exists

        :returns: the killed task
        :rtype: :class:`marathon.models.task.MarathonTask`
        """
        params = {'scale': scale}
        response = self._do_request("DELETE", "/v2/apps/{app_id}/tasks/{task_id}"
                                    .format(app_id=app_id, task_id=task_id), params)
        return self._parse_response(response, MarathonTask)

    def list_versions(self, app_id):
        """List the versions of an app.

        :param str app_id: application ID

        :returns: list of versions
        :rtype: list[str]
        """
        response = self._do_request("GET", "/v2/apps/{app_id}/versions".format(app_id=app_id))
        return [version for version in response.json()['versions']]

    def get_version(self, app_id, version):
        """Get the configuration of an app at a specific version.

        :param str app_id: application ID
        :param str version: application version

        :return: application configuration
        :rtype: :class:`marathon.models.app.MarathonApp`
        """
        response = self._do_request("GET", "/v2/apps/{app_id}/versions/{version}"
                                    .format(app_id=app_id, version=version))
        return MarathonApp(response.json())

    def list_event_subscriptions(self):
        """List the event subscriber callback URLs.

        :returns: list of callback URLs
        :rtype: list[str]
        """
        response = self._do_request("GET", "/v2/eventSubscriptions")
        return [url for url in response.json()['callbackUrls']]

    def create_event_subscription(self, url):
        """Register a callback URL as an event subscriber.

        :param str url: callback URL

        :returns: the created event subscription
        :rtype: dict
        """
        params = {"callbackUrl": url}
        response = self._do_request("POST", "/v2/eventSubscriptions", params)
        return response.json()

    def delete_event_subscription(self, url):
        """Deregister a callback URL as an event subscriber.

        :param str url: callback URL

        :returns: the deleted event subscription
        :rtype: dict
        """
        params = {"callbackUrl": url}
        response = self._do_request("DELETE", "/v2/eventSubscriptions", params)
        return response.json()