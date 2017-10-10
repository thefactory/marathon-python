# encoding: utf-8

from marathon.models.app import MarathonApp, MarathonAppVersionInfo
from datetime import datetime
import unittest


class MarathonAppTest(unittest.TestCase):

    def test_env_defaults_to_empty_dict(self):
        """
        é testé
        """
        app = MarathonApp()
        self.assertEquals(app.env, {})

    def test_add_env_empty_dict(self):
        app = MarathonApp()
        app.add_env("MY_ENV", "my-value")
        self.assertDictEqual({"MY_ENV": "my-value"}, app.env)

    def test_add_env_non_empty_dict(self):
        env_data = {"OTHER_ENV": "other-value"}
        app = MarathonApp(env=env_data)

        app.add_env("MY_ENV", "my-value")
        self.assertDictEqual({"MY_ENV": "my-value", "OTHER_ENV": "other-value"}, app.env)

    def test_version_info_datetime(self):
        app_ver_info = MarathonAppVersionInfo()
        self.assertEquals(app_ver_info._to_datetime("2017-09-28T00:31:55Z"), datetime(2017, 9, 28, 0, 31, 55))
        self.assertEquals(app_ver_info._to_datetime("2017-09-28T00:31:55.4Z"), datetime(2017, 9, 28, 0, 31, 55, 400000))
        self.assertEquals(app_ver_info._to_datetime("2017-09-28T00:31:55.004Z"), datetime(2017, 9, 28, 0, 31, 55, 4000))
        self.assertEquals(app_ver_info._to_datetime("2017-09-28T00:31:55.00042Z"), datetime(2017, 9, 28, 0, 31, 55, 420))
