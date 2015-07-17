## 0.7.2 (<not-yet-released>)

Support for Marathon 0.9.0

Changes:
* Add `accepted_resource_role` field to `MarathonApp`

## 0.7.1 (2015-07-14)

Critical fixes and @solarkennedy has been addded as a contributor!

Changes (all @solarkennedy - huge thanks):
* Fixed `MarathonApp` regex issue
* Hooked up Travis CI
* Added integration tests

## 0.7.0 (2015-07-05)

Support for Marathon 0.8.2

Changes:
* Tests (huge thanks @kevinschoon)
* Added support for Marathon EventBus (thanks @kevinschoon)
* Marathon app_id and group_id validation (thanks @mattrobenolt)
* Fixed bug in creation of deployment.steps list (thanks @AFriemann)
* Add `ignore_http1xx` on `MarathonHealthCheck` (thanks @mrtheb)

## 0.6.15 (2015-06-05)

Changes:
* Fix `force_pull_image` on `MarathonDockerContainer` (thanks @mattrobenolt)

## 0.6.14 (2015-05-28)

Changes:
* Add `force_pull_image` field to `MarathonDockerContainer` (thanks @solarkennedy)
* Add `kwargs` to `MarathonDockerContainer` for better forward compatibility (thanks @g----)
* Fix issue with `use_2to3` (thanks @vitan)

## 0.6.13 (2015-03-24)

Support for Marathon 0.8.1

Changes:
* Better handling of nulls and empty collections (thanks @wndhydrnt)
* Updated object signatures to match 0.8.1 (thanks @pradeepchhetri)

## 0.6.12 (2015-03-06)

Changes:
* Replace defunct `MarathonEndpoint` resource with a working helper object

## 0.6.11 (2015-03-06)

Support for Marathon 0.8.0

## 0.6.10 (2014-12-17)

Changes:
* Added `force` option to `delete_deployment()`

## 0.6.9 (2014-12-03)

Changes:
* Added lastFailureCause field to app.lastTaskFailure
* Added `parameters` and `privileged` fields to `MarathonContainer`

## 0.6.8 (2014-11-18)

Changes:
* (Temporarily) Added `apps` field to `DeploymentAction` (https://github.com/mesosphere/marathon/pull/802)

## 0.6.7 (2014-11-18)

Changes:
* Updated `list_tasks()` and `get_info()` to match latest Marathon response signature
* Fixed `__repr__` for `MarathonInfo()` and other `MarathonResources` without `id

## 0.6.6 (2014-11-17)

Changes:
* Improved behavior of `MarathonClient.update_app()` to strip `version` from the passed `app`

## 0.6.5 (2014-11-14)

Changes:
* Fixed bug with `MarathonClient.scale_app()` and add `force` support

## 0.6.4 (2014-11-13)

Support for Marathon 0.7.5

Changes:
* Added support for app.lastTaskFailure
* Added support for task.healthCheckResult
* Fixed support for app.upgradeStrategy

## 0.6.3 (2014-10-10)

Changes:
* Added support for embedding tasks in get/list app results
* Switched to patch-style updates for apps and groups (send partial object)

## 0.6.2 (2014-10-09)

Changes:
* Added support for service port in container port mappings (Marathon 0.7.3)

## 0.6.2 (2014-10-09)

Changes:
* Added support for LIKE and UNLIKE constraint operators
* Added support for patch-style app and group updates

## 0.6.1 (2014-09-29)

Changes:
* Fixed broken exception import

## 0.6.0 (2014-09-29)

Mesos 0.20.1- and Marathon 0.7.1-compatible release.

Changes:
* Added bridge networking support
* Use common exception for all pick-from-a-list options (`InvalidChoiceError`). `InvalidOperatorError` has been removed
* Updated `MarathonObject.__repr__` to be more useful
* Changed default HTTP request timeout from 5s to 10s

## 0.5.1 (2014-09-18)

Changes:
* Added support for multiple Marathon servers (if a request to one fails for network reasons, try the next)
* Fixed a bug with HTTP 4xx response handling

## 0.5.0 (2014-09-15)

Initial release compatible with Marathon 0.7.0 and Mesos 0.20.0.

_Warning: this includes multiple breaking changes, both from Marathon and from this library_

Changes:
* Added support for Deployments, Groups, native Docker containers, Queue, Server Info, Server Metrics, and Ping
* Updated object attributes to be at parity with Marathon 0.7.0 (RC2)
* Updated return types to be at parity with Marathon 0.7.0 (RC2)
* Updated method signatures to be more consistent
* HTTP 4xx errors other than 404 now throw `MarathonHttpError` instead of `NotFoundError`
* `json_encode()` and `json_decode()` on MarathonResource have been renamed to `to_json()` and `from_json()`, respectively
* Refactored serialization/deserialization to reduce boilerplate
