# encoding: utf-8

from marathon.models.events import EventFactory, MarathonStatusUpdateEvent
from marathon.models.task import MarathonIpAddress
import unittest


class MarathonEventTest(unittest.TestCase):

    def test_event_factory(self):
        self.assertEqual(
            set(EventFactory.event_to_class.keys()),
            set(EventFactory.class_to_event.values()),
        )

    def test_marathon_event(self):
        """Test that we can process at least one kind of event."""
        payload = {
            "eventType": "status_update_event",
            "slaveId": "slave-01",
            "taskId": "task-01",
            "taskStatus": "TASK_RUNNING",
            "message": "Some message",
            "appId": "/foo/bar",
            "host": "host-01",
            "ipAddresses": [
                {"ip_address": "127.0.0.1", "protocol": "tcp"},
                {"ip_address": "127.0.0.1", "protocol": "udp"},
            ],
            "ports": [0, 1],
            "version": "1234",
            "timestamp": 12345,
        }
        factory = EventFactory()
        event = factory.process(payload)

        expected_event = MarathonStatusUpdateEvent(
            event_type="status_update_event",
            timestamp=12345,
            slave_id="slave-01",
            task_id="task-01",
            task_status="TASK_RUNNING",
            message="Some message",
            app_id="/foo/bar",
            host="host-01",
            ports=[0, 1],
            version="1234",
        )
        expected_event.ip_addresses = [
            MarathonIpAddress(ip_address="127.0.0.1", protocol="tcp"),
            MarathonIpAddress(ip_address="127.0.0.1", protocol="udp"),
        ]

        self.assertEqual(event.to_json(), expected_event.to_json())
