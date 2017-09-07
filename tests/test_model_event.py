# encoding: utf-8

from marathon.models.events import EventFactory
import unittest


class MarathonEventTest(unittest.TestCase):

    def test_event_factory(self):
        self.assertEqual(set(EventFactory.event_to_class.keys()), set(EventFactory.class_to_event.values()))
