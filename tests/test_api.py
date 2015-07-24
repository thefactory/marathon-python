import mock
import requests_mock
from marathon import MarathonClient
from marathon import models


@requests_mock.mock()
def test_get_deployments(m):
    fake_response = '[ { "affectedApps": [ "/test" ], "id": "fakeid", "steps": [ [ { "action": "ScaleApplication", "app": "/test" } ] ], "currentActions": [ { "action": "ScaleApplication", "app": "/test" } ], "version": "fakeversion", "currentStep": 1, "totalSteps": 1 } ]'
    m.get('http://fake_server/v2/deployments', text=fake_response)
    mock_client = MarathonClient(servers='http://fake_server')
    actual_deployments = mock_client.list_deployments()
    expected_deployments = [ models.MarathonDeployment(
        id=u"fakeid",
        steps=[[models.MarathonDeploymentAction(action="ScaleApplication", app="/test")]],
        current_actions=[models.MarathonDeploymentAction(action="ScaleApplication", app="/test")],
        current_step=1,
        total_steps=1,
        affected_apps=[u"/test"],
        version=u"fakeversion"
    )]
    assert expected_deployments == actual_deployments
