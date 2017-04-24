from .base import MarathonObject, MarathonResource


class MarathonDeployment(MarathonResource):

    """Marathon Application resource.

    See: https://mesosphere.github.io/marathon/docs/rest-api.html#deployments
         https://mesosphere.github.io/marathon/docs/generated/api.html#v2_deployments_get

    :param list[str] affected_apps: list of affected app ids
    :param current_actions: current actions
    :type current_actions: list[:class:`marathon.models.deployment.MarathonDeploymentAction`] or list[dict]
    :param int current_step: current step
    :param str id: deployment id
    :param steps: deployment steps
    :type steps: list[:class:`marathon.models.deployment.MarathonDeploymentAction`] or list[dict]
    :param int total_steps: total number of steps
    :param str version: version id
    :param str affected_pods: list of strings
    """

    def __init__(self, affected_apps=None, current_actions=None, current_step=None, id=None, steps=None,
                 total_steps=None, version=None, affected_pods=None):
        self.affected_apps = affected_apps
        self.current_actions = [
            a if isinstance(
                a, MarathonDeploymentAction) else MarathonDeploymentAction().from_json(a)
            for a in (current_actions or [])
        ]
        self.current_step = current_step
        self.id = id
        self.steps = [self.parse_deployment_step(step) for step in (steps or [])]
        self.total_steps = total_steps
        self.version = version
        self.affected_pods = affected_pods

    def parse_deployment_step(self, step):
        if step.__class__ == dict:
            # This is what Marathon 1.0.0 returns: steps
            return MarathonDeploymentStep().from_json(step)
        elif step.__class__ == list:
            # This is Marathon < 1.0.0 style, a list of actions
            return [s if isinstance(s, MarathonDeploymentAction) else MarathonDeploymentAction().from_json(s) for s in step]
        else:
            return step


class MarathonDeploymentAction(MarathonObject):

    """Marathon Application resource.

    See: https://mesosphere.github.io/marathon/docs/rest-api.html#deployments

    :param str action: action
    :param str app: app id
    :param str apps: app id (see https://github.com/mesosphere/marathon/pull/802)
    :param type readiness_check_results: Undocumented
    """

    def __init__(self, action=None, app=None, apps=None, type=None, readiness_check_results=None, pod=None):
        self.action = action
        self.app = app
        self.apps = apps
        self.pod = pod
        self.type = type  # TODO: Remove builtin shadow
        self.readiness_check_results = readiness_check_results  # TODO: The docs say this is called just "readinessChecks?"


class MarathonDeploymentPlan(MarathonObject):

    def __init__(self, original=None, target=None,
                 steps=None, id=None, version=None):
        self.original = MarathonDeploymentOriginalState.from_json(original)
        self.target = MarathonDeploymentTargetState.from_json(target)
        self.steps = [MarathonDeploymentStep.from_json(x) for x in steps]
        self.id = id
        self.version = version


class MarathonDeploymentStep(MarathonObject):

    def __init__(self, actions=None):
        self.actions = [a if isinstance(a, MarathonDeploymentAction) else MarathonDeploymentAction.from_json(a) for a in (actions or [])]


class MarathonDeploymentOriginalState(MarathonObject):

    def __init__(self, dependencies=None,
                 apps=None, id=None, version=None, groups=None, pods=None):
        self.apps = apps
        self.groups = groups
        self.id = id
        self.version = version
        self.dependencies = dependencies
        self.pods = pods


class MarathonDeploymentTargetState(MarathonObject):

    def __init__(self, groups=None, apps=None,
                 dependencies=None, id=None, version=None, pods=None):
        self.apps = apps
        self.groups = groups
        self.id = id
        self.version = version
        self.dependencies = dependencies
        self.pods = pods
