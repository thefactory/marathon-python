import sys
import time

import marathon
from behave import given, when, then
import mock

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


@when(u'we create a trivial new app')
def create_trivial_new_app(context):
    context.client.create_app('myapp3', marathon.MarathonApp(cmd='sleep 100', mem=16, cpus=1))


@then(u'we should see it running via the marathon api')
def see_it_running(context):
    print(context.client.list_apps())
    assert context.client.get_app('myapp3')

