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
from marathon.resources import MarathonApp, MarathonTask


class MarathonClient(object):
    """Client interface for the Marathon REST API"""

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
            return [clazz(resource) for resource in response.json()[resource_name]]
        else:
            return clazz(response.json()[resource_name])

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

    def create_app(self, **kwargs):
        """Create and start an app.

        :param kwargs: application properties

        :returns: success
        :rtype: bool
        """
        data = json.dumps(kwargs)
        response = self._do_request("POST", "/v2/apps", data=data)
        return True if response.status_code is 204 else False

    def list_apps(self, cmd=None):
        """List all apps, optionally filtered by `cmd`.

        :param str app_id: application ID
        :param str cmd: if passed, only show apps with a matching `cmd`

        :returns: list of applications
        :rtype: list[MarathonApp]
        """
        params = {'cmd': cmd} if cmd else {}
        response = self._do_request("GET", "/v2/apps", params=params)
        return self._parse_response(response, MarathonApp, is_list=True)

    def get_app(self, app_id):
        """Get a single app.

        :param str app_id: application ID

        :returns: application
        :rtype: MarathonApp
        """
        response = self._do_request("GET", "/v2/apps/{app_id}".format(app_id=app_id))
        return self._parse_response(response, MarathonApp)

    def update_app(self, app_id, **kwargs):
        """Update an app.

        :param str app_id: application ID
        :param kwargs: application properties

        :returns: success
        :rtype: bool
        """
        data = json.dumps(kwargs)
        response = self._do_request("POST", "/v2/apps/{app_id}".format(app_id=app_id), data=data)
        return True if response.status_code is 204 else False

    def destroy_app(self, app_id):
        """Stop and destroy an app.

        :param str app_id: application ID

        :returns: success
        :rtype: bool
        """
        response = self._do_request("DELETE", "/v2/apps/{app_id}".format(app_id=app_id))
        return True if response.status_code is 204 else False

    def list_tasks(self, app_id=None):
        """List running tasks, optionally filtered by app_id.

        :param str app_id: if passed, only show tasks for this application

        :returns: list of tasks
        :rtype: list[MarathonTask]
        """
        if app_id:
            response = self._do_request("GET", "/v2/apps/{app_id}/tasks".format(app_id=app_id))
        else:
            response = self._do_request("GET", "/v2/tasks")

        return self._parse_response(response, MarathonTask, is_list=True)

    def kill_tasks(self, app_id, scale=False, host=None):
        """Kill all tasks belonging to app.

        :param str app_id: application ID
        :param bool scale: if true, scale down the app by the number of tasks killed
        :param str host: if provided, only terminate tasks on this Mesos slave

        :returns: list of killed tasks
        :rtype: list[MarathonTask]
        """
        params = {'scale': scale}
        if host: params['host'] = host
        response = self._do_request("DELETE", "/v2/apps/{app_id}/tasks".format(app_id=app_id), params)
        return self._parse_response(response, MarathonTask, is_list=True)

    def kill_task(self, app_id, task_id, scale=False, host=None):
        """Kill a task.

        :param str app_id: application ID
        :param bool scale: if true, scale down the app by one if the task exists

        :returns: the killed task
        :rtype: MarathonTask
        """
        params = {'scale': scale}
        if host: params['host'] = host
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
        :rtype: MarathonApp
        """
        response = self._do_request("GET", "/v2/apps/{app_id}/versions/{version}"
                                    .format(app_id=app_id, version=version))
        return MarathonApp(response.json())