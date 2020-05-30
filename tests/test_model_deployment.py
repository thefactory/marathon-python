from marathon.models.deployment import MarathonDeployment
import unittest


class MarathonDeploymentTest(unittest.TestCase):

    def test_env_defaults_to_empty_dict(self):
        """
        é testé
        """
        deployment_json ={"id": "ID", "version": "2020-05-30T07:35:04.695Z", "affectedApps": ["/app"], "affectedPods": [], "steps": [{"actions": [{"action": "RestartApplication", "app": "/app"}]}], "currentActions": [{"action": "RestartApplication", "app": "/app", "readinessCheckResults": []}], "currentStep": 1, "totalSteps": 1}
        
        deployment = MarathonDeployment.from_json(deployment_json)
        self.assertEquals(deployment.id, "ID")
        self.assertEquals(deployment.current_actions[0].app, "/app")

