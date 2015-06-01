__author__ = 'kevinschoon@gmail.com'

import random
import uuid

from marathon.models.app import MarathonApp, MarathonHealthCheck
from marathon.models.container import MarathonContainer

MARATHON_SERVER = 'http://ubuntu:8080'
MARATHON_CALLBACK_URL = 'http://192.168.99.1:9999'
TIMESTAMP = '2015-05-29T23:05:37.715Z'
SERVICE_PORT_RANGE = range(10000, 11000)

HEALTH_CHECK_ARGS = {
    'protocol': 'HTTP',
    'portIndex': 0,
    'path': '/',
    'gracePeriodSeconds': 5,
    'intervalSeconds': 20,
    'maxConsecutiveFailures': 3
}


def get_app():
    service_port = random.choice([x for x in SERVICE_PORT_RANGE])
    container_args = {
        'type': 'DOCKER',
        'docker': {
            'image': 'python:3.4.3',
            'network': 'BRIDGE',
            'portMappings': [
                {
                    'containerPort': 8000,
                    'servicePort': service_port,
                    'protocol': 'tcp'
                }
            ]

        }
    }

    args = {
        'id': './marathon-integration-test-{}-8000-{}'.format(str(uuid.uuid4()), service_port),
        'instances': 1,
        'cpus': 0.1,
        'mem': 64.0,
        'args': ['python', '-m', 'http.server', '8000'],
        'container': MarathonContainer.from_json(container_args),
        'health_checks': [MarathonHealthCheck.from_json(HEALTH_CHECK_ARGS)]
    }

    return MarathonApp(**args)
