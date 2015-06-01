__author__ = 'kevinschoon@gmail.com'

import unittest

from multiprocessing import Process, Queue

from tests.server import EventListener
from tests.config import get_app, MARATHON_SERVER, MARATHON_CALLBACK_URL

from marathon.models.events import EventFactory, MarathonSubscribeEvent
from marathon.client import MarathonClient


def listen_for_events(queue):
    listener = EventListener(queue=queue)
    listener.get_requests()

class TestEventSubscription(unittest.TestCase):
    """
    This test will generate an event from Marathon's EventBus and then test the creation of a Marathon EventObject.
    It will spawn a separate server process for capturing Marathon Callbacks.
    """

    def setUp(self):
        self.app = get_app()
        self.factory = EventFactory()
        self.client = MarathonClient(servers=[MARATHON_SERVER])
        self.client.create_event_subscription(url=MARATHON_CALLBACK_URL)

    def test_event_factory(self):
        queue = Queue()  # Use a Multiprocess Queue for communication with subprocess.
        receive = Process(target=listen_for_events, args=[queue])
        receive.start()  # Start the server.
        self.client.create_event_subscription(url='192.0.2.1')  # Generate an event (subscribe_event).
        while True:
            o = self.factory.process(queue.get(timeout=120))  # Raise queueEmpty if the test exceeds 2 minutes.
            if isinstance(o, MarathonSubscribeEvent):
                print(o, dir(o), o.__dict__)
                self.assertEqual(o.event_type, 'subscribe_event')
                break
        receive.terminate()

    def tearDown(self):
        self.client.delete_event_subscription(url='192.0.2.1')
