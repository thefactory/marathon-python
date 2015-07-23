import mock
import requests_mock
from marathon import MarathonClient


@requests_mock.mock()
def test_get_deployments(m):
    fake_response = '[ { "affectedApps": [ "/test" ], "id": "867ed450-f6a8-4d33-9b0e-e11c5513990b", "steps": [ [ { "action": "ScaleApplication", "app": "/test" } ] ], "currentActions": [ { "action": "ScaleApplication", "app": "/test" } ], "version": "2014-08-26T08:18:03.595Z", "currentStep": 1, "totalSteps": 1 } ]'
    m.get('http://fake_server/v2/deployments', text=fake_response)
    mock_client = MarathonClient(servers='http://fake_server')
    response = mock_client.list_deployments()
    print response
