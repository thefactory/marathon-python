import requests_mock
from marathon import MarathonClient
from marathon import models


def test_get_deployments_pre_1_0():
    fake_response = """[
      {
        "affectedApps": [
          "/test"
        ],
        "id": "fakeid",
        "steps": [
          [
            {
              "action": "ScaleApplication",
              "app": "/test"
            }
          ]
        ],
        "currentActions": [
          {
            "action": "ScaleApplication",
            "app": "/test"
          }
        ],
        "version": "fakeversion",
        "currentStep": 1,
        "totalSteps": 1
      }
    ]"""
    with requests_mock.mock() as m:
        m.get('http://fake_server/v2/deployments', text=fake_response)
        mock_client = MarathonClient(servers='http://fake_server')
        actual_deployments = mock_client.list_deployments()
        expected_deployments = [models.MarathonDeployment(
            id=u"fakeid",
            steps=[
                [models.MarathonDeploymentAction(
                    action="ScaleApplication", app="/test")]],
            current_actions=[models.MarathonDeploymentAction(
                action="ScaleApplication", app="/test")],
            current_step=1,
            total_steps=1,
            affected_apps=[u"/test"],
            version=u"fakeversion"
        )]
        assert expected_deployments == actual_deployments


def test_get_deployments_post_1_0():
    fake_response = """[
      {
        "id": "4d2ff4d8-fbe5-4239-a886-f0831ed68d20",
        "version": "2016-04-20T18:00:20.084Z",
        "affectedApps": [
          "/test-trivial-app"
        ],
        "steps": [
          {
            "actions": [
              {
                "type": "StartApplication",
                "app": "/test-trivial-app"
              }
            ]
          },
          {
            "actions": [
              {
                "type": "ScaleApplication",
                "app": "/test-trivial-app"
              }
            ]
          }
        ],
        "currentActions": [
          {
            "action": "ScaleApplication",
            "app": "/test-trivial-app",
            "readinessCheckResults": []
          }
        ],
        "currentStep": 2,
        "totalSteps": 2
      }
    ]"""
    with requests_mock.mock() as m:
        m.get('http://fake_server/v2/deployments', text=fake_response)
        mock_client = MarathonClient(servers='http://fake_server')
        actual_deployments = mock_client.list_deployments()
        expected_deployments = [models.MarathonDeployment(
            id=u"4d2ff4d8-fbe5-4239-a886-f0831ed68d20",
            steps=[
                models.MarathonDeploymentStep(
                    actions=[models.MarathonDeploymentAction(
                        type="StartApplication", app="/test-trivial-app")],
                ),
                models.MarathonDeploymentStep(
                    actions=[models.MarathonDeploymentAction(
                        type="ScaleApplication", app="/test-trivial-app")],
                ),
            ],
            current_actions=[models.MarathonDeploymentAction(
                action="ScaleApplication", app="/test-trivial-app", readiness_check_results=[])
            ],
            current_step=2,
            total_steps=2,
            affected_apps=[u"/test-trivial-app"],
            version=u"2016-04-20T18:00:20.084Z"
        )]
        # Helpful for tox to see the diff
        assert expected_deployments[0].__dict__ == actual_deployments[0].__dict__
        assert expected_deployments == actual_deployments


def test_list_tasks_with_app_id():
    fake_response = '{ "tasks": [ { "appId": "/anapp", "healthCheckResults": ' \
                    '[ { "alive": true, "consecutiveFailures": 0, "firstSuccess": "2014-10-03T22:57:02.246Z", ' \
                    '"lastFailure": null, "lastSuccess": "2014-10-03T22:57:41.643Z", "taskId": "bridged-webapp.eb76c51f-4b4a-11e4-ae49-56847afe9799" } ],' \
                    ' "host": "10.141.141.10", "id": "bridged-webapp.eb76c51f-4b4a-11e4-ae49-56847afe9799", "ports": [ 31000 ], ' \
                    '"servicePorts": [ 9000 ], "stagedAt": "2014-10-03T22:16:27.811Z", "startedAt": "2014-10-03T22:57:41.587Z", ' \
                    '"version": "2014-10-03T22:16:23.634Z" }]}'
    with requests_mock.mock() as m:
        m.get('http://fake_server/v2/apps//anapp/tasks', text=fake_response)
        mock_client = MarathonClient(servers='http://fake_server')
        actual_deployments = mock_client.list_tasks(app_id='/anapp')
        expected_deployments = [models.task.MarathonTask(
            app_id="/anapp",
            health_check_results=[
                models.task.MarathonHealthCheckResult(
                    alive=True,
                    consecutive_failures=0,
                    first_success="2014-10-03T22:57:02.246Z",
                    last_failure=None,
                    last_success="2014-10-03T22:57:41.643Z",
                    task_id="bridged-webapp.eb76c51f-4b4a-11e4-ae49-56847afe9799"
                )
            ],
            host="10.141.141.10",
            id="bridged-webapp.eb76c51f-4b4a-11e4-ae49-56847afe9799",
            ports=[
                31000
            ],
            service_ports=[
                9000
            ],
            staged_at="2014-10-03T22:16:27.811Z",
            started_at="2014-10-03T22:57:41.587Z",
            version="2014-10-03T22:16:23.634Z"
        )]
        assert actual_deployments == expected_deployments


