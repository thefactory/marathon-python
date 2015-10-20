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


@requests_mock.mock()
def test_list_tasks_with_app_id(m):
    fake_response = '{ "tasks": [ { "appId": "/anapp", "healthCheckResults": [ { "alive": true, "consecutiveFailures": 0, "firstSuccess": "2014-10-03T22:57:02.246Z", "lastFailure": null, "lastSuccess": "2014-10-03T22:57:41.643Z", "taskId": "bridged-webapp.eb76c51f-4b4a-11e4-ae49-56847afe9799" } ], "host": "10.141.141.10", "id": "bridged-webapp.eb76c51f-4b4a-11e4-ae49-56847afe9799", "ports": [ 31000 ], "servicePorts": [ 9000 ], "stagedAt": "2014-10-03T22:16:27.811Z", "startedAt": "2014-10-03T22:57:41.587Z", "version": "2014-10-03T22:16:23.634Z" }, { "appId": "/anotherapp", "healthCheckResults": [ { "alive": true, "consecutiveFailures": 0, "firstSuccess": "2014-10-03T22:57:02.246Z", "lastFailure": null, "lastSuccess": "2014-10-03T22:57:41.649Z", "taskId": "bridged-webapp.ef0b5d91-4b4a-11e4-ae49-56847afe9799" } ], "host": "10.141.141.10", "id": "bridged-webapp.ef0b5d91-4b4a-11e4-ae49-56847afe9799", "ports": [ 31001 ], "servicePorts": [ 9000 ], "stagedAt": "2014-10-03T22:16:33.814Z", "startedAt": "2014-10-03T22:57:41.593Z", "version": "2014-10-03T22:16:23.634Z" } ] }'
    m.get('http://fake_server/v2/tasks', text=fake_response)
    mock_client = MarathonClient(servers='http://fake_server')
    actual_deployments = mock_client.list_tasks(app_id='/anapp')
    expected_deployments = [ models.task.MarathonTask(
        app_id="/anapp",
        health_check_results= [
            models.task.MarathonHealthCheckResult(
                alive= True,
                consecutive_failures= 0,
                first_success= "2014-10-03T22:57:02.246Z",
                last_failure= None,
                last_success= "2014-10-03T22:57:41.643Z",
                task_id= "bridged-webapp.eb76c51f-4b4a-11e4-ae49-56847afe9799"
            )
        ],
        host= "10.141.141.10",
        id= "bridged-webapp.eb76c51f-4b4a-11e4-ae49-56847afe9799",
        ports= [
            31000
        ],
        service_ports= [
            9000
        ],
        staged_at= "2014-10-03T22:16:27.811Z",
        started_at= "2014-10-03T22:57:41.587Z",
        version= "2014-10-03T22:16:23.634Z"
    )]
    assert actual_deployments == expected_deployments


@requests_mock.mock()
def test_list_tasks_without_app_id(m):
    fake_response = '{ "tasks": [ { "appId": "/anapp", "healthCheckResults": [ { "alive": true, "consecutiveFailures": 0, "firstSuccess": "2014-10-03T22:57:02.246Z", "lastFailure": null, "lastSuccess": "2014-10-03T22:57:41.643Z", "taskId": "bridged-webapp.eb76c51f-4b4a-11e4-ae49-56847afe9799" } ], "host": "10.141.141.10", "id": "bridged-webapp.eb76c51f-4b4a-11e4-ae49-56847afe9799", "ports": [ 31000 ], "servicePorts": [ 9000 ], "stagedAt": "2014-10-03T22:16:27.811Z", "startedAt": "2014-10-03T22:57:41.587Z", "version": "2014-10-03T22:16:23.634Z" }, { "appId": "/anotherapp", "healthCheckResults": [ { "alive": true, "consecutiveFailures": 0, "firstSuccess": "2014-10-03T22:57:02.246Z", "lastFailure": null, "lastSuccess": "2014-10-03T22:57:41.649Z", "taskId": "bridged-webapp.ef0b5d91-4b4a-11e4-ae49-56847afe9799" } ], "host": "10.141.141.10", "id": "bridged-webapp.ef0b5d91-4b4a-11e4-ae49-56847afe9799", "ports": [ 31001 ], "servicePorts": [ 9000 ], "stagedAt": "2014-10-03T22:16:33.814Z", "startedAt": "2014-10-03T22:57:41.593Z", "version": "2014-10-03T22:16:23.634Z" } ] }'
    m.get('http://fake_server/v2/tasks', text=fake_response)
    mock_client = MarathonClient(servers='http://fake_server')
    actual_deployments = mock_client.list_tasks()
    expected_deployments = [
    models.task.MarathonTask(
        app_id="/anapp",
        health_check_results= [
            models.task.MarathonHealthCheckResult(
                alive= True,
                consecutive_failures= 0,
                first_success= "2014-10-03T22:57:02.246Z",
                last_failure= None,
                last_success= "2014-10-03T22:57:41.643Z",
                task_id= "bridged-webapp.eb76c51f-4b4a-11e4-ae49-56847afe9799"
            )
        ],
        host= "10.141.141.10",
        id="bridged-webapp.eb76c51f-4b4a-11e4-ae49-56847afe9799",
        ports= [
            31000
        ],
        service_ports= [
            9000
        ],
        staged_at= "2014-10-03T22:16:27.811Z",
        started_at= "2014-10-03T22:57:41.587Z",
        version= "2014-10-03T22:16:23.634Z"
    ),
    models.task.MarathonTask(
        app_id= "/anotherapp",
        health_check_results= [
            models.task.MarathonHealthCheckResult(
                alive= True,
                consecutive_failures= 0,
                first_success = "2014-10-03T22:57:02.246Z",
                last_failure= None,
                last_success= "2014-10-03T22:57:41.649Z",
                task_id= "bridged-webapp.ef0b5d91-4b4a-11e4-ae49-56847afe9799"
            )
        ],
        host= "10.141.141.10",
        id= "bridged-webapp.ef0b5d91-4b4a-11e4-ae49-56847afe9799",
        ports= [ 31001 ],
        service_ports= [ 9000 ],
        staged_at = "2014-10-03T22:16:33.814Z",
        started_at= "2014-10-03T22:57:41.593Z",
        version= "2014-10-03T22:16:23.634Z"
    )]
    assert actual_deployments == expected_deployments
