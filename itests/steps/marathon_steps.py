import sys
import time

import marathon
from behave import given, when, then

from itest_utils import get_marathon_connection_string
sys.path.append('../')


@given('a working marathon instance')
def working_marathon(context):
    """Adds a working marathon client as context.client for the purposes of
    interacting with it in the test."""
    if not hasattr(context, 'client'):
        marathon_connection_string = "http://%s" % \
            get_marathon_connection_string()
        context.client = marathon.MarathonClient(marathon_connection_string)


@then(u'we get the marathon instance\'s info')
def get_marathon_info(context):
    assert context.client.get_info()


@when(u'we create a trivial new app')
def create_trivial_new_app(context):
    context.client.create_app('test-trivial-app', marathon.MarathonApp(cmd='sleep 3600', mem=16, cpus=1, instances=5))


@then(u'we should be able to kill the tasks')
def kill_a_task(context):
    time.sleep(5)
    app = context.client.get_app('test-trivial-app')
    tasks = app.tasks
    context.client.kill_task(app_id='test-trivial-app', task_id=tasks[0].id, scale=True)


@when(u'we create a complex new app')
def create_complex_new_app_with_unicode(context):
    app_config = {
        'container': {
            'type': 'DOCKER',
            'docker': {
                'portMappings': [{'protocol': 'tcp', 'containerPort': 8888, 'hostPort': 0}],
                'image': u'localhost/fake_docker_url',
                'network': 'BRIDGE',
                'parameters': [
                    {'key': 'add-host', 'value': 'google-public-dns-a.google.com:8.8.8.8'},
                ],
            },
            'volumes': [{'hostPath': u'/etc/stuff', 'containerPath': u'/etc/stuff', 'mode': 'RO'}],
        },
        'instances': 1,
        'mem': 30,
        'args': [],
        'backoff_factor': 2,
        'cpus': 0.25,
        'uris': ['file:///root/.dockercfg'],
        'backoff_seconds': 1,
        'constraints': None,
        'cmd': u'/bin/true',
        'health_checks': [
            {
                'protocol': 'HTTP',
                'path': '/health',
                'gracePeriodSeconds': 3,
                'intervalSeconds': 10,
                'portIndex': 0,
                'timeoutSeconds': 10,
                'maxConsecutiveFailures': 3
            },
        ],
    }
    context.client.create_app('test-complex-app', marathon.MarathonApp(**app_config))


@then(u'we should see the {which} app running via the marathon api')
def see_complext_app_running(context, which):
    print(context.client.list_apps())
    assert context.client.get_app('test-%s-app' % which)


@when(u'we wait the {which} app deployment finish')
def wait_deployment_finish(context, which):
    while True:
        time.sleep(1)
        app = context.client.get_app('test-%s-app' % which, embed_tasks=True)
        if not app.deployments:
            break


@then(u'we should be able to kill the #{to_kill} tasks of the {which} app')
def kill_tasks(context, to_kill, which):
    app_tasks = context.client.get_app('test-%s-app' % which, embed_tasks=True).tasks

    index_to_kill = eval("[" + to_kill + "]")
    task_to_kill = [app_tasks[index].id for index in index_to_kill]

    context.client.kill_given_tasks(task_to_kill)


@then(u'we should be able to list tasks of the {which} app')
def list_tasks(context, which):
    app = context.client.get_app('test-%s-app' % which)
    tasks = context.client.list_tasks('test-%s-app' % which)
    assert len(tasks) == app.instances
