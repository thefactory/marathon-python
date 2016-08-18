"""
This module is used to translate Events from Marathon's EventBus system.
See: https://mesosphere.github.io/marathon/docs/event-bus.html
"""

from marathon.models.base import MarathonObject
from marathon.models.app import MarathonHealthCheck
from marathon.models.deployment import MarathonDeploymentPlan
from marathon.exceptions import MarathonError


class MarathonEvent(MarathonObject):

    """
    The MarathonEvent base class handles the translation of Event objects sent by the
    Marathon server into library MarathonObjects.
    """

    KNOWN_ATTRIBUTES = []
    attribute_name_to_marathon_object = {  # Allows embedding of MarathonObjects inside events.
        'health_check': MarathonHealthCheck,
        'plan': MarathonDeploymentPlan
    }

    def __init__(self, event_type, timestamp, **kwargs):
        self.event_type = event_type  # All events have these two attributes
        self.timestamp = timestamp
        for attribute in self.KNOWN_ATTRIBUTES:
            self._set(attribute, kwargs.get(attribute))

    def _set(self, attribute_name, attribute):
        if not attribute:
            return
        if attribute_name in self.attribute_name_to_marathon_object:
            clazz = self.attribute_name_to_marathon_object[attribute_name]
            attribute = clazz.from_json(
                attribute)  # If this attribute already has a Marathon object instantiate it.
        setattr(self, attribute_name, attribute)


class MarathonApiPostEvent(MarathonEvent):
    KNOWN_ATTRIBUTES = ['client_ip', 'app_definition', 'uri']


class MarathonStatusUpdateEvent(MarathonEvent):
    KNOWN_ATTRIBUTES = [
        'slave_id', 'task_id', 'task_status', 'app_id', 'host', 'ports', 'version', 'message']


class MarathonFrameworkMessageEvent(MarathonEvent):
    KNOWN_ATTRIBUTES = ['slave_id', 'executor_id', 'message']


class MarathonSubscribeEvent(MarathonEvent):
    KNOWN_ATTRIBUTES = ['client_ip', 'callback_url']


class MarathonUnsubscribeEvent(MarathonEvent):
    KNOWN_ATTRIBUTES = ['client_ip', 'callback_url']


class MarathonAddHealthCheckEvent(MarathonEvent):
    KNOWN_ATTRIBUTES = ['app_id', 'health_check', 'version']


class MarathonRemoveHealthCheckEvent(MarathonEvent):
    KNOWN_ATTRIBUTES = ['app_id', 'health_check']


class MarathonFailedHealthCheckEvent(MarathonEvent):
    KNOWN_ATTRIBUTES = ['app_id', 'health_check', 'task_id']


class MarathonHealthStatusChangedEvent(MarathonEvent):
    KNOWN_ATTRIBUTES = ['app_id', 'health_check', 'task_id', 'alive']


class MarathonGroupChangeSuccess(MarathonEvent):
    KNOWN_ATTRIBUTES = ['group_id', 'version']


class MarathonGroupChangeFailed(MarathonEvent):
    KNOWN_ATTRIBUTES = ['group_id', 'version', 'reason']


class MarathonDeploymentSuccess(MarathonEvent):
    KNOWN_ATTRIBUTES = ['id']


class MarathonDeploymentFailed(MarathonEvent):
    KNOWN_ATTRIBUTES = ['id']


class MarathonDeploymentInfo(MarathonEvent):
    KNOWN_ATTRIBUTES = ['plan']


class MarathonDeploymentStepSuccess(MarathonEvent):
    KNOWN_ATTRIBUTES = ['plan']


class MarathonDeploymentStepFailure(MarathonEvent):
    KNOWN_ATTRIBUTES = ['plan']


class MarathonEventStreamAttached(MarathonEvent):
    KNOWN_ATTRIBUTES = ['remote_address']


class MarathonEventStreamDetached(MarathonEvent):
    KNOWN_ATTRIBUTES = ['remote_address']


class MarathonUnhealthyTaskKillEvent(MarathonEvent):
    KNOWN_ATTRIBUTES = ['app_id', 'task_id', 'version', 'reason']


class EventFactory:

    """
    Handle an event emitted from the Marathon EventBus
    See: https://mesosphere.github.io/marathon/docs/event-bus.html
    """

    def __init__(self):
        pass

    event_to_class = {
        'api_post_event': MarathonApiPostEvent,
        'status_update_event': MarathonStatusUpdateEvent,
        'framework_message_event': MarathonFrameworkMessageEvent,
        'subscribe_event': MarathonSubscribeEvent,
        'unsubscribe_event': MarathonUnsubscribeEvent,
        'add_health_check_event': MarathonAddHealthCheckEvent,
        'remove_health_check_event': MarathonRemoveHealthCheckEvent,
        'failed_health_check_event': MarathonFailedHealthCheckEvent,
        'health_status_changed_event': MarathonHealthStatusChangedEvent,
        'unhealthy_task_kill_event': MarathonUnhealthyTaskKillEvent,
        'group_change_success': MarathonGroupChangeSuccess,
        'group_change_failed': MarathonGroupChangeFailed,
        'deployment_success': MarathonDeploymentSuccess,
        'deployment_failed': MarathonDeploymentFailed,
        'deployment_info': MarathonDeploymentInfo,
        'deployment_step_success': MarathonDeploymentStepSuccess,
        'deployment_step_failure': MarathonDeploymentStepFailure,
        'event_stream_attached': MarathonEventStreamAttached,
        'event_stream_detached': MarathonEventStreamDetached,
    }

    def process(self, event):
        event_type = event['eventType']
        if event_type in self.event_to_class:
            clazz = self.event_to_class[event_type]
            return clazz.from_json(event)
        else:
            raise MarathonError('Unknown event_type: {}, data: {}'.format(event_type, event))
