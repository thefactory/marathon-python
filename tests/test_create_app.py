__author__ = 'kevinschoon@gmail.com'

import unittest
import time

from marathon import MarathonClient
from marathon.models.app import MarathonApp, MarathonTask, MarathonHealthCheck, MarathonUpgradeStrategy
from tests.config import get_app, MARATHON_SERVER


class TestCreateApp(unittest.TestCase):
    """
    Test the creation of a Marathon app against a live endpoint. Configure MARATHON_SERVER in tests.config.
    """

    def setUp(self):
        self._app = get_app()  # Generate a random server configuration.
        self.client = MarathonClient(MARATHON_SERVER)
        self.client.create_app(app_id=self._app.id, app=self._app)
        time.sleep(2)  # Wait two seconds for the POST to be processed by Marathon.
        self.app = self.client.get_app(self._app.id)
        while not self.app.tasks_healthy:  # Wait until the app becomes healthy.
            self.app = self.client.get_app(self._app.id)
            time.sleep(1)

    def test_create(self):
        self.assertIsInstance(self.app, MarathonApp)
        self.assertIsInstance(self.app.upgrade_strategy, MarathonUpgradeStrategy)
        self.assertIsInstance(self.app.tasks.pop(), MarathonTask)
        self.assertIsInstance(self.app.health_checks.pop(), MarathonHealthCheck)

    def tearDown(self):
        self.client.delete_app(self.app.id, force=True)

