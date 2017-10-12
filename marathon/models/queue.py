from .base import MarathonResource
from .app import MarathonApp


class MarathonQueueItem(MarathonResource):

    """Marathon queue item.

    See: https://mesosphere.github.io/marathon/docs/rest-api.html#queue

    List all the tasks queued up or waiting to be scheduled. This is mainly
    used for troubleshooting and occurs when scaling changes are requested and the
    volume of scaling changes out paces the ability to schedule those tasks. In
    addition to the application in the queue, you see also the task count that
    needs to be started.

    If the task has a rate limit, then a delay to the start gets applied. You
    can see this delay for every application with the seconds to wait before
    the next launch will be tried.

    :param app:
    :type app: :class:`marathon.models.app.MarathonApp` or dict
    :param delay: queue item delay
    :type delay: :class:`marathon.models.app.MarathonQueueItemDelay` or dict
    :param bool overdue:
    """

    def __init__(self, app=None, overdue=None, count=None, delay=None, since=None,
                 processed_offers_summary=None, last_unused_offers=None):
        self.app = app if isinstance(
            app, MarathonApp) else MarathonApp().from_json(app)
        self.overdue = overdue
        self.count = count
        self.delay = delay if isinstance(
            delay, MarathonQueueItemDelay) else MarathonQueueItemDelay().from_json(delay)
        self.since = since
        self.processed_offers_summary = processed_offers_summary
        self.last_unused_offers = last_unused_offers


class MarathonQueueItemDelay(MarathonResource):

    """Marathon queue item delay.

    :param int time_left_seconds: Seconds to wait before the next launch will be tried.
    :param bool overdue: Is the queue item overdue.
    """

    def __init__(self, time_left_seconds=None, overdue=None):
        self.time_left_seconds = time_left_seconds
        self.overdue = overdue
