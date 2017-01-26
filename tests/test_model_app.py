# encoding: utf-8

from marathon.models.app import MarathonApp
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