def test_list_tasks_without_app_id():
    fake_response = '{ "tasks": [ { "appId": "/anapp", "healthCheckResults": ' \
                    '[ { "alive": true, "consecutiveFailures": 0, "firstSuccess": "2014-10-03T22:57:02.246Z", "lastFailure": null, ' \
                    '"lastSuccess": "2014-10-03T22:57:41.643Z", "taskId": "bridged-webapp.eb76c51f-4b4a-11e4-ae49-56847afe9799" } ],' \
                    ' "host": "10.141.141.10", "id": "bridged-webapp.eb76c51f-4b4a-11e4-ae49-56847afe9799", "ports": [ 31000 ], ' \
                    '"servicePorts": [ 9000 ], "stagedAt": "2014-10-03T22:16:27.811Z", "startedAt": "2014-10-03T22:57:41.587Z", ' \
                    '"version": "2014-10-03T22:16:23.634Z" }, { "appId": "/anotherapp", ' \
                    '"healthCheckResults": [ { "alive": true, "consecutiveFailures": 0, "firstSuccess": "2014-10-03T22:57:02.246Z", ' \
                    '"lastFailure": null, "lastSuccess": "2014-10-03T22:57:41.649Z", "taskId": "bridged-webapp.ef0b5d91-4b4a-11e4-ae49-56847afe9799" } ], ' \
                    '"host": "10.141.141.10", "id": "bridged-webapp.ef0b5d91-4b4a-11e4-ae49-56847afe9799", "ports": [ 31001 ], "servicePorts": [ 9000 ], ' \
                    '"stagedAt": "2014-10-03T22:16:33.814Z", "startedAt": "2014-10-03T22:57:41.593Z", "version": "2014-10-03T22:16:23.634Z" } ] }'
    with requests_mock.mock() as m:
        m.get('http://fake_server/v2/tasks', text=fake_response)
        mock_client = MarathonClient(servers='http://fake_server')
        actual_deployments = mock_client.list_tasks()
        expected_deployments = [
            models.task.MarathonTask(
                app_id="/anapp",
                health_check_results=[
                    models.task.MarathonHealthCheckResult(
                        alive=True,
                        consecutive_failures=0,
                        first_success="2014-10-03T22:57:02.246Z",
                        last_failure=None,
                        last_success="2014-10-03T22:57:41.643Z",
                        task_id="bridged-webapp.eb76c51f-4b4a-11e4-ae49-56847afe9799"
                    )
                ],
                host="10.141.141.10",
                id="bridged-webapp.eb76c51f-4b4a-11e4-ae49-56847afe9799",
                ports=[
                    31000
                ],
                service_ports=[
                    9000
                ],
                staged_at="2014-10-03T22:16:27.811Z",
                started_at="2014-10-03T22:57:41.587Z",
                version="2014-10-03T22:16:23.634Z"
            ),
            models.task.MarathonTask(
                app_id="/anotherapp",
                health_check_results=[
                    models.task.MarathonHealthCheckResult(
                        alive=True,
                        consecutive_failures=0,
                        first_success="2014-10-03T22:57:02.246Z",
                        last_failure=None,
                        last_success="2014-10-03T22:57:41.649Z",
                        task_id="bridged-webapp.ef0b5d91-4b4a-11e4-ae49-56847afe9799"
                    )
                ],
                host="10.141.141.10",
                id="bridged-webapp.ef0b5d91-4b4a-11e4-ae49-56847afe9799",
                ports=[31001],
                service_ports=[9000],
                staged_at="2014-10-03T22:16:33.814Z",
                started_at="2014-10-03T22:57:41.593Z",
                version="2014-10-03T22:16:23.634Z"
            )]
        assert actual_deployments == expected_deployments
